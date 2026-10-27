import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

import main


class TestUpgBase001(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="shared-calendar-upg-base-")
        self.previous_db_path = main.DB_PATH
        self.previous_upload_dir = main.UPLOAD_DIR
        self.previous_bootstrap = os.environ.get("WORK_CALENDAR_INITIAL_ADMIN_PASSWORD")
        main.DB_PATH = Path(self.temp_dir.name) / "calendar.db"
        main.UPLOAD_DIR = Path(self.temp_dir.name) / "private-images"
        os.environ["WORK_CALENDAR_INITIAL_ADMIN_PASSWORD"] = "base-test-admin"
        main.SESSIONS.clear()
        main.init_db()
        self.client = TestClient(main.app)

    def tearDown(self):
        self.client.close()
        main.SESSIONS.clear()
        main.DB_PATH = self.previous_db_path
        main.UPLOAD_DIR = self.previous_upload_dir
        if self.previous_bootstrap is None:
            os.environ.pop("WORK_CALENDAR_INITIAL_ADMIN_PASSWORD", None)
        else:
            os.environ["WORK_CALENDAR_INITIAL_ADMIN_PASSWORD"] = self.previous_bootstrap
        self.temp_dir.cleanup()

    def test_mounted_api_and_representative_responses(self):
        # Freeze deterministic mounted API routes snapshot
        def get_routes(app):
            # Current included-router contexts preserve the effective prefix;
            # older supported FastAPI versions expose flattened APIRoutes.
            try:
                from fastapi.routing import iter_route_contexts
            except ImportError:
                iter_route_contexts = None
            routes = []
            if iter_route_contexts is not None:
                for context in iter_route_contexts(app.routes):
                    methods = getattr(context.route, "methods", None)
                    if methods and context.path.startswith("/api"):
                        routes.extend(f"{method} {context.path}" for method in methods)
            else:
                for route in app.routes:
                    methods = getattr(route, "methods", None)
                    if methods and route.path.startswith("/api"):
                        routes.extend(f"{method} {route.path}" for method in methods)
                    elif hasattr(route, "routes"):
                        routes.extend(get_routes(route))
            return routes

        actual_routes = sorted(get_routes(main.app))
        expected_routes = [
    "DELETE /api/tasks/{task_id}",
    "DELETE /api/tasks/{task_id}/attachments/{attachment_id}",
    "DELETE /api/tasks/{task_id}/images/{image_id}",
    "GET /api/admin/audit-logs",
    "GET /api/admin/organizations",
    "GET /api/admin/request-contacts",
    "GET /api/admin/users",
    "GET /api/assignees",
    "GET /api/calendar",
    "GET /api/completed-calendar",
    "GET /api/me",
    "GET /api/me/notification-preferences",
    "GET /api/notifications",
    "GET /api/organizations",
    "GET /api/request-contacts",
    "GET /api/statistics",
    "GET /api/tasks",
    "GET /api/tasks/export.xlsx",
    "GET /api/tasks/{task_id}",
    "GET /api/tasks/{task_id}/attachments/{attachment_id}",
    "GET /api/tasks/{task_id}/history",
    "GET /api/tasks/{task_id}/images/{image_id}",
    "PATCH /api/admin/organizations/{organization_id}",
    "PATCH /api/admin/request-contacts/{contact_id}",
    "PATCH /api/admin/users/{user_id}",
    "PATCH /api/me/notification-preferences",
    "PATCH /api/tasks/{task_id}",
    "POST /api/admin/users",
    "POST /api/auth/login",
    "POST /api/auth/logout",
    "POST /api/me/password",
    "POST /api/notifications/{notification_id}/read",
    "POST /api/organizations",
    "POST /api/request-contacts",
    "POST /api/tasks",
    "POST /api/tasks/{task_id}/attachments",
    "POST /api/tasks/{task_id}/images",
    "POST /api/tasks/{task_id}/images/{image_id}/edit"
]
        self.assertEqual(actual_routes, expected_routes)

        # Test missing auth yields 401
        response = self.client.get("/api/me")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "로그인이 필요합니다.")

        # Perform login to test a representative valid response
        login_response = self.client.post(
            "/api/auth/login",
            json={"login_id": "admin", "password": "base-test-admin"}
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Test admin endpoint requires password change initially
        users_response = self.client.get("/api/admin/users", headers=headers)
        self.assertEqual(users_response.status_code, 403)
        self.assertEqual(users_response.json()["detail"], "최초 로그인 후 비밀번호를 변경해야 합니다.")

        # Complete initial password change
        pw_change = self.client.post(
            "/api/me/password",
            headers=headers,
            json={"current_password": "base-test-admin", "new_password": "new-admin-password"}
        )
        self.assertEqual(pw_change.status_code, 200)

        # Login with new password
        login_response = self.client.post(
            "/api/auth/login",
            json={"login_id": "admin", "password": "new-admin-password"}
        )
        self.assertEqual(login_response.status_code, 200)
        token = login_response.json()["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Test exact representative response fields
        me_response = self.client.get("/api/me", headers=headers)
        self.assertEqual(me_response.status_code, 200)
        me_data = me_response.json()
        self.assertEqual(set(me_data.keys()), {'must_change_password', 'login_id', 'name', 'id', 'role'})
        self.assertEqual(me_data["role"], "ADMIN")

        # Create a member to test tasks
        create_user_response = self.client.post(
            "/api/admin/users", headers=headers,
            json={"login_id": "testmember", "temporary_password": "member_pass", "name": "Member", "role": "MEMBER"}
        )
        self.assertEqual(create_user_response.status_code, 201)

        member_login = self.client.post("/api/auth/login", json={"login_id": "testmember", "password": "member_pass"})
        member_token = member_login.json()["token"]
        member_headers = {"Authorization": f"Bearer {member_token}"}

        # Change member password
        member_pw_change = self.client.post("/api/me/password", headers=member_headers, json={"current_password": "member_pass", "new_password": "new_member_pass"})
        self.assertEqual(member_pw_change.status_code, 200)

        # Member login again
        member_login = self.client.post("/api/auth/login", json={"login_id": "testmember", "password": "new_member_pass"})
        member_token = member_login.json()["token"]
        member_headers = {"Authorization": f"Bearer {member_token}"}

        # Test tasks endpoint representative response for member
        tasks_response = self.client.get("/api/tasks", headers=member_headers)
        self.assertEqual(tasks_response.status_code, 200)
        self.assertIn("items", tasks_response.json())
        self.assertIn("summary", tasks_response.json())
        self.assertIn("pagination", tasks_response.json())

        # Exact MEMBER administrator-denial assertions
        for admin_route in ["/api/admin/users", "/api/admin/audit-logs", "/api/admin/organizations", "/api/admin/request-contacts"]:
            denial = self.client.get(admin_route, headers=member_headers)
            self.assertEqual(denial.status_code, 403)
            self.assertEqual(denial.json()["detail"], "관리자 권한이 필요합니다.")

    def test_fixture_db_schema_frozen(self):
        import json
        with open(Path(__file__).parent / "fixtures" / "upg_base_contract.json", "r", encoding="utf-8") as f:
            expected_tables = json.load(f)

        tables = {}
        with main.db() as conn:
            cursor = conn.execute("SELECT name, sql FROM sqlite_master WHERE type='table' ORDER BY name")
            tables = {row["name"]: row["sql"] for row in cursor.fetchall()}

        # Freeze the WHOLE fixture schema set with equality, not only a subset loop
        self.assertEqual(tables, expected_tables)

if __name__ == "__main__":
    unittest.main()
