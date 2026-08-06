"""HTTP boundary for unchanged user-account endpoints."""
from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter, Depends, Request

try:
    from schemas.requests import PasswordChangeIn, UserIn, UserPatch
    from services.user_service import UserService
except ModuleNotFoundError:
    from backend.schemas.requests import PasswordChangeIn, UserIn, UserPatch
    from backend.services.user_service import UserService


def create_router(
    service: UserService,
    current_user: Callable[..., Any],
    admin_required: Callable[..., Any],
    password_changed_user: Callable[[Any], Any],
) -> APIRouter:
    """Build legacy user routes without placing SQL in the HTTP layer."""
    router = APIRouter()

    @router.get("/api/assignees")
    def assignees(user: Any = Depends(current_user)):
        password_changed_user(user)
        return service.assignees()

    @router.post("/api/me/password")
    def change_my_password(
        payload: PasswordChangeIn,
        request: Request,
        user: Any = Depends(current_user),
    ):
        return service.change_password(payload, user, request.client.host if request.client else None)

    @router.get("/api/admin/users")
    def users(_: Any = Depends(admin_required)):
        return service.list_users()

    @router.post("/api/admin/users", status_code=201)
    def create_user(
        payload: UserIn,
        request: Request,
        user: Any = Depends(admin_required),
    ):
        return service.create_user(payload, user, request.client.host if request.client else None)

    @router.patch("/api/admin/users/{user_id}")
    def patch_user(
        user_id: int,
        payload: UserPatch,
        request: Request,
        actor: Any = Depends(admin_required),
    ):
        return service.patch_user(user_id, payload, actor, request.client.host if request.client else None)

    return router
