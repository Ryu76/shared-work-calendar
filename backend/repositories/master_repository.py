"""Database access for request-information master persistence."""
from __future__ import annotations

from typing import Any


class MasterRepository:
    """Perform only request-information master persistence operations."""

    @staticmethod
    def active_organization_rows(connection: Any, query: str) -> Any:
        """Return active autocomplete rows with the legacy name ordering and limit."""
        return connection.execute(
            "SELECT * FROM organizations WHERE is_active=1 AND name LIKE ? ORDER BY name LIMIT 20",
            (f"%{query.strip()}%",),
        )
