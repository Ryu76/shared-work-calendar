import unittest
import sqlite3
from unittest.mock import Mock
from app.bootstrap import task_view, image_view, attachment_view, TASK_REPOSITORY
from services.task_projection_service import TaskProjectionService

class TestTaskProjections(unittest.TestCase):
    def setUp(self):
        # Memory DB
        self.conn = sqlite3.connect(':memory:')
        self.conn.row_factory = sqlite3.Row

        # Schema matching minimal required for testing projections
        self.conn.executescript("""
        CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT, login_id TEXT, is_active INTEGER);
        CREATE TABLE organizations(id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE request_contacts(id INTEGER PRIMARY KEY, organization_id INTEGER, name TEXT, phone TEXT);
        CREATE TABLE tasks(
            id INTEGER PRIMARY KEY,
            requester_contact_id INTEGER,
            status TEXT,
            description TEXT,
            received_date TEXT,
            completed_date TEXT,
            due_date TEXT,
            created_by INTEGER,
            created_at TEXT,
            updated_at TEXT,
            deleted_at TEXT
        );
        CREATE TABLE task_assignees(task_id INTEGER, user_id INTEGER, assigned_at TEXT);
        CREATE TABLE task_images(id INTEGER PRIMARY KEY, task_id INTEGER, storage_key TEXT, original_filename TEXT, mime_type TEXT, size_bytes INTEGER, sort_order INTEGER, created_by INTEGER, created_at TEXT);
        CREATE TABLE task_attachments(id INTEGER PRIMARY KEY, task_id INTEGER, storage_key TEXT, original_filename TEXT, mime_type TEXT, attachment_type TEXT, size_bytes INTEGER, sha256 TEXT, uploaded_by INTEGER, created_at TEXT);
        """)

        # Insert test data
        self.conn.executescript("""
        INSERT INTO users(id, name, login_id, is_active) VALUES (1, 'Creator1', 'c1', 1);
        INSERT INTO users(id, name, login_id, is_active) VALUES (2, 'Assignee1', 'a1', 1);
        INSERT INTO users(id, name, login_id, is_active) VALUES (3, 'Assignee2', 'a2', 0); -- Inactive assignee

        INSERT INTO organizations(id, name) VALUES (1, 'Org1');
        INSERT INTO request_contacts(id, organization_id, name, phone) VALUES (1, 1, 'Contact1', '123-4567');

        -- Create 305 tasks (to test chunk boundary > 300)
        """)

        for i in range(1, 306):
            self.conn.execute("""
            INSERT INTO tasks(id, requester_contact_id, status, description, received_date, created_by)
            VALUES (?, 1, 'RECEIVED', 'Task ' || ?, '2026-10-01', 1)
            """, (i, i))

            # Assignees for first 5 tasks
            if i <= 5:
                self.conn.execute("INSERT INTO task_assignees(task_id, user_id) VALUES (?, 2)", (i,))
                self.conn.execute("INSERT INTO task_assignees(task_id, user_id) VALUES (?, 3)", (i,))

            # Images/Attachments for task 1
            if i == 1:
                self.conn.execute("INSERT INTO task_images(id, task_id, sort_order, original_filename) VALUES (1, 1, 1, 'img1.png')")
                self.conn.execute("INSERT INTO task_images(id, task_id, sort_order, original_filename) VALUES (2, 1, 0, 'img2.png')") # Order check
                self.conn.execute("INSERT INTO task_attachments(id, task_id, created_at, original_filename) VALUES (1, 1, '2026-10-01T10:00:00Z', 'doc1.pdf')")

        self.service = TaskProjectionService(TASK_REPOSITORY, image_view, attachment_view)

    def tearDown(self):
        self.conn.close()

    def test_empty_list_no_queries(self):
        # Enable trace to count queries
        queries = []
        self.conn.set_trace_callback(queries.append)
        result = self.service.task_views(self.conn, [])
        self.assertEqual(result, [])
        self.assertEqual(len(queries), 0)
        self.conn.set_trace_callback(None)

    def test_bulk_projection_equals_legacy(self):
        tasks = self.conn.execute("SELECT * FROM tasks WHERE id <= 5").fetchall()

        # Legacy
        legacy_results = [task_view(self.conn, task) for task in tasks]

        # Bulk
        queries = []
        self.conn.set_trace_callback(queries.append)
        bulk_results = self.service.task_views(self.conn, tasks)
        self.conn.set_trace_callback(None)

        self.assertEqual(legacy_results, bulk_results)

        # Check image order (sort_order 0 should be first)
        self.assertEqual(bulk_results[0]['images'][0]['original_filename'], 'img2.png')
        self.assertEqual(bulk_results[0]['images'][1]['original_filename'], 'img1.png')

        # Check inactive assignee included
        assignees = bulk_results[0]['assignees']
        self.assertEqual(len(assignees), 2)

    def test_chunk_boundary(self):
        tasks = self.conn.execute("SELECT * FROM tasks").fetchall()
        self.assertEqual(len(tasks), 305)

        queries = []
        self.conn.set_trace_callback(queries.append)
        bulk_results = self.service.task_views(self.conn, tasks)
        self.conn.set_trace_callback(None)

        self.assertEqual(len(bulk_results), 305)
        # 5 queries (creators, contacts, assignees, images, attachments) * 2 chunks (since > 300) = 10 queries
        self.assertTrue(len(queries) <= 10, f"Expected bounded queries, got {len(queries)}")

    def test_projection_query_budget_does_not_grow_with_page_size(self):
        tasks = self.conn.execute("SELECT * FROM tasks WHERE id <= 20").fetchall()
        queries = []
        self.conn.set_trace_callback(queries.append)
        expected = [task_view(self.conn, task) for task in tasks]
        legacy_count = len(queries)
        queries.clear()
        actual = self.service.task_views(self.conn, tasks)
        bulk_count = len(queries)
        self.conn.set_trace_callback(None)
        self.assertEqual(actual, expected)
        self.assertEqual(legacy_count, len(tasks) * 5)
        self.assertEqual(bulk_count, 5)
        print(f"PROJECTION_SELECTS rows={len(tasks)} legacy={legacy_count} bulk={bulk_count}")

    def test_repeated_input_rows_do_not_duplicate_related_metadata(self):
        row = self.conn.execute("SELECT * FROM tasks WHERE id=1").fetchone()
        expected = task_view(self.conn, row)
        queries = []
        self.conn.set_trace_callback(queries.append)
        actual = self.service.task_views(self.conn, [row] * 305)
        self.conn.set_trace_callback(None)
        self.assertEqual(actual, [expected] * 305)
        self.assertEqual(len(queries), 5)

    def test_every_related_query_is_chunked_for_distinct_creators_and_contacts(self):
        for task_id in range(1, 306):
            identifier = 1000 + task_id
            self.conn.execute("INSERT INTO users(id,name,login_id,is_active) VALUES(?,?,?,1)", (identifier, f"Creator{task_id}", f"creator-{task_id}"))
            self.conn.execute("INSERT INTO request_contacts(id,organization_id,name,phone) VALUES(?,1,?,?)", (identifier, f"Contact{task_id}", f"phone-{task_id}"))
            self.conn.execute("UPDATE tasks SET created_by=?,requester_contact_id=? WHERE id=?", (identifier, identifier, task_id))
        tasks = self.conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
        expected = [task_view(self.conn, task) for task in tasks]
        queries = []
        self.conn.set_trace_callback(queries.append)
        actual = self.service.task_views(self.conn, tasks)
        self.conn.set_trace_callback(None)
        self.assertEqual(actual, expected)
        self.assertEqual(len(queries), 5 * 2)
        print(f"CHUNKED_PROJECTION_SELECTS rows={len(tasks)} distinct_creators_contacts=305 queries={len(queries)}")

    def test_attachment_ordering_and_requested_task_boundary(self):
        self.conn.execute("INSERT INTO task_attachments(id,task_id,created_at,original_filename) VALUES(2,1,'2026-10-01T09:00:00Z','doc2.pdf')")
        self.conn.execute("INSERT INTO task_attachments(id,task_id,created_at,original_filename) VALUES(3,1,'2026-10-01T09:00:00Z','doc3.pdf')")
        self.conn.execute("INSERT INTO task_images(id,task_id,sort_order,original_filename) VALUES(10,2,0,'unrequested-task.png')")
        tasks = self.conn.execute("SELECT * FROM tasks WHERE id=1").fetchall()
        actual = self.service.task_views(self.conn, tasks)
        self.assertEqual(actual, [task_view(self.conn, tasks[0])])
        self.assertEqual([item['id'] for item in actual[0]['attachments']], [2, 3, 1])
        self.assertNotIn('unrequested-task.png', [item['original_filename'] for item in actual[0]['images']])

if __name__ == '__main__':
    unittest.main()
