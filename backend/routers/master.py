"""HTTP boundary for unchanged request-information master endpoints."""
from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter, Depends

try:
    from services.master_service import MasterService
except ModuleNotFoundError:
    from backend.services.master_service import MasterService


def create_router(
    service: MasterService,
    current_user: Callable[..., Any],
    password_changed_user: Callable[[Any], Any],
) -> APIRouter:
    """Build legacy master-data routes without placing SQL in the HTTP layer."""
    router = APIRouter()

    @router.get("/api/organizations")
    def organizations(q: str = "", user: Any = Depends(current_user)):
        password_changed_user(user)
        return service.organizations(q)

    return router
