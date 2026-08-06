"""HTTP boundary for unchanged task-read endpoints."""
from __future__ import annotations

from datetime import date
from typing import Any, Callable, Literal

from fastapi import APIRouter, Depends, File, Query, Request, UploadFile, status
try:
    from schemas.requests import ImageEditIn, TaskIn, TaskUpdateIn
    from services.task_service import TaskService
except ModuleNotFoundError:
    from backend.schemas.requests import ImageEditIn, TaskIn, TaskUpdateIn
    from backend.services.task_service import TaskService


def create_router(
    service: TaskService,
    current_user: Callable[..., Any],
    password_changed_user: Callable[[Any], Any],
    admin_required: Callable[..., Any],
) -> APIRouter:
    """Build legacy task-read routes without placing SQL in the HTTP layer."""
    router = APIRouter()

    @router.post("/api/tasks", status_code=status.HTTP_201_CREATED)
    def create_task(
        payload: TaskIn,
        request: Request,
        user: Any = Depends(current_user),
    ):
        return service.create_task(
            payload,
            password_changed_user(user),
            request.client.host if request.client else None,
        )

    @router.get("/api/tasks")
    def list_tasks(
        status: Literal["RECEIVED", "IN_PROGRESS", "COMPLETED"] | None = None,
        q: str | None = Query(None, max_length=200),
        received_from: date | None = None,
        received_to: date | None = None,
        due_from: date | None = None,
        due_to: date | None = None,
        assignee_id: int | None = Query(None, gt=0),
        page: int = Query(1, ge=1),
        page_size: int = Query(20, ge=1, le=100),
        user: Any = Depends(current_user),
    ):
        user = password_changed_user(user)
        return service.list_tasks(
            status,
            q,
            received_from,
            received_to,
            due_from,
            due_to,
            assignee_id,
            page,
            page_size,
            user,
        )

    @router.get("/api/tasks/{task_id}")
    def get_task(task_id: int, user: Any = Depends(current_user)):
        return service.get_task(task_id, password_changed_user(user))

    @router.patch("/api/tasks/{task_id}")
    def patch_task(
        task_id: int,
        payload: TaskUpdateIn,
        request: Request,
        user: Any = Depends(current_user),
    ):
        return service.update_task(
            task_id,
            payload,
            password_changed_user(user),
            request.client.host if request.client else None,
        )

    @router.delete("/api/tasks/{task_id}")
    def delete_task(
        task_id: int,
        request: Request,
        user: Any = Depends(admin_required),
    ):
        return service.delete_task(
            task_id,
            user,
            request.client.host if request.client else None,
        )

    @router.post("/api/tasks/{task_id}/images", status_code=status.HTTP_201_CREATED)
    async def upload_task_images(
        task_id: int,
        request: Request,
        images: list[UploadFile] = File(...),
        user: Any = Depends(current_user),
    ):
        return await service.upload_task_images(
            task_id,
            images,
            password_changed_user(user),
            request.client.host if request.client else None,
        )

    @router.get("/api/tasks/{task_id}/history")
    def get_task_history(task_id: int, user: Any = Depends(current_user)):
        return service.get_task_history(task_id, password_changed_user(user))

    @router.get("/api/tasks/{task_id}/images/{image_id}")
    def serve_task_image(task_id: int, image_id: int, user: Any = Depends(current_user)):
        return service.get_task_image(task_id, image_id, password_changed_user(user))

    @router.post("/api/tasks/{task_id}/images/{image_id}/edit")
    def edit_task_image(
        task_id: int,
        image_id: int,
        payload: ImageEditIn,
        request: Request,
        user: Any = Depends(current_user),
    ):
        return service.edit_task_image(
            task_id,
            image_id,
            payload,
            password_changed_user(user),
            request.client.host if request.client else None,
        )

    @router.delete("/api/tasks/{task_id}/images/{image_id}")
    def delete_task_image(
        task_id: int,
        image_id: int,
        request: Request,
        user: Any = Depends(current_user),
    ):
        return service.delete_task_image(
            task_id,
            image_id,
            password_changed_user(user),
            request.client.host if request.client else None,
        )

    @router.get("/api/calendar")
    def calendar(month: str, user: Any = Depends(current_user)):
        return service.get_received_date_calendar(month, password_changed_user(user))

    return router
