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
    ) -> None:
        self._db = db
        self._task_query_sql = task_query_sql
        self._task_view = task_view
        self._accessible_task = accessible_task

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
