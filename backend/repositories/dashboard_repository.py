"""Database access for dashboard aggregate persistence operations."""
from __future__ import annotations

from datetime import date
from typing import Any


class DashboardRepository:
    """Perform only dashboard aggregate persistence queries."""

    @staticmethod
    def statistics_rows(
        connection: Any,
        user: Any,
        received_from: date | None,
        received_to: date | None,
        assignee_id: int | None,
        user_scope: int | None,
    ) -> tuple[list[Any], list[Any]]:
        """Return authorized status and assignee aggregate rows with legacy ordering."""
        sql = "SELECT t.* FROM tasks t WHERE t.deleted_at IS NULL"
        params: list[Any] = []
        if user["role"] != "ADMIN":
            sql += " AND (t.created_by=? OR EXISTS(SELECT 1 FROM task_assignees ta WHERE ta.task_id=t.id AND ta.user_id=?))"
            params.extend([user["id"], user["id"]])
        if received_from:
            sql += " AND t.received_date>=?"
            params.append(str(received_from))
        if received_to:
            sql += " AND t.received_date<=?"
            params.append(str(received_to))
        if assignee_id is not None:
            sql += " AND EXISTS(SELECT 1 FROM task_assignees ta_filter WHERE ta_filter.task_id=t.id AND ta_filter.user_id=?)"
            params.append(assignee_id)

        by_status = list(connection.execute(
            f"SELECT visible.status,COUNT(*) count FROM ({sql}) visible GROUP BY visible.status",
            params,
        ))
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
        return by_status, list(connection.execute(user_sql, user_params))

    @staticmethod
    def completed_calendar_rows(
        connection: Any,
        user: Any,
        first_day: date,
        next_month: date,
    ) -> list[Any]:
        """Return authorized completed-task rows with the legacy calendar ordering."""
        sql = "SELECT t.* FROM tasks t WHERE t.deleted_at IS NULL"
        params: list[Any] = []
        if user["role"] != "ADMIN":
            sql += " AND (t.created_by=? OR EXISTS(SELECT 1 FROM task_assignees ta WHERE ta.task_id=t.id AND ta.user_id=?))"
            params.extend([user["id"], user["id"]])
        params.extend([str(first_day), str(next_month)])
        return list(connection.execute(
            sql + " AND t.status='COMPLETED' AND t.completed_date>=? "
            "AND t.completed_date<? ORDER BY t.completed_date,t.id",
            params,
        ))
