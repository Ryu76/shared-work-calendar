"""Database access for task persistence operations."""
from __future__ import annotations

from typing import Any


class TaskRepository:
    """Perform only task-related persistence queries."""

    @staticmethod
    def active_user_ids(connection: Any) -> set[int]:
        """Return identifiers eligible to be assigned to a task."""
        return {row["id"] for row in connection.execute("SELECT id FROM users WHERE is_active=1")}
