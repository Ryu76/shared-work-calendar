"""Fresh-environment API acceptance tests for the Phase 1 MVP.

This intentionally exercises the public API as independently authenticated users,
rather than relying on database inspection or frontend-only visibility rules.
"""
import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient

import main


BOOTSTRAP_PASSWORD = "acceptance-bootstrap-admin-123"
ADMIN_PASSWORD = "acceptance-admin-password-123"
MEMBER_PASSWORD = "acceptance-member-password-123"
PNG_BYTES = b"\x89PNG\r\n\x1a\nacceptance-image"


class PhaseOneAcceptanceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(prefix="shared-calendar-acceptance-")
        self.previous_db_path = main.DB_PATH
        self.previous_upload_dir = main.UPLOAD_DIR
        self.previous_bootstrap = os.environ.get("WORK_CALENDAR_INITIAL_ADMIN_PASSWORD")
        main.DB_PATH = Path(self.temp_dir.name) / "calendar.db"
        main.UPLOAD_DIR = Path(self.temp_dir.name) / "private-images"
        os.environ["WORK_CALENDAR_INITIAL_ADMIN_PASSWORD"] = BOOTSTRAP_PASSWORD
        main.SESSIONS.clear()
        main.init_db()
        self.client = TestClient(main.app)
        self.admin = self.login("admin", BOOTSTRAP_PASSWORD)
        self.change_password(self.admin, BOOTSTRAP_PASSWORD, ADMIN_PASSWORD)
        # The original admin token remains valid after its password change.
        self.member_a_id = self.create_member("acceptance_a")
        self.member_b_id = self.create_member("acceptance_b")
        self.member_c_id = self.create_member("acceptance_c")
        self.member_a = self.login_and_activate("acceptance_a")
        self.member_b = self.login_and_activate("acceptance_b")
        self.member_c = self.login_and_activate("acceptance_c")

    def tearDown(self):
        main.SESSIONS.clear()
        main.DB_PATH = self.previous_db_path
        main.UPLOAD_DIR = self.previous_upload_dir
        if self.previous_bootstrap is None:
            os.environ.pop("WORK_CALENDAR_INITIAL_ADMIN_PASSWORD", None)
        else:
            os.environ["WORK_CALENDAR_INITIAL_ADMIN_PASSWORD"] = self.previous_bootstrap
        self.temp_dir.cleanup()

    def login(self, login_id, password):
        response = self.client.post("/api/auth/login", json={"login_id": login_id, "password": password})
        self.assertEqual(response.status_code, 200, response.text)
        return {"Authorization": "Bearer " + response.json()["token"]}

    def change_password(self, headers, current_password, new_password):
        response = self.client.post(
            "/api/me/password",
            headers=headers,
            json={"current_password": current_password, "new_password": new_password},
        )
        self.assertEqual(response.status_code, 200, response.text)

    def create_member(self, login_id):
        response = self.client.post(
            "/api/admin/users",
            headers=self.admin,
            json={
                "login_id": login_id,
                "name": login_id,
                "role": "MEMBER",
                "temporary_password": "temporary-password-123",
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()["id"]

    def login_and_activate(self, login_id):
        headers = self.login(login_id, "temporary-password-123")
        self.change_password(headers, "temporary-password-123", MEMBER_PASSWORD)
        return headers

    def create_task(self, headers, assignee_ids, description, received_date, status="RECEIVED"):
        response = self.client.post(
            "/api/tasks",
            headers=headers,
            json={
                "assignee_ids": assignee_ids,
                "contact": {
                    "name": "수용 요청 담당자",
                    "phone": "010-9876-5432",
                    "organization": "수용 기관",
                },
                "description": description,
                "received_date": received_date,
                "status": status,
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()

    def test_phase_one_task_authorization_status_images_calendar_and_audit_acceptance(self):
        """Cover every PRD acceptance criterion in one isolated HTTP-style workflow."""
        # AC 2 + AC 6: a creator can select multiple processors and retains access
        # even when the creator is no longer an assignee.
        creator_only = self.create_task(
            self.member_a,
            [self.member_b_id, self.member_c_id],
            "생성자 전용 접근 수용 업무",
            "2031-05-10",
        )
        creator_id = self.client.get("/api/me", headers=self.member_a).json()["id"]
        self.assertNotIn(creator_id, [assignee["id"] for assignee in creator_only["assignees"]])
        creator_detail = self.client.get(f"/api/tasks/{creator_only['id']}", headers=self.member_a)
        self.assertEqual(creator_detail.status_code, 200, creator_detail.text)
        creator_patch = self.client.patch(
            f"/api/tasks/{creator_only['id']}",
            headers=self.member_a,
            json={"description": "생성자가 처리자가 아니어도 수정한 수용 업무"},
        )
        self.assertEqual(creator_patch.status_code, 200, creator_patch.text)
        self.assertEqual(creator_patch.json()["description"], "생성자가 처리자가 아니어도 수정한 수용 업무")

        # AC 5: both assignees can see and modify the jointly assigned task.
        for headers in (self.member_b, self.member_c):
            self.assertEqual(self.client.get(f"/api/tasks/{creator_only['id']}", headers=headers).status_code, 200)
        joint_patch = self.client.patch(
            f"/api/tasks/{creator_only['id']}",
            headers=self.member_b,
            json={"status": "IN_PROGRESS"},
        )
        self.assertEqual(joint_patch.status_code, 200, joint_patch.text)
        self.assertEqual(joint_patch.json()["status"], "IN_PROGRESS")

        # AC 4: a nonparticipant cannot discover, open, inspect history for, or
        # modify a task belonging only to another member.
        private_task = self.create_task(
            self.member_b,
            [self.member_b_id],
            "B만 볼 수 있는 비공개 수용 업무",
            "2031-05-11",
        )
        # AC 3: the same requester information is reused as a single master record
        # and remains discoverable for a later task through authenticated autocomplete.
        self.assertEqual(private_task["requester_contact_id"], creator_only["requester_contact_id"])
        contacts = self.client.get("/api/request-contacts?q=수용 기관", headers=self.member_b)
        self.assertEqual(contacts.status_code, 200, contacts.text)
        self.assertTrue(any(
            contact["id"] == private_task["requester_contact_id"]
            and contact["name"] == "수용 요청 담당자"
            and contact["phone"] == "010-9876-5432"
            and contact["organization"] == "수용 기관"
            for contact in contacts.json()
        ))
        member_a_list = self.client.get("/api/tasks", headers=self.member_a)
        self.assertEqual(member_a_list.status_code, 200, member_a_list.text)
        self.assertNotIn(private_task["id"], [task["id"] for task in member_a_list.json()["items"]])
        for method, path, kwargs in (
            (self.client.get, f"/api/tasks/{private_task['id']}", {}),
            (self.client.get, f"/api/tasks/{private_task['id']}/history", {}),
            (self.client.patch, f"/api/tasks/{private_task['id']}", {"json": {"description": "권한 우회"}}),
        ):
            response = method(path, headers=self.member_a, **kwargs)
            self.assertEqual(response.status_code, 403, response.text)

        # AC 8–10: completion automatically stamps a date, clearing completion
        # removes it, and a non-completed status never preserves a supplied date.
        completed = self.client.patch(
            f"/api/tasks/{private_task['id']}", headers=self.member_b, json={"status": "COMPLETED"}
        )
        self.assertEqual(completed.status_code, 200, completed.text)
        self.assertIsNotNone(completed.json()["completed_date"])
        cleared = self.client.patch(
            f"/api/tasks/{private_task['id']}", headers=self.member_b,
            json={"status": "IN_PROGRESS", "completed_date": "2031-05-12"},
        )
        self.assertEqual(cleared.status_code, 200, cleared.text)
        self.assertIsNone(cleared.json()["completed_date"])

        # AC 11: private image bytes require the same task authorization as detail.
        uploaded = self.client.post(
            f"/api/tasks/{private_task['id']}/images",
            headers=self.member_b,
            files=[("images", ("acceptance.png", PNG_BYTES, "image/png"))],
        )
        self.assertEqual(uploaded.status_code, 201, uploaded.text)
        image = uploaded.json()["images"][0]
        self.assertNotIn("storage_key", image)
        self.assertEqual(
            self.client.get(
                f"/api/tasks/{private_task['id']}/images/{image['id']}", headers=self.member_a
            ).status_code,
            403,
        )
        served = self.client.get(
            f"/api/tasks/{private_task['id']}/images/{image['id']}", headers=self.member_b
        )
        self.assertEqual(served.status_code, 200, served.text)
        self.assertEqual(served.content, PNG_BYTES)
        self.assertEqual(served.headers["cache-control"], "private, no-store")

        # AC 7: the administrator sees every task in both list and received-date calendar.
        admin_list = self.client.get("/api/tasks?page_size=100", headers=self.admin)
        self.assertEqual(admin_list.status_code, 200, admin_list.text)
        self.assertTrue({creator_only["id"], private_task["id"]}.issubset({task["id"] for task in admin_list.json()["items"]}))
        admin_calendar = self.client.get("/api/calendar?month=2031-05", headers=self.admin)
        self.assertEqual(admin_calendar.status_code, 200, admin_calendar.text)
        self.assertTrue({creator_only["id"], private_task["id"]}.issubset({task["id"] for task in admin_calendar.json()}))

        # AC 12: significant changes are retained in the administrator-only audit trail.
        audit = self.client.get("/api/admin/audit-logs", headers=self.admin)
        self.assertEqual(audit.status_code, 200, audit.text)
        private_actions = {
            record["action"]
            for record in audit.json()
            if record["target_type"] == "TASK" and record["target_id"] == str(private_task["id"])
        }
        self.assertTrue({"TASK_CREATED", "TASK_UPDATED", "TASK_IMAGE_UPLOADED"}.issubset(private_actions))
        self.assertEqual(self.client.get("/api/admin/audit-logs", headers=self.member_b).status_code, 403)

        # Request-information management is administrator-only in the UI/API layer:
        # searchable master records can be edited and deactivated without erasing
        # the request data retained by existing tasks.
        master_contacts = self.client.get("/api/admin/request-contacts?q=수용", headers=self.admin)
        self.assertEqual(master_contacts.status_code, 200, master_contacts.text)
        master_contact = next(row for row in master_contacts.json() if row["id"] == creator_only["requester_contact_id"])
        master_orgs = self.client.get("/api/admin/organizations?q=수용", headers=self.admin)
        self.assertEqual(master_orgs.status_code, 200, master_orgs.text)
        master_org = next(row for row in master_orgs.json() if row["id"] == master_contact["organization_id"])
        renamed_org = self.client.patch(
            f"/api/admin/organizations/{master_org['id']}", headers=self.admin,
            json={"name": "수용 기관 수정"},
        )
        self.assertEqual(renamed_org.status_code, 200, renamed_org.text)
        retired_contact = self.client.patch(
            f"/api/admin/request-contacts/{master_contact['id']}", headers=self.admin,
            json={"name": "수정 수용 요청 담당자", "is_active": False},
        )
        self.assertEqual(retired_contact.status_code, 200, retired_contact.text)
        retained_task = self.client.get(f"/api/tasks/{creator_only['id']}", headers=self.member_a)
        self.assertEqual(retained_task.status_code, 200, retained_task.text)
        self.assertEqual(retained_task.json()["contact"]["name"], "수정 수용 요청 담당자")
        self.assertEqual(retained_task.json()["contact"]["organization"], "수용 기관 수정")
        self.assertFalse(any(row["id"] == master_contact["id"] for row in self.client.get("/api/request-contacts?q=수정", headers=self.member_a).json()))

        # The same fresh environment verifies list query/filter/page metadata used by
        # the rendered task filter and pager controls.
        first_page = self.client.get("/api/tasks?q=수용&page=1&page_size=1", headers=self.admin)
        second_page = self.client.get("/api/tasks?q=수용&page=2&page_size=1", headers=self.admin)
        self.assertEqual(first_page.status_code, 200, first_page.text)
        self.assertEqual(second_page.status_code, 200, second_page.text)
        self.assertEqual(first_page.json()["pagination"], {"page": 1, "page_size": 1, "total": 2, "total_pages": 2})
        self.assertEqual(second_page.json()["pagination"], {"page": 2, "page_size": 1, "total": 2, "total_pages": 2})
        self.assertNotEqual(first_page.json()["items"][0]["id"], second_page.json()["items"][0]["id"])
        self.assertEqual(
            self.client.get("/api/tasks?received_from=2031-05-12&received_to=2031-05-10", headers=self.admin).status_code,
            422,
        )

        # AC 1: administrators can deactivate a member and the server immediately
        # rejects a subsequent login for that inactive account.
        deactivated = self.client.patch(
            f"/api/admin/users/{self.member_c_id}", headers=self.admin, json={"is_active": False}
        )
        self.assertEqual(deactivated.status_code, 200, deactivated.text)
        self.assertFalse(deactivated.json()["is_active"])
        denied_login = self.client.post(
            "/api/auth/login", json={"login_id": "acceptance_c", "password": MEMBER_PASSWORD}
        )
        self.assertEqual(denied_login.status_code, 401, denied_login.text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
