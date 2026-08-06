"""HTTP boundary for the unchanged authentication endpoints."""
from __future__ import annotations

from typing import Any, Callable

from fastapi import APIRouter, Depends, Request

try:
    from schemas.requests import LoginIn
    from services.auth_service import AuthService
except ModuleNotFoundError:
    from backend.schemas.requests import LoginIn
    from backend.services.auth_service import AuthService


def create_router(
    service: AuthService, current_user: Callable[..., Any]
) -> APIRouter:
    """Build the legacy auth routes without placing SQL in the HTTP layer."""
    router = APIRouter()

    @router.post("/api/auth/login")
    def login(payload: LoginIn, request: Request):
        return service.login(payload, request.client.host if request.client else None)

    @router.post("/api/auth/logout")
    def logout(request: Request, _: Any = Depends(current_user)):
        token = request.headers.get("Authorization", "").removeprefix("Bearer ").strip()
        return service.logout(token)

    @router.get("/api/me")
    def me(user: Any = Depends(current_user)):
        return service.user_view(user)

    return router
