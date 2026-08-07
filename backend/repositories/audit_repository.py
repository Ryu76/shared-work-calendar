"""Database access for audit-event persistence."""
from __future__ import annotations

from typing import Any


class AuditRepository:
    """Persist immutable application audit events."""

    @staticmethod
    def create(
        connection: Any,
        actor_user_id: int | None,
        action: str,
        target_type: str,
        target_id: str,
        before_data: str | None,
        after_data: str | None,
        ip_address: str | None,
        created_at: str,
    ) -> None:
        """Insert one audit row without changing the established event payload."""
        connection.execute(
            "INSERT INTO audit_logs(actor_user_id,action,target_type,target_id,before_data,after_data,ip_address,created_at) VALUES(?,?,?,?,?,?,?,?)",
            (
                actor_user_id,
                action,
                target_type,
                target_id,
                before_data,
                after_data,
                ip_address,
                created_at,
            ),
        )