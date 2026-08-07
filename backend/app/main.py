"""Minimal ASGI composition entrypoint preserving the public application target."""
from __future__ import annotations

import sys

try:
    from app import bootstrap as _application
except ModuleNotFoundError:
    from backend.app import bootstrap as _application

sys.modules[__name__] = _application
