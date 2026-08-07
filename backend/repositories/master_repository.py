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

    @staticmethod
    def organization_by_name(connection: Any, name: str) -> Any:
        """Return the exact-name organization row, including inactive rows."""
        return connection.execute(
            "SELECT * FROM organizations WHERE name=?", (name,)
        ).fetchone()

    @staticmethod
    def create_organization(connection: Any, name: str, timestamp: str) -> int:
        """Insert an active organization and return its legacy SQLite identifier."""
        return connection.execute(
            "INSERT INTO organizations(name,is_active,created_at,updated_at) VALUES(?,1,?,?)",
            (name, timestamp, timestamp),
        ).lastrowid

    @staticmethod
    def organization_by_id(connection: Any, organization_id: int) -> Any:
        """Return one organization row by its primary key."""
        return connection.execute(
            "SELECT * FROM organizations WHERE id=?", (organization_id,)
        ).fetchone()
