"""FastAPI application and lifecycle composition boundary."""
from __future__ import annotations

import logging
from collections.abc import Callable
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

try:
    from background.scheduler import LocalNotificationScheduler
    from core.exceptions import unhandled_exception_handler
    from middleware.request_logging import RequestLoggingMiddleware
except ModuleNotFoundError:
    from backend.background.scheduler import LocalNotificationScheduler
    from backend.core.exceptions import unhandled_exception_handler
    from backend.middleware.request_logging import RequestLoggingMiddleware


def create_application(
    *,
    static_dir: Path,
    logger: logging.Logger,
    initialize_database: Callable[[], None],
) -> tuple[FastAPI, LocalNotificationScheduler]:
    """Create the existing HTTP application with its middleware and lifecycle hooks."""
    app = FastAPI(title="Shared Work Calendar MVP", version="1.0.0")
    scheduler = LocalNotificationScheduler()

    async def global_exception_handler(request: Request, error: Exception):
        return await unhandled_exception_handler(request, error, logger)

    app.add_middleware(RequestLoggingMiddleware, logger=logger)
    app.add_exception_handler(Exception, global_exception_handler)
    app.mount("/assets", StaticFiles(directory=static_dir), name="assets")

    @app.on_event("startup")
    def startup() -> None:
        initialize_database()
        scheduler.start()

    @app.on_event("shutdown")
    def shutdown() -> None:
        scheduler.stop()

    return app, scheduler
