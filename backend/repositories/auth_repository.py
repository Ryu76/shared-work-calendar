"""Database access for authentication records."""
from __future__ import annotations

from typing import Any


class AuthRepository:
    """Perform only the user-row reads and writes needed by authentication."""

    @staticmethod
    def find_by_login_id(connection: Any, login_id: str) -> Any:
        return connection.execute(
            "SELECT * FROM users WHERE login_id=?", (login_id,)
        ).fetchone()

    @staticmethod
    def update_password_hash(connection: Any, user_id: int, password_hash: str, updated_at: str) -> None:
        connection.execute(
            "UPDATE users SET password_hash=?,updated_at=? WHERE id=?",
            (password_hash, updated_at, user_id),
        )
