"""Repeatable rendered-browser regression coverage for the Phase 1 administrator UI.

The test starts an isolated application process, uses a fresh SQLite database/private
upload directory, and drives the actual single-page application in Chromium.  It does
not read or modify the repository's product database.
"""
import base64
import json
import os
import random
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright


BOOTSTRAP_PASSWORD = "browser-bootstrap-admin-123"
ADMIN_PASSWORD = "browser-admin-password-123"
BACKEND_DIR = Path(__file__).resolve().parent


def unused_local_port() -> int:
    """Choose an unused high port to avoid low-port services on shared Windows hosts."""
    for _ in range(100):
        candidate = random.SystemRandom().randint(49152, 65535)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind(("127.0.0.1", candidate))
            except OSError:
                continue
        return candidate
    raise RuntimeError("Could not reserve a high local port for the browser test server")


class BrowserUiRegressionTests(unittest.TestCase):
    """Exercise rendered controls that cannot be covered by API acceptance alone."""

    def setUp(self):
        self._cleaned_up = False
        self.temp_dir = tempfile.TemporaryDirectory(prefix="shared-calendar-browser-")
        # Register cleanup before readiness checks: unittest does not call tearDown
        # when setUp fails, and otherwise a failed startup can strand a local Uvicorn
        # process and its isolated SQLite database on Windows.
        self.addCleanup(self._cleanup_resources)
        self.server = None
        env = os.environ.copy()
        env.update({
            "WORK_CALENDAR_DB": str(Path(self.temp_dir.name) / "calendar.db"),
            "WORK_CALENDAR_UPLOAD_DIR": str(Path(self.temp_dir.name) / "private-images"),
            "WORK_CALENDAR_INITIAL_ADMIN_PASSWORD": BOOTSTRAP_PASSWORD,
        })
        # A Windows worker can occasionally leave a just-launched Uvicorn process
        # alive but unable to serve its selected random port.  Retry with a fresh
        # isolated port instead of turning an unrelated browser regression into a
        # 75-second false product failure.
        startup_error = "no server launch attempted"
        for _ in range(3):
            self.port = unused_local_port()
            self.base_url = f"http://127.0.0.1:{self.port}"
            self.server = subprocess.Popen(
                [
                    sys.executable, "-m", "uvicorn", "main:app", "--host", "127.0.0.1",
                    "--port", str(self.port), "--no-access-log", "--log-level", "warning",
                ],
                cwd=BACKEND_DIR,
                env=env,
                # Do not leave a high-volume Uvicorn output pipe unread during
                # Playwright runs; it can otherwise block a healthy local server.
                stdout=subprocess.DEVNULL,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
            )
            startup_error = self._wait_for_server()
            if startup_error is None:
                break
            self._stop_server()
        else:
            self.fail("Browser test server did not become ready: " + startup_error)
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch()
        self.page = self.browser.new_page(viewport={"width": 1280, "height": 900})
        self.page_errors = []
        self.responses = []
        self.page.on("pageerror", lambda error: self.page_errors.append(str(error)))
        self.page.on("response", lambda response: self.responses.append((response.request.method, response.status, response.url)))

    def _cleanup_resources(self):
        if self._cleaned_up:
            return
        self._cleaned_up = True
        if hasattr(self, "browser"):
            self.browser.close()
        if hasattr(self, "playwright"):
            self.playwright.stop()
        self._stop_server()
        if hasattr(self, "temp_dir"):
            self.temp_dir.cleanup()

    def _stop_server(self):
        if self.server is not None:
            if self.server.poll() is None and os.name == "nt":
                # Uvicorn is launched through the Windows Python executable.  Kill
                # its complete process tree so a failed test cannot leave an
                # isolated database server bound to a random local port.
                subprocess.run(
                    ["taskkill", "/PID", str(self.server.pid), "/T", "/F"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            elif self.server.poll() is None:
                self.server.terminate()
            try:
                self.server.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.server.kill()
                self.server.wait(timeout=10)
            self.server = None

    def tearDown(self):
        self._cleanup_resources()

    def _server_output(self) -> str:
        if self.server.poll() is None:
            return "server is still running (output is intentionally discarded during browser tests)"
        return "server output is not captured during browser tests"

    def _wait_for_server(self) -> str | None:
        # Argon2id initialization can contend with the preceding isolated API suite
        # on constrained Windows workers.  The former 30-second per-attempt limit
        # occasionally killed a healthy local Uvicorn process before it completed
        # startup, creating a false browser regression.  Keep the retry bounded,
        # but allow one complete slow local startup before declaring a product error.
        deadline = time.monotonic() + 60
        last_error = "no request attempted"
        while time.monotonic() < deadline:
            if self.server.poll() is not None:
                return "server exited during startup: " + self._server_output()
            try:
                with urllib.request.urlopen(self.base_url + "/", timeout=1) as response:
                    if response.status == 200:
                        return None
                    last_error = f"HTTP {response.status} from {self.base_url}/"
            except urllib.error.HTTPError as error:
                last_error = f"HTTP {error.code} from {self.base_url}/"
            except urllib.error.URLError as error:
                last_error = f"URL error from {self.base_url}/: {error.reason}"
            time.sleep(0.1)
        return f"{last_error}; {self._server_output()}"

    def api(self, method: str, path: str, payload=None, token: str | None = None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(
            self.base_url + path,
            data=json.dumps(payload).encode("utf-8") if payload is not None else None,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read().decode("utf-8"))

    def upload_png(self, task_id: int, token: str):
        """Upload a real small PNG using the same multipart endpoint as the UI."""
        png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAIAAAADCAYAAAC56t6BAAAAFUlEQVR4nGPkUbL4z8DAwMAEIlAYACEfAWtsOP0DAAAAAElFTkSuQmCC"
        )
        boundary = "----shared-calendar-browser-test-boundary"
        body = (
            f"--{boundary}\r\n"
            "Content-Disposition: form-data; name=\"images\"; filename=\"browser-preview.png\"\r\n"
            "Content-Type: image/png\r\n\r\n"
        ).encode("ascii") + png + f"\r\n--{boundary}--\r\n".encode("ascii")
        request = urllib.request.Request(
            self.base_url + f"/api/tasks/{task_id}/images",
            data=body,
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": f"multipart/form-data; boundary={boundary}",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            self.assertEqual(response.status, 201)
            return json.loads(response.read().decode("utf-8"))["images"][0]

    def seed_detail_task_with_private_image(self):
        status, login = self.api("POST", "/api/auth/login", {"login_id": "admin", "password": ADMIN_PASSWORD})
        self.assertEqual(status, 200, login)
        token = login["token"]
        status, admin = self.api("GET", "/api/me", token=token)
        self.assertEqual(status, 200, admin)
        status, task = self.api(
            "POST",
            "/api/tasks",
            {
                "assignee_ids": [admin["id"]],
                "contact": {
                    "name": "상세 브라우저 요청 담당자",
                    "phone": "010-2222-3333",
                    "organization": "상세 브라우저 기관",
                },
                "description": "브라우저 상세 편집 확인 업무",
                "received_date": "2031-06-15",
                "status": "RECEIVED",
            },
            token,
        )
        self.assertEqual(status, 201, task)
        image = self.upload_png(task["id"], token)
        return task, image

    def browser_login_and_change_initial_password(self):
        self.page.goto(self.base_url, wait_until="networkidle")
        self.page.locator("#loginId").fill("admin")
        self.page.locator("#password").fill(BOOTSTRAP_PASSWORD)
        self.page.get_by_role("button", name="로그인").click()
        self.page.locator("#currentPassword").wait_for()
        self.page.locator("#currentPassword").fill(BOOTSTRAP_PASSWORD)
        self.page.locator("#newPassword").fill(ADMIN_PASSWORD)
        self.page.locator("#newPasswordConfirm").fill(ADMIN_PASSWORD)
        self.page.get_by_role("button", name="비밀번호 변경").click()
        self.page.locator("#taskFilters").wait_for()

    def seed_tasks(self):
        status, login = self.api("POST", "/api/auth/login", {"login_id": "admin", "password": ADMIN_PASSWORD})
        self.assertEqual(status, 200, login)
        token = login["token"]
        status, admin = self.api("GET", "/api/me", token=token)
        self.assertEqual(status, 200, admin)
        for number in range(21):
            status, task = self.api(
                "POST",
                "/api/tasks",
                {
                    "assignee_ids": [admin["id"]],
                    "contact": {
                        "name": "브라우저 요청 담당자",
                        "phone": "010-1111-2222",
                        "organization": "브라우저 기관",
                    },
                    "description": f"브라우저 목록 업무 {number + 1:02d}",
                    "received_date": "2031-05-10",
                    "status": "RECEIVED",
                },
                token,
            )
            self.assertEqual(status, 201, task)

    def test_admin_master_management_and_task_filter_pagination_ui(self):
        """Cover rendered request-master edits plus task filter errors and paging."""
        self.browser_login_and_change_initial_password()
        self.seed_tasks()
        self.page.reload(wait_until="networkidle")
        self.page.locator("#taskList .board-task").first.wait_for()

        # Request contacts are a genuine name/organization autocomplete rather than
        # a fixed first-page selector: selecting a matched entry fills all three
        # request fields used for task creation.
        self.page.get_by_role("button", name="업무 등록").click()
        self.page.get_by_role("heading", name="업무 등록").wait_for()
        contact_search = self.page.locator("#contactSearch")
        with self.page.expect_response(
            lambda response: "/api/request-contacts?" in response.url and response.request.method == "GET"
        ) as contact_search_response:
            contact_search.fill("브라우저 기관")
        self.assertEqual(contact_search_response.value.status, 200)
        contact_label = "브라우저 요청 담당자 · 브라우저 기관 · 010-1111-2222"
        contact_search.fill(contact_label)
        self.page.locator("#contactName").wait_for()
        self.page.wait_for_function(
            """() => document.querySelector('#contactName')?.value === '브라우저 요청 담당자'
            && document.querySelector('#phone')?.value === '010-1111-2222'
            && document.querySelector('#organization')?.value === '브라우저 기관'"""
        )
        self.assertTrue(self.page.locator("#contactSuggestions option").count() >= 1)
        self.page.get_by_role("button", name="전체 업무").click()
        # Reload only to reset the SPA's in-memory route after exercising the
        # autocomplete form.  `networkidle` is not a product readiness criterion
        # here and can be held open by Chromium connection reuse on Windows;
        # the rendered filter form is the actual UI readiness condition.
        self.page.reload(wait_until="domcontentloaded")
        self.page.locator("#taskFilters").wait_for()

        # Task filtering rejects an inverted date range in the accessible in-place
        # alert, then the page-aware pager reaches the server's next result page.
        self.page.locator("#receivedFrom").fill("2031-05-12")
        self.page.locator("#receivedTo").fill("2031-05-10")
        self.page.locator("#taskFilters").get_by_role("button", name="적용").click()
        self.page.locator("#taskFilterError").get_by_text("접수일 시작일은 종료일보다 늦을 수 없습니다.").wait_for()
        self.page.locator("#resetFilters").click()
        self.page.locator("#search").fill("브라우저 목록 업무")
        self.page.locator("#taskFilters").get_by_role("button", name="적용").click()
        # The administrator board initially renders only three cards for a status.
        # It requests the next three only after the explicit right-side load affordance.
        self.page.locator("#taskList .board-task").nth(2).wait_for()
        self.assertEqual(self.page.locator("#taskList .board-task").count(), 3)
        load_more = self.page.locator("#taskList .board-load-sentinel")
        self.assertEqual(load_more.count(), 1)
        with self.page.expect_response(
            lambda response: response.url.startswith(self.base_url + "/api/tasks?")
            and "page=2" in response.url
            and "page_size=3" in response.url,
        ) as next_page_response:
            load_more.click()
        self.assertEqual(next_page_response.value.status, 200)
        self.assertEqual(next_page_response.value.json()["pagination"]["page"], 2)
        self.page.locator("#taskList .board-task").nth(5).wait_for()
        self.assertEqual(self.page.locator("#taskList .board-task").count(), 6)

        # Administrator request-information organization editing uses the rendered
        # management controls; contact lifecycle and authorization are covered in
        # the isolated API acceptance suite.
        self.page.get_by_role("button", name="요청 정보 관리").click()
        self.page.get_by_role("heading", name="요청 정보 관리").wait_for()
        organization_form = self.page.locator("[data-org]").first
        self.assertEqual(organization_form.count(), 1)
        organization_form.locator('input[name="name"]').fill("브라우저 기관 수정")
        with self.page.expect_response(
            lambda response: "/api/admin/organizations/" in response.url and response.request.method == "PATCH"
        ) as organization_update:
            organization_form.get_by_role("button", name="저장").click()
        self.assertEqual(organization_update.value.status, 200)
        # Saving rerenders both master tables; wait before taking the contact-row locator.
        self.page.wait_for_timeout(150)
        renamed_organization = self.page.locator('[data-org] input[name="name"]')
        renamed_organization.wait_for()
        self.assertEqual(renamed_organization.input_value(), "브라우저 기관 수정")
        self.assertEqual(self.page_errors, [])

    def test_phase_two_statistics_ui_uses_authorized_aggregate_api(self):
        """Render the Phase 2 dashboard and verify the aggregate request/result."""
        self.browser_login_and_change_initial_password()
        self.seed_tasks()
        self.page.reload(wait_until="networkidle")
        with self.page.expect_response(
            lambda response: "/api/statistics?" in response.url and response.request.method == "GET"
        ) as statistics_response:
            self.page.get_by_role("button", name="통계").click()
        self.assertEqual(statistics_response.value.status, 200)
        self.assertEqual(statistics_response.value.json()["total"], 21)
        self.page.get_by_role("heading", name="운영 통계").wait_for()
        self.assertIn("접수", self.page.locator("[aria-label='상태별 업무 통계']").inner_text())
        self.assertEqual(self.page.locator("#userStatistics .task").count(), 1)
        # The Phase 2 reminder screen renders from the authenticated local-outbox API
        # and explicitly communicates that it never dispatches external messages.
        with self.page.expect_response(
            lambda response: response.url.endswith("/api/notifications") and response.request.method == "GET"
        ) as notification_response:
            self.page.get_by_role("button", name="알림").click()
        self.assertEqual(notification_response.value.status, 200)
        self.page.get_by_role("heading", name="마감 알림").wait_for()
        self.page.get_by_text("이메일·문자·메신저는 전송하지 않습니다.", exact=False).wait_for()
        self.assertEqual(self.page_errors, [])

    def test_received_date_calendar_renders_completed_work_with_green_status_tag(self):
        """The operational calendar keeps completed tasks visible by received date."""
        self.browser_login_and_change_initial_password()
        status, login = self.api("POST", "/api/auth/login", {"login_id": "admin", "password": ADMIN_PASSWORD})
        self.assertEqual(status, 200, login)
        token = login["token"]
        status, admin = self.api("GET", "/api/me", token=token)
        self.assertEqual(status, 200, admin)
        status, task = self.api(
            "POST", "/api/tasks",
            {
                "assignee_ids": [admin["id"]],
                "contact": {"name": "접수일 완료 캘린더 요청", "phone": "010-5151-6262", "organization": "접수일 완료 캘린더 기관"},
                "description": "접수일 캘린더의 처리 완료 업무",
                "status": "COMPLETED",
                "received_date": "2035-06-18",
                "completed_date": "2035-06-20",
            },
            token,
        )
        self.assertEqual(status, 201, task)
        self.page.evaluate("() => { state.month = '2035-06'; }")
        with self.page.expect_response(
            lambda response: "/api/calendar?month=2035-06" in response.url and response.request.method == "GET"
        ) as calendar_response:
            self.page.get_by_role("button", name="캘린더").click()
        self.assertEqual(calendar_response.value.status, 200)
        self.assertEqual([item["id"] for item in calendar_response.value.json()], [task["id"]])
        tag = self.page.get_by_role("button", name="18일 업무 상세 열기: 접수일 캘린더의 처리 완료 업무")
        tag.wait_for()
        self.assertIn("COMPLETED", tag.get_attribute("class"))
        self.assertEqual(self.page.locator(".panel .muted").filter(has_text="초록 처리").count(), 1)
        self.assertEqual(self.page_errors, [])

    def test_calendar_month_navigation_is_safe_in_the_product_seoul_timezone(self):
        """Month controls must not roll back when Korea is ahead of UTC."""
        self.page.close()
        seoul_context = self.browser.new_context(
            timezone_id="Asia/Seoul", viewport={"width": 1280, "height": 900}
        )
        self.page = seoul_context.new_page()
        self.page_errors = []
        self.page.on("pageerror", lambda error: self.page_errors.append(str(error)))
        self.browser_login_and_change_initial_password()

        # A UTC timestamp late on June 30 is already July 1 in Seoul. The helper
        # also supplies the new-task default date, so it must use Seoul time.
        self.assertEqual(
            self.page.evaluate("() => seoulDate(new Date('2035-06-30T15:30:00Z'))"),
            "2035-07-01",
        )
        self.page.evaluate("() => { state.month = '2035-06'; }")
        with self.page.expect_response(
            lambda response: "/api/calendar?month=2035-06" in response.url
            and response.request.method == "GET"
        ) as initial_calendar:
            self.page.get_by_role("button", name="캘린더").click()
        self.assertEqual(initial_calendar.value.status, 200)
        self.page.get_by_role("heading", name="2035-06 접수일 캘린더").wait_for()
        with self.page.expect_response(
            lambda response: "/api/calendar?month=2035-07" in response.url
            and response.request.method == "GET"
        ) as next_calendar:
            self.page.locator("#nextMonth").click()
        self.assertEqual(next_calendar.value.status, 200)
        self.page.get_by_role("heading", name="2035-07 접수일 캘린더").wait_for()
        with self.page.expect_response(
            lambda response: "/api/calendar?month=2035-06" in response.url
            and response.request.method == "GET"
        ) as previous_calendar:
            self.page.locator("#previousMonth").click()
        self.assertEqual(previous_calendar.value.status, 200)
        self.page.get_by_role("heading", name="2035-06 접수일 캘린더").wait_for()

        with self.page.expect_response(
            lambda response: "/api/completed-calendar?month=2035-06" in response.url
            and response.request.method == "GET"
        ) as initial_report:
            self.page.get_by_role("button", name="처리 리포트").click()
        self.assertEqual(initial_report.value.status, 200)
        with self.page.expect_response(
            lambda response: "/api/completed-calendar?month=2035-07" in response.url
            and response.request.method == "GET"
        ) as next_report:
            self.page.locator("#nextReportMonth").click()
        self.assertEqual(next_report.value.status, 200)
        self.page.get_by_role("heading", name="2035-07 처리일 리포트 캘린더").wait_for()
        self.assertEqual(self.page_errors, [])

    def test_completed_date_report_calendar_renders_authorized_month_view(self):
        """The separate completed-date calendar calls the protected report endpoint."""
        self.browser_login_and_change_initial_password()
        status, login = self.api("POST", "/api/auth/login", {"login_id": "admin", "password": ADMIN_PASSWORD})
        self.assertEqual(status, 200, login)
        token = login["token"]
        status, admin = self.api("GET", "/api/me", token=token)
        self.assertEqual(status, 200, admin)
        status, task = self.api(
            "POST", "/api/tasks",
            {
                "assignee_ids": [admin["id"]],
                "contact": {"name": "처리 리포트 브라우저 요청", "phone": "010-3131-4242", "organization": "처리 리포트 브라우저 기관"},
                "description": "브라우저 처리일 리포트 업무",
                "status": "COMPLETED",
                "received_date": "2035-06-01",
                "completed_date": "2035-06-18",
            },
            token,
        )
        self.assertEqual(status, 201, task)
        self.page.evaluate("() => { state.month = '2035-06'; }")
        with self.page.expect_response(
            lambda response: "/api/completed-calendar?month=2035-06" in response.url and response.request.method == "GET"
        ) as report_response:
            self.page.get_by_role("button", name="처리 리포트").click()
        self.assertEqual(report_response.value.status, 200)
        self.assertEqual([item["id"] for item in report_response.value.json()], [task["id"]])
        self.page.get_by_role("heading", name="2035-06 처리일 리포트 캘린더").wait_for()
        self.page.get_by_role("button", name="18일 처리 업무 상세 열기: 브라우저 처리일 리포트 업무").wait_for()
        self.assertIn("처리일 기준", self.page.locator(".panel").inner_text())
        self.assertEqual(self.page_errors, [])

    def test_excel_export_button_uses_filtered_authorized_download_api(self):
        """The rendered list exposes a responsive XLSX download through the protected API."""
        self.browser_login_and_change_initial_password()
        self.seed_tasks()
        self.page.reload(wait_until="networkidle")
        self.page.locator("#taskList .board-task").first.wait_for()
        with self.page.expect_download() as download_info:
            with self.page.expect_response(
                lambda response: "/api/tasks/export.xlsx" in response.url and response.request.method == "GET"
            ) as export_response:
                self.page.locator("#exportTasks").click()
        self.assertEqual(export_response.value.status, 200)
        self.assertEqual(
            export_response.value.headers["content-type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertEqual(export_response.value.headers["cache-control"], "private, no-store")
        download = download_info.value
        self.assertEqual(download.suggested_filename, "shared-work-calendar-tasks.xlsx")
        self.assertTrue(Path(download.path()).read_bytes().startswith(b"PK"))
        self.assertEqual(self.page.locator("#exportTasks").inner_text(), "엑셀 다운로드")
        self.assertEqual(self.page_errors, [])

    def test_admin_task_detail_edit_history_private_preview_and_delete_confirmation_ui(self):
        """Exercise the complete rendered task-detail vertical slice as an admin."""
        self.browser_login_and_change_initial_password()
        task, image = self.seed_detail_task_with_private_image()
        self.page.reload(wait_until="networkidle")

        # The task list exposes an actual labelled button, not a click-only card.
        opener = self.page.get_by_role("button", name=f"업무 상세 열기: {task['description']}")
        opener.wait_for()
        self.assertEqual(opener.evaluate("node => node.tagName"), "BUTTON")
        with self.page.expect_response(
            lambda response: response.url.endswith(f"/api/tasks/{task['id']}")
            and response.request.method == "GET"
        ) as detail_response:
            opener.click()
        self.assertEqual(detail_response.value.status, 200)
        self.page.get_by_role("heading", name="업무 상세 및 수정").wait_for()
        self.page.get_by_role("heading", name="변경 이력").wait_for()

        # Preview bytes are fetched over the authorized private-image endpoint and
        # rendered only as a transient blob URL, never as a public storage URL.
        preview = self.page.locator(f"img[data-private-image='{image['id']}']")
        preview.wait_for()
        self.page.wait_for_function(
            f"() => document.querySelector(\"img[data-private-image='{image['id']}']\")?.src.startsWith('blob:')"
        )
        self.assertTrue(any(
            method == "GET" and status == 200 and url.endswith(f"/api/tasks/{task['id']}/images/{image['id']}")
            for method, status, url in self.responses
        ))
        self.assertTrue(preview.get_attribute("src").startswith("blob:"))

        # The responsive detail surface exposes the safe image-edit slice. It makes
        # an authenticated POST only after a native confirmation and then renders
        # the retained private-image preview plus the audit-backed task history.
        self.page.once("dialog", lambda dialog: dialog.accept())
        with self.page.expect_response(
            lambda response: response.url.endswith(f"/api/tasks/{task['id']}/images/{image['id']}/edit")
            and response.request.method == "POST"
        ) as image_edit_response:
            self.page.locator(f"[data-edit-image='{image['id']}'][data-direction='CLOCKWISE']").click()
        self.assertEqual(image_edit_response.value.status, 200)
        self.assertTrue(image_edit_response.value.json()["non_destructive"])
        self.page.locator(".history").get_by_text("이미지 90° 회전", exact=False).wait_for()
        self.page.locator(f"[data-edit-image='{image['id']}'][data-direction='COUNTERCLOCKWISE']").wait_for()

        # An administrator's rendered edit form makes a server-authorized PATCH;
        # the resulting field-level history is shown without a page reload.
        updated_description = "브라우저에서 수정한 상세 업무"
        self.page.locator("#description").fill(updated_description)
        self.page.locator("#due").fill("2031-06-20")
        # The rendered form uploads a validated private document through the same
        # authorized task-detail save flow, then renders its download-only card.
        attachment_path = Path(self.temp_dir.name) / "browser-private-report.pdf"
        attachment_path.write_bytes(b"%PDF-1.4\nbrowser-private-attachment\n%%EOF")
        self.page.locator("#taskAttachments").set_input_files(str(attachment_path))
        with self.page.expect_response(
            lambda response: response.url.endswith(f"/api/tasks/{task['id']}")
            and response.request.method == "GET"
        ) as refreshed_detail_response:
            with self.page.expect_response(
                lambda response: response.url.endswith(f"/api/tasks/{task['id']}/attachments")
                and response.request.method == "POST"
            ) as attachment_response:
                with self.page.expect_response(
                    lambda response: response.url.endswith(f"/api/tasks/{task['id']}")
                    and response.request.method == "PATCH"
                ) as update_response:
                    self.page.get_by_role("button", name="변경 저장").click()
        self.assertEqual(update_response.value.status, 200)
        self.assertEqual(update_response.value.json()["due_date"], "2031-06-20")
        self.assertEqual(attachment_response.value.status, 201)
        self.assertEqual(attachment_response.value.json()["attachments"][0]["attachment_type"], "DOCUMENT")
        self.assertEqual(refreshed_detail_response.value.status, 200)
        self.assertEqual(refreshed_detail_response.value.json()["attachments"][0]["original_filename"], "browser-private-report.pdf")
        self.page.get_by_role("heading", name="문서/동영상 첨부").wait_for()
        self.page.locator("[data-download-attachment]").wait_for()
        self.page.get_by_text(updated_description, exact=True).wait_for()
        self.page.locator(".history").get_by_text("업무 수정", exact=False).wait_for()
        self.assertIn("업무 설명", self.page.locator(".history").inner_text())

        # A rejected native confirmation must not delete; acceptance issues the
        # administrator-only DELETE and returns to the task list.
        cancelled_dialogs = []
        self.page.once("dialog", lambda dialog: (cancelled_dialogs.append(dialog.message), dialog.dismiss()))
        self.page.locator("#deleteTask").click()
        self.page.wait_for_timeout(100)
        self.assertEqual(
            cancelled_dialogs,
            ["이 업무를 삭제하시겠습니까? 삭제 후 목록과 캘린더에서 보이지 않습니다."],
        )
        self.page.get_by_role("heading", name="업무 상세 및 수정").wait_for()
        self.page.once("dialog", lambda dialog: dialog.accept())
        with self.page.expect_response(
            lambda response: response.url.endswith(f"/api/tasks/{task['id']}")
            and response.request.method == "DELETE"
        ) as delete_response:
            self.page.locator("#deleteTask").click()
        self.assertEqual(delete_response.value.status, 200)
        self.page.locator("#taskList").wait_for()
        self.assertEqual(self.page.locator(f"[data-task-id='{task['id']}']").count(), 0)
        self.assertEqual(self.page_errors, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
