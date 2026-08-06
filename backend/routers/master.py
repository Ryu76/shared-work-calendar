"""HTTP boundary for unchanged request-information master endpoints."""
from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter, Depends, Request, status

try:
    from schemas.requests import ContactIn, ContactPatch, OrganizationIn, OrganizationPatch
    from services.master_service import MasterService
except ModuleNotFoundError:
    from backend.schemas.requests import ContactIn, ContactPatch, OrganizationIn, OrganizationPatch
    from backend.services.master_service import MasterService


def create_router(
    service: MasterService,
    current_user: Callable[..., Any],
    password_changed_user: Callable[[Any], Any],
    admin_required: Callable[..., Any],
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

    @router.get("/api/request-contacts")
    def contacts(q: str = "", user: Any = Depends(current_user)):
        password_changed_user(user)
        return service.contacts(q)

    @router.post("/api/request-contacts", status_code=status.HTTP_201_CREATED)
    def create_contact(
        payload: ContactIn,
        request: Request,
        user: Any = Depends(current_user),
    ):
        return service.create_contact(
            payload,
            password_changed_user(user),
            request.client.host if request.client else None,
        )

    @router.get("/api/admin/organizations")
    def admin_organizations(q: str = "", _: Any = Depends(admin_required)):
        return service.admin_organizations(q)

    @router.patch("/api/admin/organizations/{organization_id}")
    def patch_organization(
        organization_id: int,
        payload: OrganizationPatch,
        request: Request,
        user: Any = Depends(admin_required),
    ):
        return service.patch_organization(
            organization_id,
            payload,
            user,
            request.client.host if request.client else None,
        )

    @router.get("/api/admin/request-contacts")
    def admin_contacts(q: str = "", _: Any = Depends(admin_required)):
        return service.admin_contacts(q)

    @router.patch("/api/admin/request-contacts/{contact_id}")
    def patch_contact(
        contact_id: int,
        payload: ContactPatch,
        request: Request,
        user: Any = Depends(admin_required),
    ):
        return service.patch_contact(
            contact_id,
            payload,
            user,
            request.client.host if request.client else None,
        )

    return router
