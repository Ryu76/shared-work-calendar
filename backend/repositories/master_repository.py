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

    @staticmethod
    def active_contact_rows(connection: Any, query: str) -> Any:
        """Return active contact autocomplete rows with the legacy ordering and limit."""
        return connection.execute(
            "SELECT rc.* FROM request_contacts rc JOIN organizations o ON o.id=rc.organization_id "
            "WHERE rc.is_active=1 AND o.is_active=1 AND (rc.name LIKE ? OR o.name LIKE ?) "
            "ORDER BY rc.name, o.name LIMIT 20",
            (f"%{query.strip()}%", f"%{query.strip()}%"),
        )
