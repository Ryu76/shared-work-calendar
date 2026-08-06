"""Backward-compatible ASGI entrypoint.

The implementation lives in :mod:`app.main`; replacing this module in the import
cache preserves existing ``import main`` callers (including runtime overrides used
by isolated tests) without changing the public ASGI target, URLs, or API schema.
"""
from __future__ import annotations

import sys

try:  # ``uvicorn main:app`` from backend/
    from app import main as _api
except ModuleNotFoundError:  # ``uvicorn backend.main:app`` from repository root
    from backend.app import main as _api

sys.modules[__name__] = _api
