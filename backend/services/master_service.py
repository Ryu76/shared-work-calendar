"""Request-information master operations extracted from the HTTP router."""
from __future__ import annotations

from typing import Any, Callable, ContextManager


class MasterService:
    """Provide unchanged authenticated master-data operations."""

    def __init__(
        self,
        db: Callable[[], ContextManager[Any]],
        organization_view: Callable[[Any], dict],
        contact_view: Callable[[Any, Any], dict],
        now: Callable[[], str],
        audit: Callable[..., None],
    ) -> None:
        self._db = db
        self._organization_view = organization_view
        self._contact_view = contact_view
        self._now = now
        self._audit = audit

    def organizations(self, query: str) -> list[dict]:
        """Return the existing active-organization autocomplete response."""
        with self._db() as connection:
            rows = connection.execute(
                "SELECT * FROM organizations WHERE is_active=1 AND name LIKE ? ORDER BY name LIMIT 20",
                (f"%{query.strip()}%",),
            )
            return [self._organization_view(row) for row in rows]

    def create_organization(self, payload: Any, user: Any, ip_address: str | None) -> dict:
        """Create or reuse an organization with the legacy audit behavior."""
        with self._db() as connection:
            existing = connection.execute(
                "SELECT * FROM organizations WHERE name=?", (payload.name,)
            ).fetchone()
            if existing:
                return self._organization_view(existing)
            timestamp = self._now()
            organization_id = connection.execute(
                "INSERT INTO organizations(name,is_active,created_at,updated_at) VALUES(?,1,?,?)",
                (payload.name, timestamp, timestamp),
            ).lastrowid
            row = connection.execute(
                "SELECT * FROM organizations WHERE id=?", (organization_id,)
            ).fetchone()
            result = self._organization_view(row)
            self._audit(
                connection,
                user["id"],
                "ORGANIZATION_CREATED",
                "ORGANIZATION",
                organization_id,
                after=result,
                ip=ip_address,
            )
            return result

    def contacts(self, query: str) -> list[dict]:
        """Return the existing active request-contact autocomplete response."""
        with self._db() as connection:
            rows = connection.execute(
                "SELECT rc.* FROM request_contacts rc JOIN organizations o ON o.id=rc.organization_id "
                "WHERE rc.is_active=1 AND o.is_active=1 AND (rc.name LIKE ? OR o.name LIKE ?) "
                "ORDER BY rc.name, o.name LIMIT 20",
                (f"%{query.strip()}%", f"%{query.strip()}%"),
            )
            return [self._contact_view(connection, row) for row in rows]
