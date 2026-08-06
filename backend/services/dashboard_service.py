"""Dashboard aggregate operations extracted from the HTTP router."""
from __future__ import annotations

import re
from datetime import date
from typing import Any, Callable, ContextManager

from fastapi import HTTPException


class DashboardService:
    """Calculate caller-authorized task aggregates without HTTP concerns."""

    def __init__(
        self,
        db: Callable[[], ContextManager[Any]],
        task_query_sql: Callable[[Any], tuple[str, list]],
        task_view: Callable[[Any, Any], dict],
    ) -> None:
        self._db = db
        self._task_query_sql = task_query_sql
        self._task_view = task_view

    @staticmethod
    def _apply_statistics_filters(
        sql: str,
        params: list,
        user: Any,
        received_from: date | None,
        received_to: date | None,
        assignee_id: int | None,
    ) -> tuple[str, list, int | None]:
        """Apply report scope without weakening the existing task visibility policy."""
        if received_from and received_to and received_from > received_to:
            raise HTTPException(status_code=422, detail="접수일 시작일은 종료일보다 늦을 수 없습니다.")
        if user["role"] != "ADMIN" and assignee_id is not None and assignee_id != user["id"]:
            raise HTTPException(status_code=403, detail="일반 이용자의 처리자 필터는 본인으로 고정됩니다.")
        if received_from:
            sql += " AND t.received_date>=?"
            params.append(str(received_from))
        if received_to:
            sql += " AND t.received_date<=?"
            params.append(str(received_to))
        if assignee_id is not None:
            sql += " AND EXISTS(SELECT 1 FROM task_assignees ta_filter WHERE ta_filter.task_id=t.id AND ta_filter.user_id=?)"
            params.append(assignee_id)
        user_scope = assignee_id if assignee_id is not None else (
            user["id"] if user["role"] != "ADMIN" else None
        )
        return sql, params, user_scope

    def statistics(
        self,
        received_from: date | None,
        received_to: date | None,
        assignee_id: int | None,
        user: Any,
    ) -> dict:
        """Return the unchanged authorized status and processor aggregates."""
        with self._db() as connection:
            sql, params = self._task_query_sql(user)
            sql, params, user_scope = self._apply_statistics_filters(
                sql, params, user, received_from, received_to, assignee_id
            )
            by_status = {name: 0 for name in ("RECEIVED", "IN_PROGRESS", "COMPLETED")}
            for row in connection.execute(
                f"SELECT visible.status,COUNT(*) count FROM ({sql}) visible GROUP BY visible.status",
                params,
            ):
                by_status[row["status"]] = row["count"]
            total = sum(by_status.values())

            user_sql = (
                "SELECT u.id,u.name,u.login_id,u.is_active,COUNT(*) total,"
                "SUM(CASE WHEN visible.status='RECEIVED' THEN 1 ELSE 0 END) RECEIVED,"
                "SUM(CASE WHEN visible.status='IN_PROGRESS' THEN 1 ELSE 0 END) IN_PROGRESS,"
                "SUM(CASE WHEN visible.status='COMPLETED' THEN 1 ELSE 0 END) COMPLETED "
                "FROM task_assignees ta JOIN users u ON u.id=ta.user_id "
                f"JOIN ({sql}) visible ON visible.id=ta.task_id"
            )
            user_params = list(params)
            if user_scope is not None:
                user_sql += " WHERE ta.user_id=?"
                user_params.append(user_scope)
            user_sql += " GROUP BY u.id,u.name,u.login_id,u.is_active ORDER BY total DESC,u.name,u.id"
            by_user = []
            for row in connection.execute(user_sql, user_params):
                item = dict(row)
                item["is_active"] = bool(item["is_active"])
                item["by_status"] = {
                    name: item.pop(name)
                    for name in ("RECEIVED", "IN_PROGRESS", "COMPLETED")
                }
                by_user.append(item)
            return {
                "scope": "ALL_TASKS" if user["role"] == "ADMIN" and assignee_id is None else "MY_AUTHORIZED_TASKS",
                "period": {
                    "received_from": str(received_from) if received_from else None,
                    "received_to": str(received_to) if received_to else None,
                },
                "assignee_id": assignee_id,
                "total": total,
                "by_status": by_status,
                "by_user": by_user,
                "user_totals_note": "공동 처리 업무는 각 처리자에게 1건씩 집계됩니다.",
            }

    def completed_calendar(self, month: str, user: Any) -> list[dict]:
        """Return unchanged authorized completed-task report calendar rows."""
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", month):
            raise HTTPException(status_code=422, detail="month는 유효한 YYYY-MM 형식이어야 합니다.")
        year, month_number = map(int, month.split("-"))
        first_day = date(year, month_number, 1)
        next_month = (
            date(year + 1, 1, 1)
            if month_number == 12
            else date(year, month_number + 1, 1)
        )
        with self._db() as connection:
            sql, params = self._task_query_sql(user)
            sql += (
                " AND t.status='COMPLETED' AND t.completed_date>=? "
                "AND t.completed_date<? ORDER BY t.completed_date,t.id"
            )
            params.extend([str(first_day), str(next_month)])
            return [self._task_view(connection, row) for row in connection.execute(sql, params)]
