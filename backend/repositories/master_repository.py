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
    def admin_organization_rows(connection: Any, query: str) -> Any:
        """Return administrator organization rows with the legacy ordering and limit."""
        return connection.execute(
            "SELECT * FROM organizations WHERE name LIKE ? "
            "ORDER BY is_active DESC,name LIMIT 100",
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

    @staticmethod
    def contact_by_identity(
        connection: Any, name: str, phone: str, organization_id: int
    ) -> Any:
        """Return the exact reusable request-contact row, including inactive rows."""
        return connection.execute(
            "SELECT * FROM request_contacts WHERE name=? AND phone=? AND organization_id=?",
            (name, phone, organization_id),
        ).fetchone()

    @staticmethod
    def create_contact(
        connection: Any, name: str, phone: str, organization_id: int, timestamp: str
    ) -> int:
        """Insert an active request contact and return its legacy SQLite identifier."""
        return connection.execute(
            "INSERT INTO request_contacts(name,phone,organization_id,is_active,created_at,updated_at) "
            "VALUES(?,?,?,1,?,?)",
            (name, phone, organization_id, timestamp, timestamp),
        ).lastrowid

    @staticmethod
    def contact_by_id(connection: Any, contact_id: int) -> Any:
        """Return one request-contact row by its primary key."""
        return connection.execute(
            "SELECT * FROM request_contacts WHERE id=?", (contact_id,)
        ).fetchone()

    @staticmethod
    def contact_organization_name(connection: Any, organization_id: int) -> str:
        """Return the organization name used by the legacy contact response."""
        return connection.execute(
            "SELECT name FROM organizations WHERE id=?", (organization_id,)
        ).fetchone()["name"]

    @staticmethod
    def update_organization(
        connection: Any, organization_id: int, name: str, is_active: int, updated_at: str
    ) -> Any:
        """Persist and return one organization management update."""
        connection.execute(
            "UPDATE organizations SET name=?,is_active=?,updated_at=? WHERE id=?",
            (name, is_active, updated_at, organization_id),
        )
        return MasterRepository.organization_by_id(connection, organization_id)

    @staticmethod
    def organization_name_conflict(connection: Any, name: str, organization_id: int) -> bool:
        """Report whether a different organization already uses the requested name."""
        return bool(connection.execute(
            "SELECT id FROM organizations WHERE name=? AND id!=?", (name, organization_id)
        ).fetchone())

    @staticmethod
    def admin_contact_rows(connection: Any, query: str) -> Any:
        """Return administrator contact rows with the legacy ordering and limit."""
        return connection.execute(
            "SELECT rc.* FROM request_contacts rc JOIN organizations o ON o.id=rc.organization_id "
            "WHERE rc.name LIKE ? OR rc.phone LIKE ? OR o.name LIKE ? "
            "ORDER BY rc.is_active DESC,rc.name,o.name LIMIT 100",
            (f"%{query.strip()}%",) * 3,
        )

    @staticmethod
    def organization_exists(connection: Any, organization_id: int) -> bool:
        """Report whether the requested organization exists."""
        return bool(connection.execute(
            "SELECT 1 FROM organizations WHERE id=?", (organization_id,)
        ).fetchone())

    @staticmethod
    def contact_identity_conflict(
        connection: Any, name: str, phone: str, organization_id: int, contact_id: int
    ) -> bool:
        """Report whether another request contact has the same identity."""
        return bool(connection.execute(
            "SELECT id FROM request_contacts WHERE name=? AND phone=? AND organization_id=? AND id!=?",
            (name, phone, organization_id, contact_id),
        ).fetchone())

    @staticmethod
    def update_contact(
        connection: Any,
        contact_id: int,
        name: str,
        phone: str,
        organization_id: int,
        is_active: int,
        updated_at: str,
    ) -> Any:
        """Persist and return one request-contact management update."""
        connection.execute(
            "UPDATE request_contacts SET name=?,phone=?,organization_id=?,is_active=?,updated_at=? WHERE id=?",
            (name, phone, organization_id, is_active, updated_at, contact_id),
        )
        return MasterRepository.contact_by_id(connection, contact_id)

    @staticmethod
    def audit_log_rows(
        connection: Any,
        action: str | None,
        actor_user_id: int | None,
        created_from: str | None,
        created_to_exclusive: str | None,
    ) -> Any:
        """Return the legacy filtered administrator audit trail."""
        sql = "SELECT a.*,u.name actor_name FROM audit_logs a LEFT JOIN users u ON u.id=a.actor_user_id WHERE 1=1"
        params: list[str | int] = []
        if action:
            sql += " AND a.action=?"
            params.append(action)
        if actor_user_id is not None:
            sql += " AND a.actor_user_id=?"
            params.append(actor_user_id)
        if created_from:
            sql += " AND a.created_at>=?"
            params.append(created_from)
        if created_to_exclusive:
            sql += " AND a.created_at<?"
            params.append(created_to_exclusive)
        return connection.execute(sql + " ORDER BY a.id DESC LIMIT 100", params)
