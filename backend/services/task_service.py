"""Task-read business operations extracted from the HTTP router.

The service receives existing application helpers explicitly so its initial boundary
move preserves the established SQLCipher transaction, authorization scope, task
view shape, and error responses without importing the ASGI application.
"""
from __future__ import annotations

import hashlib
import os
import re
import uuid
from datetime import date
from pathlib import Path
from typing import Any, Callable, ContextManager, Mapping
from urllib.parse import quote

from fastapi import HTTPException
from fastapi.responses import FileResponse

try:
    from repositories.task_repository import TaskRepository
except ModuleNotFoundError:
    from backend.repositories.task_repository import TaskRepository


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
        task_history: Callable[[Any, int], list[dict]],
        private_image_path: Callable[[str], Any],
        private_upload_path: Callable[[str], Any],
        image_view: Callable[[Any], dict],
        attachment_view: Callable[[Any], dict],
        rotate_private_image: Callable[[bytes, str, str], bytes],
        image_suffixes: Mapping[str, str],
        upload_dir: Path,
        max_image_count: int,
        max_image_bytes: int,
        validate_image_upload: Callable[[Any, bytes], str],
        attachment_rules: Mapping[str, tuple[str, str, int]],
        max_attachment_count: int,
        validate_attachment_upload: Callable[[Any, bytes], tuple[str, str, str]],
        integrity_error: type[Exception],
        repository: TaskRepository,
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
        self._task_history = task_history
        self._private_image_path = private_image_path
        self._private_upload_path = private_upload_path
        self._image_view = image_view
        self._attachment_view = attachment_view
        self._rotate_private_image = rotate_private_image
        self._image_suffixes = image_suffixes
        self._upload_dir = upload_dir
        self._max_image_count = max_image_count
        self._max_image_bytes = max_image_bytes
        self._validate_image_upload = validate_image_upload
        self._attachment_rules = attachment_rules
        self._max_attachment_count = max_attachment_count
        self._validate_attachment_upload = validate_attachment_upload
        self._integrity_error = integrity_error
        self._repository = repository

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
            active = self._repository.active_user_ids(connection)
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
            active = self._repository.active_user_ids(connection)
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

    def delete_task(self, task_id: int, user: Any, ip_address: str | None) -> dict:
        """Soft-delete a task with the established admin audit and cleanup behavior."""
        with self._db() as connection:
            task = self._accessible_task(connection, task_id, user)
            before = self._task_view(connection, task)
            connection.execute(
                "UPDATE tasks SET deleted_at=?,deleted_by=?,updated_at=? WHERE id=?",
                (self._now(), user["id"], self._now(), task_id),
            )
            connection.execute("DELETE FROM notification_outbox WHERE task_id=?", (task_id,))
            self._audit(
                connection,
                user["id"],
                "TASK_DELETED",
                "TASK",
                task_id,
                before,
                None,
                ip_address,
            )
            return {"ok": True}

    async def upload_task_images(
        self, task_id: int, images: list[Any], user: Any, ip_address: str | None
    ) -> dict:
        """Store validated private images with the established authorization and audit behavior."""
        if not images or len(images) > self._max_image_count:
            raise HTTPException(status_code=422, detail="한 번에 이미지는 1개 이상 5개 이하만 업로드할 수 있습니다.")
        prepared: list[tuple[Any, bytes, str]] = []
        try:
            for upload in images:
                content = await upload.read(self._max_image_bytes + 1)
                if not content or len(content) > self._max_image_bytes:
                    raise HTTPException(status_code=422, detail="이미지 파일당 최대 크기는 10MB입니다.")
                prepared.append((upload, content, self._validate_image_upload(upload, content)))

            created_paths: list[Path] = []
            try:
                with self._db() as connection:
                    self._accessible_task(connection, task_id, user)
                    existing_count = connection.execute(
                        "SELECT COUNT(*) FROM task_images WHERE task_id=?", (task_id,)
                    ).fetchone()[0]
                    if existing_count + len(prepared) > self._max_image_count:
                        raise HTTPException(status_code=422, detail="업무당 이미지는 최대 5개까지 첨부할 수 있습니다.")
                    self._upload_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
                    uploaded = []
                    for offset, (upload, content, mime_type) in enumerate(prepared):
                        storage_key = f"{task_id}/{uuid.uuid4().hex}{self._image_suffixes[mime_type]}"
                        destination = self._private_image_path(storage_key)
                        destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                        destination.write_bytes(content)
                        try:
                            os.chmod(destination, 0o600)
                        except OSError:
                            pass
                        created_paths.append(destination)
                        filename = Path(upload.filename or "image").name[-255:] or "image"
                        image_id = connection.execute(
                            "INSERT INTO task_images(task_id,storage_key,original_filename,mime_type,size_bytes,sort_order,uploaded_by,created_at) VALUES(?,?,?,?,?,?,?,?)",
                            (task_id, storage_key, filename, mime_type, len(content), existing_count + offset, user["id"], self._now()),
                        ).lastrowid
                        row = connection.execute("SELECT * FROM task_images WHERE id=?", (image_id,)).fetchone()
                        uploaded.append(self._image_view(row))
                    self._audit(
                        connection, user["id"], "TASK_IMAGE_UPLOADED", "TASK", task_id,
                        after={"images": uploaded}, ip=ip_address,
                    )
                    return {"images": uploaded}
            except self._integrity_error as exc:
                for path in created_paths:
                    path.unlink(missing_ok=True)
                raise HTTPException(status_code=422, detail="업무당 이미지는 최대 5개까지 첨부할 수 있습니다.") from exc
            except Exception:
                for path in created_paths:
                    path.unlink(missing_ok=True)
                raise
        finally:
            for upload in images:
                await upload.close()

    async def upload_task_attachments(
        self, task_id: int, attachments: list[Any], user: Any, ip_address: str | None
    ) -> dict:
        """Store validated private documents/videos with the existing audit behavior."""
        if not attachments or len(attachments) > self._max_attachment_count:
            raise HTTPException(status_code=422, detail="한 번에 문서/동영상 첨부는 1개 이상 10개 이하만 업로드할 수 있습니다.")
        # Authorize before inspecting private bytes, preserving direct-URL protection.
        with self._db() as connection:
            self._accessible_task(connection, task_id, user)
        prepared: list[tuple[Any, bytes, str, str, str]] = []
        created_paths: list[Path] = []
        try:
            for upload in attachments:
                rule = self._attachment_rules.get((upload.content_type or "").lower())
                if not rule:
                    raise HTTPException(status_code=422, detail="문서는 PDF, TXT, DOCX, XLSX만, 동영상은 MP4, WEBM만 허용합니다.")
                content = await upload.read(rule[2] + 1)
                if not content or len(content) > rule[2]:
                    limit_mb = rule[2] // (1024 * 1024)
                    attachment_kind = "문서" if rule[0] == "DOCUMENT" else "동영상"
                    raise HTTPException(status_code=422, detail=f"{attachment_kind} 파일당 최대 크기는 {limit_mb}MB입니다.")
                attachment_type, suffix, mime_type = self._validate_attachment_upload(upload, content)
                prepared.append((upload, content, attachment_type, suffix, mime_type))
            with self._db() as connection:
                self._accessible_task(connection, task_id, user)
                existing_count = connection.execute(
                    "SELECT COUNT(*) FROM task_attachments WHERE task_id=?", (task_id,)
                ).fetchone()[0]
                if existing_count + len(prepared) > self._max_attachment_count:
                    raise HTTPException(status_code=422, detail="업무당 문서/동영상 첨부는 최대 10개입니다.")
                self._upload_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
                uploaded = []
                for upload, content, attachment_type, suffix, mime_type in prepared:
                    storage_key = f"attachments/{task_id}/{uuid.uuid4().hex}{suffix}"
                    destination = self._private_upload_path(storage_key)
                    destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                    destination.write_bytes(content)
                    try:
                        os.chmod(destination, 0o600)
                    except OSError:
                        pass
                    created_paths.append(destination)
                    filename = Path(upload.filename or f"attachment{suffix}").name[-255:] or f"attachment{suffix}"
                    attachment_id = connection.execute(
                        "INSERT INTO task_attachments(task_id,storage_key,original_filename,mime_type,attachment_type,size_bytes,sha256,uploaded_by,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
                        (
                            task_id, storage_key, filename, mime_type, attachment_type, len(content),
                            hashlib.sha256(content).hexdigest(), user["id"], self._now(),
                        ),
                    ).lastrowid
                    row = connection.execute(
                        "SELECT * FROM task_attachments WHERE id=?", (attachment_id,)
                    ).fetchone()
                    uploaded.append(self._attachment_view(row))
                self._audit(
                    connection, user["id"], "TASK_ATTACHMENT_UPLOADED", "TASK", task_id,
                    after={"attachments": uploaded}, ip=ip_address,
                )
                return {"attachments": uploaded}
        except self._integrity_error as exc:
            for path in created_paths:
                path.unlink(missing_ok=True)
            raise HTTPException(status_code=422, detail="업무당 문서/동영상 첨부는 최대 10개입니다.") from exc
        except Exception:
            for path in created_paths:
                path.unlink(missing_ok=True)
            raise
        finally:
            for upload in attachments:
                await upload.close()

    def get_task_history(self, task_id: int, user: Any) -> list[dict]:
        """Return the existing audit history after task-level authorization."""
        with self._db() as connection:
            self._accessible_task(connection, task_id, user)
            return self._task_history(connection, task_id)

    def get_task_image(self, task_id: int, image_id: int, user: Any) -> FileResponse:
        """Serve one private image after the established task-level authorization."""
        with self._db() as connection:
            self._accessible_task(connection, task_id, user)
            image = connection.execute(
                "SELECT * FROM task_images WHERE id=? AND task_id=?", (image_id, task_id)
            ).fetchone()
            if not image:
                raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")
            path = self._private_image_path(image["storage_key"])
            if not path.is_file():
                raise HTTPException(status_code=404, detail="이미지 파일을 찾을 수 없습니다.")
            return FileResponse(
                path,
                media_type=image["mime_type"],
                headers={"Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"},
            )

    def download_task_attachment(
        self, task_id: int, attachment_id: int, user: Any
    ) -> FileResponse:
        """Authorize first, then return a private attachment with forced download headers."""
        with self._db() as connection:
            self._accessible_task(connection, task_id, user)
            attachment = connection.execute(
                "SELECT * FROM task_attachments WHERE id=? AND task_id=?",
                (attachment_id, task_id),
            ).fetchone()
            if not attachment:
                raise HTTPException(status_code=404, detail="첨부 파일을 찾을 수 없습니다.")
            path = self._private_upload_path(attachment["storage_key"])
            if not path.is_file():
                raise HTTPException(status_code=404, detail="첨부 파일을 찾을 수 없습니다.")
            safe_name = quote(attachment["original_filename"], safe="")
            return FileResponse(
                path,
                media_type=attachment["mime_type"],
                filename=attachment["original_filename"],
                headers={
                    "Cache-Control": "private, no-store",
                    "X-Content-Type-Options": "nosniff",
                    "Content-Disposition": f"attachment; filename*=UTF-8''{safe_name}",
                },
            )

    def delete_task_attachment(
        self, task_id: int, attachment_id: int, user: Any, ip_address: str | None
    ) -> dict:
        """Delete one authorized private attachment with its established audit event."""
        with self._db() as connection:
            self._accessible_task(connection, task_id, user)
            attachment = connection.execute(
                "SELECT * FROM task_attachments WHERE id=? AND task_id=?",
                (attachment_id, task_id),
            ).fetchone()
            if not attachment:
                raise HTTPException(status_code=404, detail="첨부 파일을 찾을 수 없습니다.")
            result = self._attachment_view(attachment)
            path = self._private_upload_path(attachment["storage_key"])
            connection.execute("DELETE FROM task_attachments WHERE id=?", (attachment_id,))
            self._audit(
                connection,
                user["id"],
                "TASK_ATTACHMENT_DELETED",
                "TASK",
                task_id,
                before={"attachment": result},
                ip=ip_address,
            )
        path.unlink(missing_ok=True)
        return {"ok": True}

    def edit_task_image(
        self, task_id: int, image_id: int, payload: Any, user: Any, ip_address: str | None
    ) -> dict:
        """Create the established private non-destructive image revision."""
        created_path: Path | None = None
        try:
            with self._db() as connection:
                self._accessible_task(connection, task_id, user)
                image = connection.execute(
                    "SELECT * FROM task_images WHERE id=? AND task_id=?", (image_id, task_id)
                ).fetchone()
                if not image:
                    raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")
                source_path = self._private_image_path(image["storage_key"])
                if not source_path.is_file():
                    raise HTTPException(status_code=404, detail="이미지 파일을 찾을 수 없습니다.")
                edited_content = self._rotate_private_image(
                    source_path.read_bytes(), image["mime_type"], payload.direction
                )
                storage_key = f"edits/{task_id}/{uuid.uuid4().hex}{self._image_suffixes[image['mime_type']]}"
                destination = self._private_image_path(storage_key)
                destination.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                destination.write_bytes(edited_content)
                try:
                    os.chmod(destination, 0o600)
                except OSError:
                    pass
                created_path = destination
                connection.execute(
                    "INSERT INTO task_image_edits(task_id,image_id,source_storage_key,result_storage_key,direction,edited_by,created_at) VALUES(?,?,?,?,?,?,?)",
                    (
                        task_id,
                        image_id,
                        image["storage_key"],
                        storage_key,
                        payload.direction,
                        user["id"],
                        self._now(),
                    ),
                )
                connection.execute(
                    "UPDATE task_images SET storage_key=?,size_bytes=? WHERE id=?",
                    (storage_key, len(edited_content), image_id),
                )
                updated = connection.execute(
                    "SELECT * FROM task_images WHERE id=?", (image_id,)
                ).fetchone()
                result = self._image_view(updated)
                self._audit(
                    connection,
                    user["id"],
                    "TASK_IMAGE_EDITED",
                    "TASK",
                    task_id,
                    before={"image_id": image_id, "direction": payload.direction},
                    after={"image": result, "direction": payload.direction},
                    ip=ip_address,
                )
                return {
                    "image": result,
                    "direction": payload.direction,
                    "non_destructive": True,
                }
        except Exception:
            if created_path is not None:
                created_path.unlink(missing_ok=True)
            raise

    def delete_task_image(
        self, task_id: int, image_id: int, user: Any, ip_address: str | None
    ) -> dict:
        """Delete one authorized image and its retained private source revision."""
        with self._db() as connection:
            self._accessible_task(connection, task_id, user)
            image = connection.execute(
                "SELECT * FROM task_images WHERE id=? AND task_id=?", (image_id, task_id)
            ).fetchone()
            if not image:
                raise HTTPException(status_code=404, detail="이미지를 찾을 수 없습니다.")
            result = self._image_view(image)
            paths = {self._private_image_path(image["storage_key"])}
            paths.update(
                self._private_image_path(row["source_storage_key"])
                for row in connection.execute(
                    "SELECT source_storage_key FROM task_image_edits WHERE image_id=?", (image_id,)
                )
            )
            connection.execute("DELETE FROM task_images WHERE id=?", (image_id,))
            self._audit(
                connection,
                user["id"],
                "TASK_IMAGE_DELETED",
                "TASK",
                task_id,
                before={"image": result},
                ip=ip_address,
            )
        for path in paths:
            path.unlink(missing_ok=True)
        return {"ok": True}

    def get_received_date_calendar(self, month: str, user: Any) -> list[dict]:
        """Return all authorized live tasks received during a validated month."""
        if not re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", month):
            raise HTTPException(
                status_code=422,
                detail="month는 유효한 YYYY-MM 형식이어야 합니다.",
            )
        year, month_number = map(int, month.split("-"))
        first_day = date(year, month_number, 1)
        next_month = (
            date(year + 1, 1, 1)
            if month_number == 12
            else date(year, month_number + 1, 1)
        )
        with self._db() as connection:
            sql, params = self._task_query_sql(user)
            sql += " AND t.received_date>=? AND t.received_date<? ORDER BY t.received_date"
            params.extend([str(first_day), str(next_month)])
            return [self._task_view(connection, row) for row in connection.execute(sql, params)]
