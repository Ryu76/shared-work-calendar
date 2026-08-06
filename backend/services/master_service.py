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

    def contact_from_input(
        self,
        connection: Any,
        payload: Any,
        actor_id: int | None = None,
        ip_address: str | None = None,
    ) -> int:
        """Find or create reusable master records with the legacy audit behavior."""
        organization = connection.execute(
            "SELECT * FROM organizations WHERE name=?", (payload.organization,)
        ).fetchone()
        if not organization:
            timestamp = self._now()
            organization_id = connection.execute(
                "INSERT INTO organizations(name,is_active,created_at,updated_at) VALUES(?,1,?,?)",
                (payload.organization, timestamp, timestamp),
            ).lastrowid
            self._audit(
                connection,
                actor_id,
                "ORGANIZATION_CREATED",
                "ORGANIZATION",
                organization_id,
                after={"name": payload.organization, "is_active": True},
                ip=ip_address,
            )
        else:
            organization_id = organization["id"]
        contact = connection.execute(
            "SELECT * FROM request_contacts WHERE name=? AND phone=? AND organization_id=?",
            (payload.name, payload.phone, organization_id),
        ).fetchone()
        if contact:
            return contact["id"]
        timestamp = self._now()
        contact_id = connection.execute(
            "INSERT INTO request_contacts(name,phone,organization_id,is_active,created_at,updated_at) "
            "VALUES(?,?,?,1,?,?)",
            (payload.name, payload.phone, organization_id, timestamp, timestamp),
        ).lastrowid
        self._audit(
            connection,
            actor_id,
            "REQUEST_CONTACT_CREATED",
            "REQUEST_CONTACT",
            contact_id,
            after={
                "name": payload.name,
                "phone": payload.phone,
                "organization_id": organization_id,
                "is_active": True,
            },
            ip=ip_address,
        )
        return contact_id

    def create_contact(self, payload: Any, user: Any, ip_address: str | None) -> dict:
        """Create or reuse a request contact with the existing response projection."""
        with self._db() as connection:
            contact_id = self.contact_from_input(
                connection, payload, user["id"], ip_address
            )
            contact = connection.execute(
                "SELECT * FROM request_contacts WHERE id=?", (contact_id,)
            ).fetchone()
            return self._contact_view(connection, contact)

    def admin_organizations(self, query: str) -> list[dict]:
        """Return the existing administrator organization-management list."""
        with self._db() as connection:
            rows = connection.execute(
                "SELECT * FROM organizations WHERE name LIKE ? "
                "ORDER BY is_active DESC,name LIMIT 100",
                (f"%{query.strip()}%",),
            )
            return [self._organization_view(row) for row in rows]
