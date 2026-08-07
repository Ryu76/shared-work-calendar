"""Global exception boundary for unexpected application failures."""
from __future__ import annotations

import logging

from fastapi import Request
from starlette.responses import Response

try:
    from utils.responses import error_response
except ModuleNotFoundError:
    from backend.utils.responses import error_response


async def unhandled_exception_handler(
    request: Request, error: Exception, logger: logging.Logger
) -> Response:
    """Log unexpected failures and keep the established ``detail`` error contract."""
    logger.exception("unhandled request error method=%s path=%s", request.method, request.url.path)
    return error_response(500, "서버 오류가 발생했습니다.")
