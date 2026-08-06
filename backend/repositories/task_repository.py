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
