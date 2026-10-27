"""Database access for task persistence operations."""
from __future__ import annotations

from typing import Any


class TaskRepository:
    """Perform only task-related persistence queries."""

    @staticmethod
    def authorized_task_query(user: Any) -> tuple[str, list[Any]]:
        """Build the established live-task SQL scope for one caller.

        Callers may compose this read scope with task-specific predicates, but the
        authorization SQL itself remains at the task persistence boundary.
        """
        sql = "SELECT t.* FROM tasks t WHERE t.deleted_at IS NULL"
        params: list[Any] = []
        if user["role"] != "ADMIN":
            sql += (
                " AND (t.created_by=? OR EXISTS(SELECT 1 FROM task_assignees ta "
                "WHERE ta.task_id=t.id AND ta.user_id=?))"
            )
            params = [user["id"], user["id"]]
        return sql, params

    @staticmethod
    def live_task_by_id(connection: Any, task_id: int) -> Any:
        """Return one non-deleted task for the established detail authorization flow."""
        return connection.execute(
            "SELECT * FROM tasks WHERE id=? AND deleted_at IS NULL", (task_id,)
        ).fetchone()

    @staticmethod
    def task_has_assignee(connection: Any, task_id: int, user_id: int) -> bool:
        """Report whether one user is assigned to the specified task."""
        return bool(connection.execute(
            "SELECT 1 FROM task_assignees WHERE task_id=? AND user_id=?",
            (task_id, user_id),
        ).fetchone())

    @staticmethod
    def active_user_ids(connection: Any) -> set[int]:
        """Return identifiers eligible to be assigned to a task."""
        return {row["id"] for row in connection.execute("SELECT id FROM users WHERE is_active=1")}

    @staticmethod
    def task_creator_name(connection: Any, user_id: int) -> str:
        """Return the creator name used by the legacy task response projection."""
        return connection.execute(
            "SELECT name FROM users WHERE id=?", (user_id,)
        ).fetchone()["name"]

    @staticmethod
    def task_assignee_rows(connection: Any, task_id: int) -> list[Any]:
        """Return task assignees in the established task-view ordering."""
        return list(connection.execute(
            "SELECT u.id,u.name,u.login_id FROM task_assignees ta "
            "JOIN users u ON u.id=ta.user_id WHERE ta.task_id=? ORDER BY u.name",
            (task_id,),
        ))

    @staticmethod
    def task_contact_row(connection: Any, contact_id: int) -> Any:
        """Return the requester contact projection used by task views."""
        return connection.execute(
            "SELECT rc.id,rc.name,rc.phone,o.name organization FROM request_contacts rc "
            "JOIN organizations o ON o.id=rc.organization_id WHERE rc.id=?",
            (contact_id,),
        ).fetchone()

    @staticmethod
    def task_image_rows(connection: Any, task_id: int) -> list[Any]:
        """Return task image metadata in its established display ordering."""
        return list(connection.execute(
            "SELECT * FROM task_images WHERE task_id=? ORDER BY sort_order,id", (task_id,)
        ))

    @staticmethod
    def task_attachment_rows(connection: Any, task_id: int) -> list[Any]:
        """Return task attachment metadata in its established display ordering."""
        return list(connection.execute(
            "SELECT * FROM task_attachments WHERE task_id=? ORDER BY created_at,id", (task_id,)
        ))

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

    @staticmethod
    def task_image(connection: Any, task_id: int, image_id: int) -> Any:
        """Return one image metadata row belonging to the given task."""
        return connection.execute(
            "SELECT * FROM task_images WHERE id=? AND task_id=?", (image_id, task_id)
        ).fetchone()

    @staticmethod
    def revise_task_image(
        connection: Any,
        task_id: int,
        image_id: int,
        source_storage_key: str,
        result_storage_key: str,
        direction: str,
        edited_by: int,
        created_at: str,
        size_bytes: int,
    ) -> Any:
        """Persist one non-destructive image revision and return its updated image row."""
        connection.execute(
            "INSERT INTO task_image_edits(task_id,image_id,source_storage_key,result_storage_key,direction,edited_by,created_at) VALUES(?,?,?,?,?,?,?)",
            (
                task_id,
                image_id,
                source_storage_key,
                result_storage_key,
                direction,
                edited_by,
                created_at,
            ),
        )
        connection.execute(
            "UPDATE task_images SET storage_key=?,size_bytes=? WHERE id=?",
            (result_storage_key, size_bytes, image_id),
        )
        return connection.execute("SELECT * FROM task_images WHERE id=?", (image_id,)).fetchone()

    @staticmethod
    def delete_task_image(connection: Any, image_id: int) -> list[str]:
        """Delete image metadata and return every private image key retained for it."""
        source_keys = [
            row["source_storage_key"]
            for row in connection.execute(
                "SELECT source_storage_key FROM task_image_edits WHERE image_id=?", (image_id,)
            )
        ]
        connection.execute("DELETE FROM task_images WHERE id=?", (image_id,))
        return source_keys

    @staticmethod
    def attachment_count(connection: Any, task_id: int) -> int:
        """Return the current number of document/video attachments on one task."""
        return connection.execute(
            "SELECT COUNT(*) FROM task_attachments WHERE task_id=?", (task_id,)
        ).fetchone()[0]

    @staticmethod
    def create_task_attachment(
        connection: Any,
        task_id: int,
        storage_key: str,
        original_filename: str,
        mime_type: str,
        attachment_type: str,
        size_bytes: int,
        sha256: str,
        uploaded_by: int,
        created_at: str,
    ) -> Any:
        """Persist and return one task-attachment metadata row."""
        attachment_id = connection.execute(
            "INSERT INTO task_attachments(task_id,storage_key,original_filename,mime_type,attachment_type,size_bytes,sha256,uploaded_by,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
            (
                task_id,
                storage_key,
                original_filename,
                mime_type,
                attachment_type,
                size_bytes,
                sha256,
                uploaded_by,
                created_at,
            ),
        ).lastrowid
        return connection.execute(
            "SELECT * FROM task_attachments WHERE id=?", (attachment_id,)
        ).fetchone()

    @staticmethod
    def task_attachment(connection: Any, task_id: int, attachment_id: int) -> Any:
        """Return one attachment metadata row belonging to the given task."""
        return connection.execute(
            "SELECT * FROM task_attachments WHERE id=? AND task_id=?",
            (attachment_id, task_id),
        ).fetchone()

    @staticmethod
    def delete_task_attachment(connection: Any, attachment_id: int) -> None:
        """Delete one task-attachment metadata row after service authorization."""
        connection.execute("DELETE FROM task_attachments WHERE id=?", (attachment_id,))

    @staticmethod
    def task_history_rows(connection: Any, task_id: int) -> list[Any]:
        """Return persisted audit rows for one task in the legacy display order."""
        return list(
            connection.execute(
                "SELECT a.id,a.action,a.before_data,a.after_data,a.created_at,u.name actor_name "
                "FROM audit_logs a LEFT JOIN users u ON u.id=a.actor_user_id "
                "WHERE a.target_type='TASK' AND a.target_id=? ORDER BY a.id DESC",
                (str(task_id),),
            )
        )

    @staticmethod
    def users_by_ids(connection: Any, user_ids: list[int]) -> dict[int, str]:
        """Return a mapping of user ID to name for the given user IDs."""
        if not user_ids:
            return {}
        placeholders = ",".join("?" for _ in user_ids)
        rows = connection.execute(f"SELECT id, name FROM users WHERE id IN ({placeholders})", user_ids)
        return {row["id"]: row["name"] for row in rows}

    @staticmethod
    def contacts_by_ids(connection: Any, contact_ids: list[int]) -> dict[int, dict]:
        """Return a mapping of contact ID to contact projection for the given IDs."""
        if not contact_ids:
            return {}
        placeholders = ",".join("?" for _ in contact_ids)
        rows = connection.execute(
            f"SELECT rc.id, rc.name, rc.phone, o.name AS organization "
            f"FROM request_contacts rc JOIN organizations o ON o.id = rc.organization_id "
            f"WHERE rc.id IN ({placeholders})",
            contact_ids
        )
        return {
            row["id"]: {"id": row["id"], "name": row["name"], "phone": row["phone"], "organization": row["organization"]}
            for row in rows
        }

    @staticmethod
    def assignees_by_task_ids(connection: Any, task_ids: list[int]) -> list[Any]:
        """Return assignees for the given task IDs in established task-view ordering."""
        if not task_ids:
            return []
        placeholders = ",".join("?" for _ in task_ids)
        return list(connection.execute(
            f"SELECT ta.task_id, u.id, u.name, u.login_id FROM task_assignees ta "
            f"JOIN users u ON u.id = ta.user_id WHERE ta.task_id IN ({placeholders}) "
            f"ORDER BY ta.task_id, u.name",
            task_ids
        ))

    @staticmethod
    def images_by_task_ids(connection: Any, task_ids: list[int]) -> list[Any]:
        """Return task image metadata for the given task IDs in established display ordering."""
        if not task_ids:
            return []
        placeholders = ",".join("?" for _ in task_ids)
        return list(connection.execute(
            f"SELECT * FROM task_images WHERE task_id IN ({placeholders}) "
            f"ORDER BY task_id, sort_order, id",
            task_ids
        ))

    @staticmethod
    def attachments_by_task_ids(connection: Any, task_ids: list[int]) -> list[Any]:
        """Return task attachment metadata for the given task IDs in established display ordering."""
        if not task_ids:
            return []
        placeholders = ",".join("?" for _ in task_ids)
        return list(connection.execute(
            f"SELECT * FROM task_attachments WHERE task_id IN ({placeholders}) "
            f"ORDER BY task_id, created_at, id",
            task_ids
        ))
