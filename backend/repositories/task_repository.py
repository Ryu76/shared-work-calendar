"""Database access for task persistence operations."""
from __future__ import annotations

from typing import Any


class TaskRepository:
    """Perform only task-related persistence queries."""

    @staticmethod
    def active_user_ids(connection: Any) -> set[int]:
        """Return identifiers eligible to be assigned to a task."""
        return {row["id"] for row in connection.execute("SELECT id FROM users WHERE is_active=1")}

    @staticmethod
    def list_tasks(
        connection: Any,
        user: Any,
        task_status: str | None,
        keyword: str,
        received_from: str | None,
        received_to: str | None,
        due_from: str | None,
        due_to: str | None,
        assignee_id: int | None,
        page: int,
        page_size: int,
    ) -> tuple[int, dict[str, int], list[Any]]:
        """Return one authorized filtered task page with its count and status summary."""
        sql = "SELECT t.* FROM tasks t WHERE t.deleted_at IS NULL"
        params: list[Any] = []
        if user["role"] != "ADMIN":
            sql += " AND (t.created_by=? OR EXISTS(SELECT 1 FROM task_assignees ta WHERE ta.task_id=t.id AND ta.user_id=?))"
            params.extend([user["id"], user["id"]])
        if task_status:
            sql += " AND t.status=?"
            params.append(task_status)
        if received_from:
            sql += " AND t.received_date>=?"
            params.append(received_from)
        if received_to:
            sql += " AND t.received_date<=?"
            params.append(received_to)
        if due_from:
            sql += " AND t.due_date>=?"
            params.append(due_from)
        if due_to:
            sql += " AND t.due_date<=?"
            params.append(due_to)
        if keyword:
            sql += (
                " AND (t.description LIKE ? OR EXISTS(SELECT 1 FROM request_contacts rc "
                "JOIN organizations o ON o.id=rc.organization_id WHERE rc.id=t.requester_contact_id "
                "AND (rc.name LIKE ? OR o.name LIKE ?)))"
            )
            params += [f"%{keyword}%"] * 3
        if assignee_id is not None:
            sql += " AND EXISTS(SELECT 1 FROM task_assignees ta_filter WHERE ta_filter.task_id=t.id AND ta_filter.user_id=?)"
            params.append(assignee_id)
        total = connection.execute(f"SELECT COUNT(*) FROM ({sql})", params).fetchone()[0]
        summary = {name: 0 for name in ("RECEIVED", "IN_PROGRESS", "COMPLETED")}
        for row in connection.execute(
            f"SELECT t.status,COUNT(*) count FROM ({sql}) t GROUP BY t.status", params
        ):
            summary[row["status"]] = row["count"]
        rows = list(connection.execute(
            sql + " ORDER BY CASE t.status WHEN 'RECEIVED' THEN 1 WHEN 'IN_PROGRESS' THEN 2 ELSE 3 END,t.received_date DESC,t.id DESC LIMIT ? OFFSET ?",
            [*params, page_size, (page - 1) * page_size],
        ))
        return total, summary, rows

    @staticmethod
    def received_date_calendar(
        connection: Any, user: Any, first_day: str, next_month: str
    ) -> list[Any]:
        """Return authorized live tasks received within one calendar month."""
        sql = "SELECT t.* FROM tasks t WHERE t.deleted_at IS NULL"
        params: list[Any] = []
        if user["role"] != "ADMIN":
            sql += " AND (t.created_by=? OR EXISTS(SELECT 1 FROM task_assignees ta WHERE ta.task_id=t.id AND ta.user_id=?))"
            params.extend([user["id"], user["id"]])
        return list(connection.execute(
            sql + " AND t.received_date>=? AND t.received_date<? ORDER BY t.received_date",
            [*params, first_day, next_month],
        ))

    @staticmethod
    def create_task(
        connection: Any,
        requester_contact_id: int,
        status: str,
        description: str,
        received_date: str,
        completed_date: str | None,
        due_date: str | None,
        created_by: int,
        created_at: str,
        updated_at: str,
        assignee_ids: list[int],
        assigned_at: list[str],
    ) -> tuple[int, Any]:
        """Insert a task, its assignees, and return the persisted task row."""
        cursor = connection.execute(
            "INSERT INTO tasks(requester_contact_id,status,description,received_date,completed_date,due_date,created_by,created_at,updated_at) "
            "VALUES(?,?,?,?,?,?,?,?,?)",
            (
                requester_contact_id,
                status,
                description,
                received_date,
                completed_date,
                due_date,
                created_by,
                created_at,
                updated_at,
            ),
        )
        task_id = cursor.lastrowid
        for assignee_id, timestamp in zip(assignee_ids, assigned_at, strict=True):
            connection.execute(
                "INSERT INTO task_assignees(task_id,user_id,assigned_at) VALUES(?,?,?)",
                (task_id, assignee_id, timestamp),
            )
        task = connection.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        return task_id, task

    @staticmethod
    def update_task(
        connection: Any,
        task_id: int,
        requester_contact_id: int,
        status: str,
        description: str,
        received_date: str,
        completed_date: str | None,
        due_date: str | None,
        updated_at: str,
        refresh_notifications: bool,
        assignee_ids: list[int] | None,
        assigned_at: list[str],
    ) -> Any:
        """Persist one task update and its optional assignee replacement."""
        connection.execute(
            "UPDATE tasks SET requester_contact_id=?,status=?,description=?,received_date=?,completed_date=?,due_date=?,updated_at=? WHERE id=?",
            (
                requester_contact_id,
                status,
                description,
                received_date,
                completed_date,
                due_date,
                updated_at,
                task_id,
            ),
        )
        if refresh_notifications:
            connection.execute("DELETE FROM notification_outbox WHERE task_id=?", (task_id,))
        if assignee_ids is not None:
            connection.execute("DELETE FROM task_assignees WHERE task_id=?", (task_id,))
            for assignee_id, timestamp in zip(assignee_ids, assigned_at, strict=True):
                connection.execute(
                    "INSERT INTO task_assignees(task_id,user_id,assigned_at) VALUES(?,?,?)",
                    (task_id, assignee_id, timestamp),
                )
        return connection.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()

    @staticmethod
    def soft_delete_task(
        connection: Any,
        task_id: int,
        deleted_at: str,
        deleted_by: int,
        updated_at: str,
    ) -> None:
        """Mark one task deleted and clear its local notification outbox rows."""
        connection.execute(
            "UPDATE tasks SET deleted_at=?,deleted_by=?,updated_at=? WHERE id=?",
            (deleted_at, deleted_by, updated_at, task_id),
        )
        connection.execute("DELETE FROM notification_outbox WHERE task_id=?", (task_id,))

    @staticmethod
    def image_count(connection: Any, task_id: int) -> int:
        """Return the current number of images attached to one task."""
        return connection.execute(
            "SELECT COUNT(*) FROM task_images WHERE task_id=?", (task_id,)
        ).fetchone()[0]

    @staticmethod
    def create_task_image(
        connection: Any,
        task_id: int,
        storage_key: str,
        original_filename: str,
        mime_type: str,
        size_bytes: int,
        sort_order: int,
        uploaded_by: int,
        created_at: str,
    ) -> Any:
        """Persist and return one task-image metadata row."""
        image_id = connection.execute(
            "INSERT INTO task_images(task_id,storage_key,original_filename,mime_type,size_bytes,sort_order,uploaded_by,created_at) VALUES(?,?,?,?,?,?,?,?)",
            (
                task_id,
                storage_key,
                original_filename,
                mime_type,
                size_bytes,
                sort_order,
                uploaded_by,
                created_at,
            ),
        ).lastrowid
        return connection.execute("SELECT * FROM task_images WHERE id=?", (image_id,)).fetchone()
