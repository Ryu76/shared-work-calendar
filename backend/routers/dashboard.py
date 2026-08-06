"""HTTP boundary for unchanged dashboard aggregate endpoints."""
from __future__ import annotations

from datetime import date
from typing import Any, Callable

from fastapi import APIRouter, Depends, Query

try:
    from services.dashboard_service import DashboardService
except ModuleNotFoundError:
    from backend.services.dashboard_service import DashboardService


def create_router(
    service: DashboardService,
    current_user: Callable[..., Any],
    password_changed_user: Callable[[Any], Any],
) -> APIRouter:
    """Build legacy dashboard routes without placing SQL in the HTTP layer."""
    router = APIRouter()

    @router.get("/api/statistics")
    def statistics(
        received_from: date | None = None,
        received_to: date | None = None,
        assignee_id: int | None = Query(None, gt=0),
        user: Any = Depends(current_user),
    ):
        return service.statistics(
            received_from,
            received_to,
            assignee_id,
            password_changed_user(user),
        )

    @router.get("/api/completed-calendar")
    def completed_calendar(month: str, user: Any = Depends(current_user)):
        return service.completed_calendar(month, password_changed_user(user))

    return router
