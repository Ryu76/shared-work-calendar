"""Typed, environment-backed application configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class Settings:
    static_dir: Path
    upload_dir: Path
    log_level: str


def load_settings(base_dir: Path) -> Settings:
    """Load non-secret runtime configuration without changing API contracts."""
    return Settings(
        static_dir=base_dir.parent / "web",
        upload_dir=Path(os.getenv("WORK_CALENDAR_UPLOAD_DIR", base_dir / "private_uploads")),
        log_level=os.getenv("WORK_CALENDAR_LOG_LEVEL", "INFO").upper(),
    )
