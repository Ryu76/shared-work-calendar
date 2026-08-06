"""HTTP boundary for unchanged dashboard aggregate endpoints."""
from __future__ import annotations

from datetime import date
from typing import Any, Callable, Literal

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import Response

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

    @router.get("/api/tasks/export.xlsx")
    def export_tasks_xlsx(
        request: Request,
        status: Literal["RECEIVED", "IN_PROGRESS", "COMPLETED"] | None = None,
        q: str | None = Query(None, max_length=200),
        received_from: date | None = None,
        received_to: date | None = None,
        due_from: date | None = None,
        due_to: date | None = None,
        assignee_id: int | None = Query(None, gt=0),
        user: Any = Depends(current_user),
    ):
        document = service.export_tasks_xlsx(
            status,
            q,
            received_from,
            received_to,
            due_from,
            due_to,
            assignee_id,
            password_changed_user(user),
            request.client.host if request.client else None,
        )
        return Response(
            content=document,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": "attachment; filename=shared-work-calendar-tasks.xlsx",
                "Cache-Control": "private, no-store",
                "X-Content-Type-Options": "nosniff",
            },
        )

    return router
