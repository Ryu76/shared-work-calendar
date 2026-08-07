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
        self._repository.clear_disabled_due_kinds(
            connection,
            user["id"],
            preferences["due_soon_enabled"],
            preferences["overdue_enabled"],
        )
        task_sql, params = self._task_query_sql(user)
        today = self._today_in_seoul()
        for task in self._repository.due_task_rows(connection, task_sql, params):
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
                self._repository.add_due_notification(
                    connection, user["id"], task["id"], kind, str(due), message, self._now()
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
            total, rows = self._repository.notification_page(
                connection, user["id"], unread_only, page, page_size
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
