"""HTTP boundary for unchanged private local notification endpoints."""
from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter, Depends, Query, Request

try:
    from schemas.requests import NotificationPreferencesIn
    from services.notification_service import NotificationService
except ModuleNotFoundError:
    from backend.schemas.requests import NotificationPreferencesIn
    from backend.services.notification_service import NotificationService


def create_router(
    service: NotificationService,
    current_user: Callable[..., Any],
    password_changed_user: Callable[[Any], Any],
) -> APIRouter:
    """Build legacy notification routes without placing SQL in the HTTP layer."""
    router = APIRouter()

    @router.get("/api/me/notification-preferences")
    def notification_preferences(user: Any = Depends(current_user)):
        return service.preferences(password_changed_user(user))

    @router.patch("/api/me/notification-preferences")
    def patch_notification_preferences(
        payload: NotificationPreferencesIn,
        request: Request,
        user: Any = Depends(current_user),
    ):
        return service.update_preferences(
            payload,
            password_changed_user(user),
            request.client.host if request.client else None,
        )

    @router.get("/api/notifications")
    def notifications(
        unread_only: bool = False,
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
        user: Any = Depends(current_user),
    ):
        return service.list_notifications(
            unread_only, page, page_size, password_changed_user(user)
        )

    @router.post("/api/notifications/{notification_id}/read")
    def read_notification(notification_id: int, user: Any = Depends(current_user)):
        return service.mark_read(notification_id, password_changed_user(user))

    return router
