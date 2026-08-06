"""User-account business operations extracted from the HTTP router.

The service receives existing application dependencies explicitly to preserve
password handling, session invalidation, audit history, and SQLCipher
transaction behavior without importing the ASGI application.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Callable, ContextManager, MutableMapping

from fastapi import HTTPException

try:
    from repositories.user_repository import UserRepository
except ModuleNotFoundError:
    from backend.repositories.user_repository import UserRepository


class UserService:
    """Handle user selection, password changes, and administrator user lifecycle."""

    def __init__(
        self,
        db: Callable[[], ContextManager[Any]],
        verify_password: Callable[[str, str], bool],
        hash_password: Callable[[str], str],
        now: Callable[[], str],
        sessions: MutableMapping[str, tuple[int, datetime]],
        audit: Callable[..., None],
        integrity_error: type[Exception],
        repository: UserRepository,
    ) -> None:
        self._db = db
        self._verify_password = verify_password
        self._hash_password = hash_password
        self._now = now
        self._sessions = sessions
        self._audit = audit
        self._integrity_error = integrity_error
        self._repository = repository

    def assignees(self) -> list[dict]:
        """Return the unchanged active-user task-assignee selection response."""
        with self._db() as connection:
            return [dict(row) for row in self._repository.active_assignees(connection)]

    def change_password(self, payload: Any, user: Any, ip_address: str | None) -> dict:
        if not self._verify_password(payload.current_password, user["password_hash"]):
            raise HTTPException(status_code=400, detail="현재 비밀번호를 확인하세요.")
        if payload.current_password == payload.new_password:
            raise HTTPException(status_code=422, detail="새 비밀번호는 현재 비밀번호와 달라야 합니다.")
        with self._db() as connection:
            connection.execute(
                "UPDATE users SET password_hash=?,must_change_password=0,updated_at=? WHERE id=?",
                (self._hash_password(payload.new_password), self._now(), user["id"]),
            )
            self._audit(
                connection,
                user["id"],
                "PASSWORD_CHANGED",
                "USER",
                user["id"],
                after={"must_change_password": False},
                ip=ip_address,
            )
        return {"ok": True, "must_change_password": False}

    def list_users(self) -> list[dict]:
        with self._db() as connection:
            return [
                dict(row)
                | {
                    "is_active": bool(row["is_active"]),
                    "must_change_password": bool(row["must_change_password"]),
                }
                for row in connection.execute(
                    "SELECT id,login_id,name,role,is_active,must_change_password,created_at,updated_at "
                    "FROM users ORDER BY is_active DESC,name"
                )
            ]

    def create_user(self, payload: Any, actor: Any, ip_address: str | None) -> dict:
        with self._db() as connection:
            try:
                cursor = connection.execute(
                    "INSERT INTO users(login_id,password_hash,name,role,is_active,must_change_password,created_at,updated_at) "
                    "VALUES(?,?,?,?,1,1,?,?)",
                    (
                        payload.login_id,
                        self._hash_password(payload.temporary_password),
                        payload.name,
                        payload.role,
                        self._now(),
                        self._now(),
                    ),
                )
            except self._integrity_error:
                raise HTTPException(status_code=409, detail="이미 사용 중인 로그인 ID입니다.")
            result = {
                "id": cursor.lastrowid,
                "login_id": payload.login_id,
                "name": payload.name,
                "role": payload.role,
            }
            self._audit(
                connection,
                actor["id"],
                "USER_CREATED",
                "USER",
                cursor.lastrowid,
                after=result,
                ip=ip_address,
            )
            return result

    def patch_user(self, user_id: int, payload: Any, actor: Any, ip_address: str | None) -> dict:
        with self._db() as connection:
            target = connection.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
            if not target:
                raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")
            new_role = payload.role or target["role"]
            new_active = int(target["is_active"] if payload.is_active is None else payload.is_active)
            if target["role"] == "ADMIN" and target["is_active"] and (new_role != "ADMIN" or not new_active):
                active_admins = connection.execute(
                    "SELECT COUNT(*) FROM users WHERE role='ADMIN' AND is_active=1"
                ).fetchone()[0]
                if active_admins <= 1:
                    raise HTTPException(status_code=409, detail="마지막 활성 관리자 계정은 변경하거나 비활성화할 수 없습니다.")
            before = {
                "name": target["name"],
                "role": target["role"],
                "is_active": bool(target["is_active"]),
            }
            connection.execute(
                "UPDATE users SET name=?,role=?,is_active=?,password_hash=COALESCE(?,password_hash),"
                "must_change_password=CASE WHEN ? IS NULL THEN must_change_password ELSE 1 END,updated_at=? "
                "WHERE id=?",
                (
                    payload.name or target["name"],
                    new_role,
                    new_active,
                    self._hash_password(payload.password) if payload.password else None,
                    payload.password,
                    self._now(),
                    user_id,
                ),
            )
            if payload.password or payload.role is not None or payload.is_active is not None:
                for token, session in list(self._sessions.items()):
                    if session[0] == user_id:
                        self._sessions.pop(token, None)
            after = {
                "name": payload.name or target["name"],
                "role": new_role,
                "is_active": bool(new_active),
            }
            self._audit(connection, actor["id"], "USER_UPDATED", "USER", user_id, before, after, ip_address)
            return after | {"id": user_id}
