"""Authentication business operations extracted from the HTTP router.

The service receives the existing application dependencies explicitly so its move
preserves current session lifetime, audit history, password migration, and
SQLCipher transaction behavior without importing the ASGI application.
"""
from __future__ import annotations

import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, ContextManager, MutableMapping


class AuthService:
    """Handle login, logout, and current-user response construction."""

    def __init__(
        self,
        db: Callable[[], ContextManager[Any]],
        verify_password: Callable[[str, str], bool],
        password_hash_needs_upgrade: Callable[[str], bool],
        hash_password: Callable[[str], str],
        now: Callable[[], str],
        sessions: MutableMapping[str, tuple[int, datetime]],
        audit: Callable[..., None],
    ) -> None:
        self._db = db
        self._verify_password = verify_password
        self._password_hash_needs_upgrade = password_hash_needs_upgrade
        self._hash_password = hash_password
        self._now = now
        self._sessions = sessions
        self._audit = audit

    def login(self, payload: Any, ip_address: str | None) -> dict:
        """Authenticate an account and retain the established eight-hour session."""
        with self._db() as connection:
            user = connection.execute(
                "SELECT * FROM users WHERE login_id=?", (payload.login_id,)
            ).fetchone()
            if not user or not user["is_active"] or not self._verify_password(
                payload.password, user["password_hash"]
            ):
                self._audit(
                    connection,
                    user["id"] if user else None,
                    "LOGIN_FAILED",
                    "USER",
                    user["id"] if user else payload.login_id,
                    ip=ip_address,
                )
                from fastapi import HTTPException

                raise HTTPException(status_code=401, detail="아이디 또는 비밀번호를 확인하세요.")
            if self._password_hash_needs_upgrade(user["password_hash"]):
                connection.execute(
                    "UPDATE users SET password_hash=?,updated_at=? WHERE id=?",
                    (self._hash_password(payload.password), self._now(), user["id"]),
                )
                self._audit(
                    connection,
                    user["id"],
                    "PASSWORD_HASH_UPGRADED",
                    "USER",
                    user["id"],
                    after={"algorithm": "Argon2id"},
                    ip=ip_address,
                )
            token = secrets.token_urlsafe(32)
            self._sessions[token] = (
                user["id"],
                datetime.now(timezone.utc) + timedelta(hours=8),
            )
            self._audit(
                connection, user["id"], "LOGIN_SUCCESS", "USER", user["id"], ip=ip_address
            )
            return {"token": token, "user": self.user_view(user)}

    def logout(self, token: str) -> dict:
        self._sessions.pop(token, None)
        return {"ok": True}

    @staticmethod
    def user_view(user: Any) -> dict:
        return {
            "id": user["id"],
            "login_id": user["login_id"],
            "name": user["name"],
            "role": user["role"],
            "must_change_password": bool(user["must_change_password"]),
        }
