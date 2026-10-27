"""Bulk task view projection service."""
from __future__ import annotations

import sqlite3
from typing import Any, Callable

try:
    from repositories.task_repository import TaskRepository
except ModuleNotFoundError:
    from backend.repositories.task_repository import TaskRepository

class TaskProjectionService:
    """Project authorized task summaries eliminating N+1 database queries."""

    def __init__(
        self,
        repository: TaskRepository,
        image_view: Callable[[Any], dict],
        attachment_view: Callable[[Any], dict],
    ) -> None:
        self._repository = repository
        self._image_view = image_view
        self._attachment_view = attachment_view

    def task_views(self, connection: sqlite3.Connection, tasks: list[sqlite3.Row]) -> list[dict]:
        """Project multiple tasks using bounded bulk queries to eliminate N+1."""
        if not tasks:
            return []

        task_ids = list(dict.fromkeys(t["id"] for t in tasks))
        creator_ids = list({t["created_by"] for t in tasks})
        contact_ids = list({t["requester_contact_id"] for t in tasks})

        # Fetch in chunks of 300
        creators = {}
        for i in range(0, len(creator_ids), 300):
            chunk = creator_ids[i:i + 300]
            creators.update(self._repository.users_by_ids(connection, chunk))

        contacts = {}
        for i in range(0, len(contact_ids), 300):
            chunk = contact_ids[i:i + 300]
            contacts.update(self._repository.contacts_by_ids(connection, chunk))

        assignees_by_task = {tid: [] for tid in task_ids}
        for i in range(0, len(task_ids), 300):
            chunk = task_ids[i:i + 300]
            for row in self._repository.assignees_by_task_ids(connection, chunk):
                item = dict(row)
                item.pop("task_id", None)
                assignees_by_task[row["task_id"]].append(item)

        images_by_task = {tid: [] for tid in task_ids}
        for i in range(0, len(task_ids), 300):
            chunk = task_ids[i:i + 300]
            for row in self._repository.images_by_task_ids(connection, chunk):
                images_by_task[row["task_id"]].append(self._image_view(row))

        attachments_by_task = {tid: [] for tid in task_ids}
        for i in range(0, len(task_ids), 300):
            chunk = task_ids[i:i + 300]
            for row in self._repository.attachments_by_task_ids(connection, chunk):
                attachments_by_task[row["task_id"]].append(self._attachment_view(row))

        result = []
        for task in tasks:
            tid = task["id"]
            out = dict(task)
            out["created_by_name"] = creators[task["created_by"]]
            out["assignees"] = assignees_by_task.get(tid, [])
            out["contact"] = contacts.get(task["requester_contact_id"])
            out["images"] = images_by_task.get(tid, [])
            out["attachments"] = attachments_by_task.get(tid, [])
            result.append(out)

        return result
