"""Response construction helpers that preserve the established error schema."""
from __future__ import annotations

from typing import Any

from fastapi.responses import JSONResponse


def error_response(status_code: int, detail: Any) -> JSONResponse:
    """Return the product's existing FastAPI-compatible ``detail`` error body."""
    return JSONResponse(status_code=status_code, content={"detail": detail})
