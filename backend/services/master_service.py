"""Request-information master lookup operations extracted from the HTTP router."""
from __future__ import annotations

from typing import Any, Callable, ContextManager


class MasterService:
    """Provide unchanged authenticated master-data autocomplete operations."""

    def __init__(
        self,
        db: Callable[[], ContextManager[Any]],
        organization_view: Callable[[Any], dict],
    ) -> None:
        self._db = db
        self._organization_view = organization_view

    def organizations(self, query: str) -> list[dict]:
        """Return the existing active-organization autocomplete response."""
        with self._db() as connection:
            rows = connection.execute(
                "SELECT * FROM organizations WHERE is_active=1 AND name LIKE ? ORDER BY name LIMIT 20",
                (f"%{query.strip()}%",),
            )
            return [self._organization_view(row) for row in rows]
