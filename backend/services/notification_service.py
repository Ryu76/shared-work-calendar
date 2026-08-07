"""Private local in-app notification operations extracted from the HTTP router."""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any, Callable, ContextManager

from fastapi import HTTPException

try:
    from repositories.notification_repository import NotificationRepository
except ModuleNotFoundError:
    from backend.repositories.notification_repository import NotificationRepository


class NotificationService:
    """Manage a user's due-date preferences and private local outbox."""

    def __init__(
        self,
        db: Callable[[], ContextManager[Any]],
        task_query_sql: Callable[[Any], tuple[str, list]],
        now: Callable[[], str],
        today_in_seoul: Callable[[], date],
        audit: Callable[..., None],
        repository: NotificationRepository,
    ) -> None:
        self._db = db
        self._task_query_sql = task_query_sql
        self._now = now
        self._today_in_seoul = today_in_seoul
        self._audit = audit
        self._repository = repository

    def _preferences(self, connection: Any, user_id: int) -> dict:
        """Return and lazily create the unchanged local-only preference record."""
        row = self._repository.preference(connection, user_id, self._now())
        return {
            "due_soon_enabled": bool(row["due_soon_enabled"]),
            "overdue_enabled": bool(row["overdue_enabled"]),
            "updated_at": row["updated_at"],
            "delivery": "IN_APP_OUTBOX_ONLY",
        }

    def _refresh_due_notifications(self, connection: Any, user: Any) -> None:
        """Populate only the caller's local outbox; no external delivery is invoked."""
        preferences = self._preferences(connection, user["id"])
        if not preferences["due_soon_enabled"]:
            connection.execute(
                "DELETE FROM notification_outbox WHERE user_id=? AND kind IN ('DUE_SOON','DUE_TODAY')",
                (user["id"],),
            )
        if not preferences["overdue_enabled"]:
            connection.execute(
                "DELETE FROM notification_outbox WHERE user_id=? AND kind='OVERDUE'",
                (user["id"],),
            )
        task_sql, params = self._task_query_sql(user)
        task_sql += " AND t.status!='COMPLETED' AND t.due_date IS NOT NULL"
        today = self._today_in_seoul()
        for task in connection.execute(task_sql, params):
            due = date.fromisoformat(task["due_date"])
            if due < today:
                kind = "OVERDUE"
                enabled = preferences["overdue_enabled"]
                message = f"마감일이 지났습니다: {task['description'][:80]}"
            elif due == today:
                kind = "DUE_TODAY"
                enabled = preferences["due_soon_enabled"]
                message = f"오늘 마감: {task['description'][:80]}"
            elif due <= today + timedelta(days=3):
                kind = "DUE_SOON"
                enabled = preferences["due_soon_enabled"]
                message = f"마감 임박 ({due.isoformat()}): {task['description'][:80]}"
            else:
                continue
            if enabled:
                connection.execute(
                    "INSERT INTO notification_outbox(user_id,task_id,kind,due_date,message,created_at) "
                    "VALUES(?,?,?,?,?,?) ON CONFLICT(user_id,task_id,kind,due_date) DO NOTHING",
                    (user["id"], task["id"], kind, str(due), message, self._now()),
                )

    def preferences(self, user: Any) -> dict:
        with self._db() as connection:
            return self._preferences(connection, user["id"])

    def update_preferences(self, payload: Any, user: Any, ip_address: str | None) -> dict:
        with self._db() as connection:
            before = self._preferences(connection, user["id"])
            self._repository.update_preferences(
                connection,
                user["id"],
                payload.due_soon_enabled,
                payload.overdue_enabled,
                self._now(),
            )
            after = self._preferences(connection, user["id"])
            if before != after:
                self._audit(
                    connection,
                    user["id"],
                    "NOTIFICATION_PREFERENCES_UPDATED",
                    "USER",
                    user["id"],
                    before,
                    after,
                    ip_address,
                )
            return after

    def list_notifications(self, unread_only: bool, page: int, page_size: int, user: Any) -> dict:
        """Return only the caller's private local due-date outbox entries."""
        with self._db() as connection:
            self._refresh_due_notifications(connection, user)
            where = "WHERE n.user_id=?"
            params: list[int] = [user["id"]]
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
            return {
                "items": [dict(row) | {"is_read": row["read_at"] is not None} for row in rows],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "total_pages": (total + page_size - 1) // page_size,
                },
                "delivery": "IN_APP_OUTBOX_ONLY",
            }

    def mark_read(self, notification_id: int, user: Any) -> dict:
        with self._db() as connection:
            updated = self._repository.mark_read(
                connection, notification_id, user["id"], self._now()
            )
            if not updated:
                raise HTTPException(status_code=404, detail="알림을 찾을 수 없습니다.")
            return {"ok": True}
