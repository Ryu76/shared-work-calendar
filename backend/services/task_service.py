"""Task-read business operations extracted from the HTTP router.

The service receives existing application helpers explicitly so its initial boundary
move preserves the established SQLCipher transaction, authorization scope, task
view shape, and error responses without importing the ASGI application.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Callable, ContextManager

from fastapi import HTTPException


class TaskService:
    """Handle authorized task listing and detail retrieval."""

    def __init__(
        self,
        db: Callable[[], ContextManager[Any]],
        task_query_sql: Callable[[Any], tuple[str, list]],
        task_view: Callable[[Any, Any], dict],
        accessible_task: Callable[[Any, int, Any], Any],
        contact_from_input: Callable[..., int],
        today_in_seoul: Callable[[], date],
        now: Callable[[], str],
        audit: Callable[..., None],
        task_changes: Callable[[dict, dict], list[str]],
    ) -> None:
        self._db = db
        self._task_query_sql = task_query_sql
        self._task_view = task_view
        self._accessible_task = accessible_task
        self._contact_from_input = contact_from_input
        self._today_in_seoul = today_in_seoul
        self._now = now
        self._audit = audit
        self._task_changes = task_changes

    def create_task(self, payload: Any, user: Any, ip_address: str | None) -> dict:
        """Create a task with the unchanged validation, audit, and response view."""
        received = payload.received_date or self._today_in_seoul()
        due = payload.due_date
        if due is not None and due < received:
            raise HTTPException(status_code=422, detail="마감일은 접수일보다 빠를 수 없습니다.")
        completed = payload.completed_date or (
            self._today_in_seoul() if payload.status == "COMPLETED" else None
        )
        if payload.status != "COMPLETED":
            completed = None
        with self._db() as connection:
            active = {
                row["id"]
                for row in connection.execute("SELECT id FROM users WHERE is_active=1")
            }
            if not set(payload.assignee_ids).issubset(active):
                raise HTTPException(
                    status_code=422,
                    detail="비활성 또는 존재하지 않는 처리자가 포함되어 있습니다.",
                )
            contact_id = self._contact_from_input(
                connection, payload.contact, user["id"], ip_address
            )
            cursor = connection.execute(
                "INSERT INTO tasks(requester_contact_id,status,description,received_date,completed_date,due_date,created_by,created_at,updated_at) "
                "VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    contact_id,
                    payload.status,
                    payload.description.strip(),
                    str(received),
                    str(completed) if completed else None,
                    str(due) if due else None,
                    user["id"],
                    self._now(),
                    self._now(),
                ),
            )
            for assignee_id in payload.assignee_ids:
                connection.execute(
                    "INSERT INTO task_assignees(task_id,user_id,assigned_at) VALUES(?,?,?)",
                    (cursor.lastrowid, assignee_id, self._now()),
                )
            task = connection.execute(
                "SELECT * FROM tasks WHERE id=?", (cursor.lastrowid,)
            ).fetchone()
            result = self._task_view(connection, task)
            self._audit(
                connection,
                user["id"],
                "TASK_CREATED",
                "TASK",
                cursor.lastrowid,
                after=result,
                ip=ip_address,
            )
            return result

    def list_tasks(
        self,
        task_status: str | None,
        query: str | None,
        received_from: date | None,
        received_to: date | None,
        due_from: date | None,
        due_to: date | None,
        assignee_id: int | None,
        page: int,
        page_size: int,
        user: Any,
    ) -> dict:
        """Return the unchanged authorized task page and summary metadata."""
        if received_from and received_to and received_from > received_to:
            raise HTTPException(status_code=422, detail="접수일 시작일은 종료일보다 늦을 수 없습니다.")
        if due_from and due_to and due_from > due_to:
            raise HTTPException(status_code=422, detail="마감일 시작일은 종료일보다 늦을 수 없습니다.")
        if user["role"] != "ADMIN" and assignee_id is not None and assignee_id != user["id"]:
            raise HTTPException(status_code=403, detail="일반 이용자의 처리자 필터는 본인으로 고정됩니다.")
        with self._db() as connection:
            sql, params = self._task_query_sql(user)
            if task_status:
                sql += " AND t.status=?"
                params.append(task_status)
            if received_from:
                sql += " AND t.received_date>=?"
                params.append(str(received_from))
            if received_to:
                sql += " AND t.received_date<=?"
                params.append(str(received_to))
            if due_from:
                sql += " AND t.due_date>=?"
                params.append(str(due_from))
            if due_to:
                sql += " AND t.due_date<=?"
                params.append(str(due_to))
            keyword = (query or "").strip()
            if keyword:
                sql += (
                    " AND (t.description LIKE ? OR EXISTS(SELECT 1 FROM request_contacts rc "
                    "JOIN organizations o ON o.id=rc.organization_id WHERE rc.id=t.requester_contact_id "
                    "AND (rc.name LIKE ? OR o.name LIKE ?)))"
                )
                params += [f"%{keyword}%"] * 3
            if assignee_id is not None:
                sql += " AND EXISTS(SELECT 1 FROM task_assignees ta_filter WHERE ta_filter.task_id=t.id AND ta_filter.user_id=?)"
                params.append(assignee_id)
            total = connection.execute(f"SELECT COUNT(*) FROM ({sql})", params).fetchone()[0]
            summary = {name: 0 for name in ("RECEIVED", "IN_PROGRESS", "COMPLETED")}
            for row in connection.execute(f"SELECT t.status,COUNT(*) count FROM ({sql}) t GROUP BY t.status", params):
                summary[row["status"]] = row["count"]
            rows = connection.execute(
                sql + " ORDER BY CASE t.status WHEN 'RECEIVED' THEN 1 WHEN 'IN_PROGRESS' THEN 2 ELSE 3 END,t.received_date DESC,t.id DESC LIMIT ? OFFSET ?",
                [*params, page_size, (page - 1) * page_size],
            )
            return {
                "items": [self._task_view(connection, row) for row in rows],
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "total_pages": (total + page_size - 1) // page_size,
                },
                "summary": summary,
            }

    def get_task(self, task_id: int, user: Any) -> dict:
        """Return one task only after the existing task-level authorization check."""
        with self._db() as connection:
            return self._task_view(connection, self._accessible_task(connection, task_id, user))

    def update_task(self, task_id: int, payload: Any, user: Any, ip_address: str | None) -> dict:
        """Update a task while preserving the existing authorization and audit rules."""
        with self._db() as connection:
            old = self._accessible_task(connection, task_id, user)
            before = self._task_view(connection, old)
            assignee_ids = (
                payload.assignee_ids
                if payload.assignee_ids is not None
                else [assignee["id"] for assignee in before["assignees"]]
            )
            active = {
                row["id"]
                for row in connection.execute("SELECT id FROM users WHERE is_active=1")
            }
            if not set(assignee_ids).issubset(active):
                raise HTTPException(
                    status_code=422,
                    detail="비활성 또는 존재하지 않는 처리자가 포함되어 있습니다.",
                )
            next_status = payload.status or old["status"]
            stored_received = date.fromisoformat(old["received_date"])
            if (
                payload.received_date is not None
                and payload.received_date != stored_received
                and user["role"] != "ADMIN"
                and old["created_by"] != user["id"]
            ):
                raise HTTPException(
                    status_code=403,
                    detail="접수일은 업무 생성자 또는 관리자만 수정할 수 있습니다.",
                )
            received = payload.received_date or stored_received
            due = (
                payload.due_date
                if "due_date" in payload.model_fields_set
                else date.fromisoformat(old["due_date"]) if old["due_date"] else None
            )
            if due is not None and due < received:
                raise HTTPException(status_code=422, detail="마감일은 접수일보다 빠를 수 없습니다.")
            if next_status != "COMPLETED":
                completed = None
            elif payload.completed_date is not None:
                completed = payload.completed_date
            elif old["status"] == "COMPLETED" and old["completed_date"]:
                completed = date.fromisoformat(old["completed_date"])
            else:
                completed = self._today_in_seoul()
            contact_id = (
                self._contact_from_input(connection, payload.contact, user["id"], ip_address)
                if payload.contact
                else old["requester_contact_id"]
            )
            description = payload.description if payload.description is not None else old["description"]
            connection.execute(
                "UPDATE tasks SET requester_contact_id=?,status=?,description=?,received_date=?,completed_date=?,due_date=?,updated_at=? WHERE id=?",
                (
                    contact_id,
                    next_status,
                    description,
                    str(received),
                    str(completed) if completed else None,
                    str(due) if due else None,
                    self._now(),
                    task_id,
                ),
            )
            notification_needs_refresh = (
                old["due_date"] != (str(due) if due else None)
                or old["status"] != next_status
                or old["description"] != description
                or payload.assignee_ids is not None
            )
            if notification_needs_refresh:
                connection.execute("DELETE FROM notification_outbox WHERE task_id=?", (task_id,))
            if payload.assignee_ids is not None:
                connection.execute("DELETE FROM task_assignees WHERE task_id=?", (task_id,))
                for assignee_id in assignee_ids:
                    connection.execute(
                        "INSERT INTO task_assignees(task_id,user_id,assigned_at) VALUES(?,?,?)",
                        (task_id, assignee_id, self._now()),
                    )
            updated = connection.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
            after = self._task_view(connection, updated)
            if self._task_changes(before, after):
                self._audit(
                    connection,
                    user["id"],
                    "TASK_UPDATED",
                    "TASK",
                    task_id,
                    before,
                    after,
                    ip_address,
                )
            return after
