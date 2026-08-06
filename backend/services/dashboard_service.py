"""Dashboard aggregate operations extracted from the HTTP router."""
from __future__ import annotations

import re
from datetime import date
from typing import Any, Callable, ContextManager, Literal

from fastapi import HTTPException

try:
    from repositories.dashboard_repository import DashboardRepository
except ModuleNotFoundError:
    from backend.repositories.dashboard_repository import DashboardRepository


class DashboardService:
    """Calculate caller-authorized task aggregates without HTTP concerns."""

    def __init__(
        self,
        db: Callable[[], ContextManager[Any]],
        task_view: Callable[[Any, Any], dict],
        task_export_workbook: Callable[[Any, list, Any], bytes],
        audit: Callable[..., None],
        repository: DashboardRepository,
    ) -> None:
        self._db = db
        self._task_view = task_view
        self._task_export_workbook = task_export_workbook
        self._audit = audit
        self._repository = repository


    def statistics(
        self,
        received_from: date | None,
        received_to: date | None,
        assignee_id: int | None,
        user: Any,
    ) -> dict:
        """Return the unchanged authorized status and processor aggregates."""
        with self._db() as connection:
            if received_from and received_to and received_from > received_to:
                raise HTTPException(status_code=422, detail="접수일 시작일은 종료일보다 늦을 수 없습니다.")
            if user["role"] != "ADMIN" and assignee_id is not None and assignee_id != user["id"]:
                raise HTTPException(status_code=403, detail="일반 이용자의 처리자 필터는 본인으로 고정됩니다.")
            user_scope = assignee_id if assignee_id is not None else (
                user["id"] if user["role"] != "ADMIN" else None
            )
            status_rows, user_rows = self._repository.statistics_rows(
                connection, user, received_from, received_to, assignee_id, user_scope
            )
            by_status = {name: 0 for name in ("RECEIVED", "IN_PROGRESS", "COMPLETED")}
            for row in status_rows:
                by_status[row["status"]] = row["count"]
            total = sum(by_status.values())
            by_user = []
            for row in user_rows:
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
            rows = self._repository.completed_calendar_rows(
                connection, user, first_day, next_month
            )
            return [self._task_view(connection, row) for row in rows]

    def export_tasks_xlsx(
        self,
        status: Literal["RECEIVED", "IN_PROGRESS", "COMPLETED"] | None,
        q: str | None,
        received_from: date | None,
        received_to: date | None,
        due_from: date | None,
        due_to: date | None,
        assignee_id: int | None,
        user: Any,
        ip: str | None,
    ) -> bytes:
        """Create the unchanged, caller-authorized XLSX task export."""
        if received_from and received_to and received_from > received_to:
            raise HTTPException(status_code=422, detail="접수일 시작일은 종료일보다 늦을 수 없습니다.")
        if due_from and due_to and due_from > due_to:
            raise HTTPException(status_code=422, detail="마감일 시작일은 종료일보다 늦을 수 없습니다.")
        if user["role"] != "ADMIN" and assignee_id is not None and assignee_id != user["id"]:
            raise HTTPException(status_code=403, detail="일반 이용자의 처리자 필터는 본인으로 고정됩니다.")
        with self._db() as connection:
            keyword = (q or "").strip()
            rows = self._repository.export_task_rows(
                connection,
                user,
                status,
                keyword,
                received_from,
                received_to,
                due_from,
                due_to,
                assignee_id,
            )
            if len(rows) > 10_000:
                raise HTTPException(status_code=422, detail="엑셀 내보내기는 한 번에 최대 10,000건까지 가능합니다. 필터를 좁혀 다시 시도하세요.")
            document = self._task_export_workbook(connection, rows, user)
            self._audit(connection, user["id"], "TASKS_EXPORTED", "TASK_EXPORT", "FILTERED_SCOPE", after={
                "count": len(rows), "status": status, "received_from": str(received_from) if received_from else None,
                "received_to": str(received_to) if received_to else None, "due_from": str(due_from) if due_from else None,
                "due_to": str(due_to) if due_to else None, "assignee_id": assignee_id, "has_keyword": bool(keyword),
            }, ip=ip)
            return document
