"""Metadata-only request logging middleware."""
from __future__ import annotations

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log method, path, status, and duration without request bodies or credentials."""

    def __init__(self, app, logger: logging.Logger) -> None:
        super().__init__(app)
        self._logger = logger

    async def dispatch(self, request: Request, call_next) -> Response:
        started = time.perf_counter()
        response = await call_next(request)
        self._logger.info(
            "request method=%s path=%s status=%s duration_ms=%d",
            request.method, request.url.path, response.status_code,
            (time.perf_counter() - started) * 1000,
        )
        return response
