"""Database access for user-account records."""
from __future__ import annotations

from typing import Any


class UserRepository:
    """Perform only persistence operations for user-account records."""

    @staticmethod
    def active_assignees(connection: Any) -> list[Any]:
        return list(
            connection.execute(
                "SELECT id,name,login_id,role FROM users WHERE is_active=1 ORDER BY name,login_id"
            )
        )

    @staticmethod
    def list_users(connection: Any) -> list[Any]:
        return list(
            connection.execute(
                "SELECT id,login_id,name,role,is_active,must_change_password,created_at,updated_at "
                "FROM users ORDER BY is_active DESC,name"
            )
        )

    @staticmethod
    def find_active_by_id(connection: Any, user_id: int) -> Any:
        return connection.execute(
            "SELECT * FROM users WHERE id=? AND is_active=1", (user_id,)
        ).fetchone()

    @staticmethod
    def find_by_id(connection: Any, user_id: int) -> Any:
        return connection.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()

    @staticmethod
    def active_admin_count(connection: Any) -> int:
        return connection.execute(
            "SELECT COUNT(*) FROM users WHERE role='ADMIN' AND is_active=1"
        ).fetchone()[0]

    @staticmethod
    def update_password(
        connection: Any, password_hash: str, updated_at: str, user_id: int
    ) -> None:
        connection.execute(
            "UPDATE users SET password_hash=?,must_change_password=0,updated_at=? WHERE id=?",
            (password_hash, updated_at, user_id),
        )

    @staticmethod
    def create_user(
        connection: Any,
        login_id: str,
        password_hash: str,
        name: str,
        role: str,
        created_at: str,
        updated_at: str,
    ) -> Any:
        return connection.execute(
            "INSERT INTO users(login_id,password_hash,name,role,is_active,must_change_password,created_at,updated_at) "
            "VALUES(?,?,?,?,1,1,?,?)",
            (login_id, password_hash, name, role, created_at, updated_at),
        )

    @staticmethod
    def update_user(
        connection: Any,
        name: str,
        role: str,
        is_active: int,
        password_hash: str | None,
        password: str | None,
        updated_at: str,
        user_id: int,
    ) -> None:
        connection.execute(
            "UPDATE users SET name=?,role=?,is_active=?,password_hash=COALESCE(?,password_hash),"
            "must_change_password=CASE WHEN ? IS NULL THEN must_change_password ELSE 1 END,updated_at=? "
            "WHERE id=?",
            (name, role, is_active, password_hash, password, updated_at, user_id),
        )
