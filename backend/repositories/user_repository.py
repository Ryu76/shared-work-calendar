"""Database access for user-account records."""
from __future__ import annotations

from typing import Any


class UserRepository:
    """Perform only the user-row reads needed by user-account operations."""

    @staticmethod
    def active_assignees(connection: Any) -> list[Any]:
        return list(
            connection.execute(
                "SELECT id,name,login_id,role FROM users WHERE is_active=1 ORDER BY name,login_id"
            )
        )
