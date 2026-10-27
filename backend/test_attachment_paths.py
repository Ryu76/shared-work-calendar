"""Real encrypted API regression for private attachments beyond Windows MAX_PATH."""
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


BACKEND_DIR = Path(__file__).resolve().parent
# Keep the focused command importable from either the repository or backend root.
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
PROGRAM = r'''
import os
from pathlib import Path
import sqlite3
from fastapi import HTTPException
from fastapi.testclient import TestClient
import main

content = b"%PDF-1.4\nlong-private-document\n%%EOF"
with TestClient(main.app, raise_server_exceptions=False) as client:
    login = client.post("/api/auth/login", json={"login_id": "admin", "password": os.environ["WORK_CALENDAR_INITIAL_ADMIN_PASSWORD"]})
    assert login.status_code == 200
    headers = {"Authorization": "Bearer " + login.json()["token"]}
    changed = client.post("/api/me/password", headers=headers, json={"current_password": os.environ["WORK_CALENDAR_INITIAL_ADMIN_PASSWORD"], "new_password": "long-fixture-password-123"})
    assert changed.status_code == 200
    login = client.post("/api/auth/login", json={"login_id": "admin", "password": "long-fixture-password-123"})
    assert login.status_code == 200
    headers = {"Authorization": "Bearer " + login.json()["token"]}
    me = client.get("/api/me", headers=headers)
    assert me.status_code == 200
    task = client.post("/api/tasks", headers=headers, json={"assignee_ids": [me.json()["id"]], "contact": {"name": "Long fixture", "phone": "010-1111-2222", "organization": "Fixture"}, "description": "Long private upload", "received_date": "2031-06-15", "status": "RECEIVED"})
    assert task.status_code == 201
    task_id = task.json()["id"]
    endpoint = f"/api/tasks/{task_id}/attachments"
    uploaded = client.post(endpoint, headers=headers, files=[("attachments", ("long-report.pdf", content, "application/pdf"))])
    assert uploaded.status_code == 201, f"attachment upload: expected 201, actual {uploaded.status_code}"
    attachment = uploaded.json()["attachments"][0]
    assert attachment["attachment_type"] == "DOCUMENT"
    assert "storage_key" not in attachment and "sha256" not in attachment
    with main.db() as connection:
        row = connection.execute("SELECT storage_key FROM task_attachments WHERE id=?", (attachment["id"],)).fetchone()
        logical_path = Path(os.environ["WORK_CALENDAR_UPLOAD_DIR"]) / row["storage_key"]
        assert len(str(logical_path)) > 260, "fixture did not cross MAX_PATH"
        assert main.private_upload_path(row["storage_key"]).read_bytes() == content
    download = f"{endpoint}/{attachment['id']}"
    assert client.get(download).status_code == 401
    served = client.get(download, headers=headers)
    assert served.status_code == 200 and served.content == content
    assert served.headers["cache-control"] == "private, no-store"
    assert "attachment" in served.headers["content-disposition"]
    for unsafe in ("../../outside.pdf", str(Path(os.environ["WORK_CALENDAR_UPLOAD_DIR"]).parent / "outside.pdf")):
        try:
            main.private_upload_path(unsafe)
        except HTTPException as error:
            assert error.status_code == 404
        else:
            raise AssertionError("private path containment was weakened")
    connection = sqlite3.connect(os.environ["WORK_CALENDAR_DB"])
    try:
        try:
            connection.execute("SELECT name FROM sqlite_master").fetchall()
        except sqlite3.DatabaseError:
            pass
        else:
            raise AssertionError("encrypted fixture readable without SQLCipher")
    finally:
        connection.close()
    deleted = client.delete(download, headers=headers)
    assert deleted.status_code == 200
    assert client.get(download, headers=headers).status_code == 404
print("LONG_ATTACHMENT_UPLOAD_DOWNLOAD_DELETE_PASS")
'''


