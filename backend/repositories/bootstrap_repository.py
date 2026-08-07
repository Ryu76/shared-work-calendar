"""Database bootstrap and compatible schema migration persistence."""
from __future__ import annotations

import os
from typing import Any, Callable


_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
  id INTEGER PRIMARY KEY, login_id TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL, name TEXT NOT NULL,
  role TEXT NOT NULL CHECK(role IN ('ADMIN','MEMBER')),
  is_active INTEGER NOT NULL DEFAULT 1,
  must_change_password INTEGER NOT NULL DEFAULT 1,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS organizations (
  id INTEGER PRIMARY KEY, name TEXT UNIQUE NOT NULL,
  is_active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS request_contacts (
  id INTEGER PRIMARY KEY, name TEXT NOT NULL, phone TEXT NOT NULL,
  organization_id INTEGER NOT NULL REFERENCES organizations(id),
  is_active INTEGER NOT NULL DEFAULT 1, created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
  UNIQUE(name, phone, organization_id)
);
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY, requester_contact_id INTEGER NOT NULL REFERENCES request_contacts(id),
  status TEXT NOT NULL CHECK(status IN ('RECEIVED','IN_PROGRESS','COMPLETED')),
  description TEXT NOT NULL, received_date TEXT NOT NULL, completed_date TEXT, due_date TEXT,
  created_by INTEGER NOT NULL REFERENCES users(id), created_at TEXT NOT NULL, updated_at TEXT NOT NULL,
  deleted_at TEXT, deleted_by INTEGER REFERENCES users(id),
  CHECK((status = 'COMPLETED' AND completed_date IS NOT NULL) OR (status != 'COMPLETED' AND completed_date IS NULL))
);
CREATE TABLE IF NOT EXISTS task_assignees (
  task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  user_id INTEGER NOT NULL REFERENCES users(id), assigned_at TEXT NOT NULL,
  PRIMARY KEY(task_id,user_id)
);
CREATE TABLE IF NOT EXISTS task_images (
  id INTEGER PRIMARY KEY, task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  storage_key TEXT UNIQUE NOT NULL, original_filename TEXT NOT NULL, mime_type TEXT NOT NULL,
  size_bytes INTEGER NOT NULL CHECK(size_bytes > 0 AND size_bytes <= 10485760),
  sort_order INTEGER NOT NULL, uploaded_by INTEGER NOT NULL REFERENCES users(id), created_at TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS task_images_max_count
BEFORE INSERT ON task_images
WHEN (SELECT COUNT(*) FROM task_images WHERE task_id=NEW.task_id) >= 5
BEGIN SELECT RAISE(ABORT, '업무당 이미지는 최대 5개입니다.'); END;
CREATE TABLE IF NOT EXISTS task_image_edits (
  id INTEGER PRIMARY KEY, task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  image_id INTEGER NOT NULL REFERENCES task_images(id) ON DELETE CASCADE,
  source_storage_key TEXT NOT NULL, result_storage_key TEXT UNIQUE NOT NULL,
  direction TEXT NOT NULL CHECK(direction IN ('CLOCKWISE','COUNTERCLOCKWISE')),
  edited_by INTEGER NOT NULL REFERENCES users(id), created_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_task_image_edits_image_created
  ON task_image_edits(image_id, created_at, id);
CREATE TABLE IF NOT EXISTS task_attachments (
  id INTEGER PRIMARY KEY, task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  storage_key TEXT UNIQUE NOT NULL, original_filename TEXT NOT NULL, mime_type TEXT NOT NULL,
  attachment_type TEXT NOT NULL CHECK(attachment_type IN ('DOCUMENT','VIDEO')),
  size_bytes INTEGER NOT NULL CHECK(size_bytes > 0 AND size_bytes <= 104857600),
  sha256 TEXT NOT NULL, uploaded_by INTEGER NOT NULL REFERENCES users(id), created_at TEXT NOT NULL
);
CREATE TRIGGER IF NOT EXISTS task_attachments_max_count
BEFORE INSERT ON task_attachments
WHEN (SELECT COUNT(*) FROM task_attachments WHERE task_id=NEW.task_id) >= 10
BEGIN SELECT RAISE(ABORT, '업무당 문서/동영상 첨부는 최대 10개입니다.'); END;
CREATE TABLE IF NOT EXISTS audit_logs (
  id INTEGER PRIMARY KEY, actor_user_id INTEGER REFERENCES users(id), action TEXT NOT NULL,
  target_type TEXT NOT NULL, target_id TEXT NOT NULL, before_data TEXT, after_data TEXT,
  ip_address TEXT, created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS notification_preferences (
  user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  due_soon_enabled INTEGER NOT NULL DEFAULT 1 CHECK(due_soon_enabled IN (0,1)),
  overdue_enabled INTEGER NOT NULL DEFAULT 1 CHECK(overdue_enabled IN (0,1)),
  updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS notification_outbox (
  id INTEGER PRIMARY KEY,
  user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  task_id INTEGER NOT NULL REFERENCES tasks(id) ON DELETE CASCADE,
  kind TEXT NOT NULL CHECK(kind IN ('DUE_SOON','DUE_TODAY','OVERDUE')),
  due_date TEXT NOT NULL,
  message TEXT NOT NULL,
  read_at TEXT,
  created_at TEXT NOT NULL,
  UNIQUE(user_id, task_id, kind, due_date)
);
CREATE INDEX IF NOT EXISTS idx_tasks_live_received_status
  ON tasks(deleted_at, received_date, status);
CREATE INDEX IF NOT EXISTS idx_task_assignees_user_task
  ON task_assignees(user_id, task_id);
CREATE INDEX IF NOT EXISTS idx_notification_outbox_user_read
  ON notification_outbox(user_id, read_at, id DESC);
CREATE INDEX IF NOT EXISTS idx_task_attachments_task_created
  ON task_attachments(task_id, created_at, id);
"""


class BootstrapRepository:
    """Own compatible schema creation, migration, and initial-admin persistence."""

    @staticmethod
    def initialize(
        connection: Any, hash_password: Callable[[str], str], now: Callable[[], str]
    ) -> None:
        """Initialize legacy-compatible tables without changing existing data/schema contracts."""
        connection.executescript(_SCHEMA)
        task_columns = {row["name"] for row in connection.execute("PRAGMA table_info('tasks')")}
        if "due_date" not in task_columns:
            connection.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")
        connection.execute(
            "CREATE INDEX IF NOT EXISTS idx_tasks_live_due_date ON tasks(deleted_at, due_date, status)"
        )
        if connection.execute("SELECT 1 FROM users WHERE login_id='admin'").fetchone():
            return
        bootstrap_password = os.getenv("WORK_CALENDAR_INITIAL_ADMIN_PASSWORD")
        if not bootstrap_password or len(bootstrap_password) < 8:
            raise RuntimeError(
                "새 데이터베이스를 초기화하려면 8자 이상의 WORK_CALENDAR_INITIAL_ADMIN_PASSWORD를 설정해야 합니다."
            )
        timestamp = now()
        connection.execute(
            "INSERT INTO users(login_id,password_hash,name,role,is_active,must_change_password,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?)",
            ("admin", hash_password(bootstrap_password), "초기 관리자", "ADMIN", 1, 1, timestamp, timestamp),
        )
