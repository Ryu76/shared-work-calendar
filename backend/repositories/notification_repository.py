"""Database access for local in-app notification persistence."""
from __future__ import annotations

from typing import Any


class NotificationRepository:
    """Perform only notification preference persistence operations."""

    @staticmethod
    def preference(connection: Any, user_id: int, updated_at: str) -> Any:
        """Lazily create and return the user's unchanged local preference row."""
        connection.execute(
            "INSERT INTO notification_preferences(user_id,due_soon_enabled,overdue_enabled,updated_at) "
            "VALUES(?,1,1,?) ON CONFLICT(user_id) DO NOTHING",
            (user_id, updated_at),
        )
        return connection.execute(
            "SELECT * FROM notification_preferences WHERE user_id=?", (user_id,)
        ).fetchone()

    @staticmethod
    def update_preferences(
        connection: Any,
        user_id: int,
        due_soon_enabled: bool,
        overdue_enabled: bool,
        updated_at: str,
    ) -> None:
        """Persist preferences and remove only newly disabled local-outbox kinds."""
        connection.execute(
            "UPDATE notification_preferences SET due_soon_enabled=?,overdue_enabled=?,updated_at=? WHERE user_id=?",
            (int(due_soon_enabled), int(overdue_enabled), updated_at, user_id),
        )
        if not due_soon_enabled:
            connection.execute(
                "DELETE FROM notification_outbox WHERE user_id=? AND kind IN ('DUE_SOON','DUE_TODAY')",
                (user_id,),
            )
        if not overdue_enabled:
            connection.execute(
                "DELETE FROM notification_outbox WHERE user_id=? AND kind='OVERDUE'",
                (user_id,),
            )