class AttachmentPathRegressionTests(unittest.TestCase):
    def test_real_private_attachment_round_trip_beyond_windows_max_path(self):
        # Parent imports no application/settings. The child receives only fresh
        # synthetic paths and a generated, unlogged SQLCipher key.
        with tempfile.TemporaryDirectory(prefix="cal-long-") as directory:
            root = Path(directory)
            upload = root / "uploads"
            while len(str(upload)) < 235:
                remaining = 235 - len(str(upload)) - 1
                if remaining <= 0:
                    break
                upload /= "p" * min(remaining, 30)
            env = {name: value for name, value in os.environ.items() if not name.startswith("WORK_CALENDAR_")}
            env.update({
                "WORK_CALENDAR_DB": str(root / "calendar.db"),
                "WORK_CALENDAR_DB_KEY_FILE": str(root / "isolated.dpapi"),
                "WORK_CALENDAR_DB_KEY": secrets.token_hex(32),
                "WORK_CALENDAR_UPLOAD_DIR": str(upload),
                "WORK_CALENDAR_INITIAL_ADMIN_PASSWORD": secrets.token_urlsafe(24),
                "WORK_CALENDAR_LOG_LEVEL": "ERROR",
                "PYTHONNOUSERSITE": "1",
                "PYTHONDONTWRITEBYTECODE": "1",
            })
            result = subprocess.run(
                [sys.executable, "-s", "-c", PROGRAM], cwd=BACKEND_DIR, env=env,
                capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=90,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("LONG_ATTACHMENT_UPLOAD_DOWNLOAD_DELETE_PASS", result.stdout)
        self.assertFalse(root.exists(), "isolated long-path resources were not removed")


class BrowserFixtureCleanupRegressionTests(unittest.TestCase):
    def native_root(self, directory):
        from test_browser_ui import native_namespace_path
        return native_namespace_path(directory)

    def test_native_namespace_path_is_idempotent(self):
        from test_browser_ui import native_namespace_path
        if os.name == "nt":
            self.assertEqual(native_namespace_path("C:\\plain"), "\\\\?\\C:\\plain")
            self.assertEqual(native_namespace_path("\\\\?\\C:\\plain"), "\\\\?\\C:\\plain")
            self.assertEqual(native_namespace_path("\\\\server\\share"), "\\\\?\\UNC\\server\\share")
            self.assertEqual(native_namespace_path("\\\\?\\UNC\\server\\share"), "\\\\?\\UNC\\server\\share")

    def test_actual_real_tree_removal_in_already_prefixed_tmp(self):
        from test_browser_ui import remove_browser_fixture_tree, native_namespace_path
        with tempfile.TemporaryDirectory(prefix="cal-clean-") as directory:
            prefixed = native_namespace_path(directory)
            Path(prefixed, "synthetic.txt").write_text("fixture", encoding="utf-8")
            remove_browser_fixture_tree(prefixed)
            self.assertFalse(Path(directory).exists())

    def test_permission_retry_removes_the_real_owned_tree(self):
        import shutil
        from test_browser_ui import remove_browser_fixture_tree
        real_remove = shutil.rmtree
        with tempfile.TemporaryDirectory(prefix="cal-clean-") as directory:
            Path(directory, "synthetic.txt").write_text("fixture", encoding="utf-8")
            attempts = []

            def sharing_then_remove(root):
                attempts.append(root)
                if len(attempts) == 1:
                    raise PermissionError("synthetic sharing violation")
                real_remove(root)

            with patch("test_browser_ui.shutil.rmtree", side_effect=sharing_then_remove), patch("test_browser_ui.time.sleep"):
                remove_browser_fixture_tree(self.native_root(directory))
            self.assertEqual(len(attempts), 2)
            self.assertFalse(Path(directory).exists())

    def test_exhausted_permission_error_is_not_suppressed(self):
        from test_browser_ui import remove_browser_fixture_tree
        with tempfile.TemporaryDirectory(prefix="cal-clean-") as directory:
            with patch("test_browser_ui.shutil.rmtree", side_effect=PermissionError("synthetic sharing violation")) as remove, patch("test_browser_ui.time.sleep"):
                with self.assertRaises(PermissionError):
                    remove_browser_fixture_tree(self.native_root(directory))
            self.assertEqual(remove.call_count, 6)
            self.assertTrue(Path(directory).exists())
        self.assertFalse(Path(directory).exists())

    def test_other_cleanup_errors_are_not_retried(self):
        from test_browser_ui import remove_browser_fixture_tree
        with tempfile.TemporaryDirectory(prefix="cal-clean-") as directory:
            with patch("test_browser_ui.shutil.rmtree", side_effect=OSError("synthetic other failure")) as remove, patch("test_browser_ui.time.sleep"):
                with self.assertRaises(OSError):
                    remove_browser_fixture_tree(self.native_root(directory))
            self.assertEqual(remove.call_count, 1)
            self.assertTrue(Path(directory).exists())
        self.assertFalse(Path(directory).exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
