"""Database access for local in-app notification persistence."""
from __future__ import annotations

from typing import Any


class NotificationRepository:
    """Perform only local in-app notification persistence operations."""

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

    @staticmethod
    def mark_read(connection: Any, notification_id: int, user_id: int, read_at: str) -> int:
        """Mark only the caller's local outbox row read and return its update count."""
        updated = connection.execute(
            "UPDATE notification_outbox SET read_at=COALESCE(read_at,?) WHERE id=? AND user_id=?",
            (read_at, notification_id, user_id),
        )
        return updated.rowcount

    @staticmethod
    def clear_disabled_due_kinds(
        connection: Any, user_id: int, due_soon_enabled: bool, overdue_enabled: bool
    ) -> None:
        """Remove only local-outbox kinds disabled by the caller's preferences."""
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

    @staticmethod
    def due_task_rows(connection: Any, task_sql: str, params: list[Any]) -> Any:
        """Return already-authorized incomplete tasks with a due date."""
        return connection.execute(
            task_sql + " AND t.status!='COMPLETED' AND t.due_date IS NOT NULL", params
        )

    @staticmethod
    def add_due_notification(
        connection: Any,
        user_id: int,
        task_id: int,
        kind: str,
        due_date: str,
        message: str,
        created_at: str,
    ) -> None:
        """Insert a local reminder without changing an existing read state."""
        connection.execute(
            "INSERT INTO notification_outbox(user_id,task_id,kind,due_date,message,created_at) "
            "VALUES(?,?,?,?,?,?) ON CONFLICT(user_id,task_id,kind,due_date) DO NOTHING",
            (user_id, task_id, kind, due_date, message, created_at),
        )

    @staticmethod
    def notification_page(
        connection: Any, user_id: int, unread_only: bool, page: int, page_size: int
    ) -> tuple[int, Any]:
        """Return one caller-scoped local-outbox page and its unchanged total."""
        where = "WHERE n.user_id=?"
        params: list[Any] = [user_id]
        if unread_only:
            where += " AND n.read_at IS NULL"
        total = connection.execute(
            f"SELECT COUNT(*) FROM notification_outbox n {where}", params
        ).fetchone()[0]
        rows = connection.execute(
            "SELECT n.id,n.task_id,n.kind,n.due_date,n.message,n.read_at,n.created_at,t.description,t.status "
            "FROM notification_outbox n JOIN tasks t ON t.id=n.task_id "
            + where
            + " ORDER BY n.read_at IS NOT NULL,n.id DESC LIMIT ? OFFSET ?",
            [*params, page_size, (page - 1) * page_size],
        )
        return total, rows
