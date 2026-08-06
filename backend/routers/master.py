"""HTTP boundary for unchanged request-information master endpoints."""
from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter, Depends, Request, status

try:
    from schemas.requests import OrganizationIn
    from services.master_service import MasterService
except ModuleNotFoundError:
    from backend.schemas.requests import OrganizationIn
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

    @router.post("/api/organizations", status_code=status.HTTP_201_CREATED)
    def create_organization(
        payload: OrganizationIn,
        request: Request,
        user: Any = Depends(current_user),
    ):
        return service.create_organization(
            payload,
            password_changed_user(user),
            request.client.host if request.client else None,
        )

    return router
