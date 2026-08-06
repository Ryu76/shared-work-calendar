# Shared Work Calendar — Current Status

## Status (2026-08-01 13:39:05 UTC — scheduled roadmap inspection, PRD conformance correction, and full regression verification)
- **Phase 1 and every PRD-authorized Phase 2 vertical slice are complete in the required order:** (1) status/user statistics, (2) task due dates with safe local-only in-app notifications, (3) expanded private document/video attachments, (4) authorization-scoped XLSX export, and (5) completed-date report calendar.
- During this run, a PRD §5 calendar conformance gap was found despite the previous complete status: `GET /api/calendar` omitted `COMPLETED` tasks even though the received-date calendar requires all three status colors, including green completed work. The server endpoint and rendered calendar were corrected. This was an additive behavior correction only; it does not migrate, modify, or delete existing SQLite data.
- The main operational calendar now returns every authorized, non-deleted task whose **received date** falls in the selected month. Completed work retains the established `.tag.COMPLETED` green UI treatment. The separate Phase-2 completed-date report calendar remains available and continues to filter only completed work by `completed_date`.
- Re-read authoritative `PRD.md`, inspected source/tests/this status file, and scanned Python/JavaScript sources for incomplete implementation markers. The PRD authorizes no Phase 3 scope. No further incomplete authorized item or safe follow-on slice was found.

## Latest Scheduled Verification (2026-08-01 14:05:18 UTC)
- Re-read the authoritative Phase-2 ordering in `PRD.md`, inspected implementation/test/UI sources and this status file, and searched Python/JavaScript for incomplete markers. All five authorized Phase-2 vertical slices remain complete in the required order; the PRD defines no authorized Phase 3 item.
- No new product slice exists to implement. Accordingly, this inspection made **no product source, schema, runtime data, attachment, notification, external-service, deployment, or credential change**. The only file updated is this verification record.
- `python -m unittest discover -s backend -p 'test*.py' -v`: **PASS** — all **25 tests** in **82.274 seconds**, including Phase-1 acceptance, all five Phase-2 API authorization/validation/migration slices, and local rendered Chromium UI coverage.
- `node --check web/app.js` and `python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS**, executed after the full successful test suite in one command chain.
- Live SQLite inspection confirmed `backend/calendar.db` remains **122,880 bytes**; `tasks` contains additive `due_date`; `task_attachments`, `notification_preferences`, and `notification_outbox` are present.
- Python and JavaScript source scans found **no** `TODO`, `FIXME`, or `NotImplemented` markers. Git metadata remains unavailable: `git status --short` reports `fatal: not a git repository (or any of the parent directories): .git`.

## Previous Scheduled Verification (2026-08-01 13:43:08 UTC)
- No new PRD-authorized implementation slice existed after the five completed Phase-2 items. The same product source/schema/data/external-service safety boundary was preserved.
- The prior full suite passed all 25 tests; static JavaScript and Python compilation checks passed; the live schema contained the additive Phase-2 tables and `due_date` migration.

## This Run
- **Changed files:**
  - `backend/main.py` — corrected the received-date calendar query to include authorized `COMPLETED` tasks as required by PRD §5.
  - `backend/test_main.py` — updated focused API coverage to assert all three task statuses appear in the received-date calendar.
  - `backend/test_browser_ui.py` — added isolated Chromium coverage that creates a completed task, verifies `/api/calendar?month=2035-06` returns it, and verifies the rendered completed-status calendar tag and green-status legend.
  - `web/app.js` — corrected the received-date calendar legend to accurately state all three visible status colors.
  - `PROGRESS.md` — recorded this implementation and verification evidence.
- No runtime product SQLite data, private attachment storage, notification preference/outbox, deployment setting, credential, or external-service configuration changed.
- Git metadata remains unavailable: `git status --short` returned `fatal: not a git repository (or any of the parent directories): .git`.

## Verification from repository root on 2026-08-01
- `python -m unittest backend.test_browser_ui.BrowserUiRegressionTests.test_received_date_calendar_renders_completed_work_with_green_status_tag -v`: **PASS** — 1 isolated rendered Chromium test in **6.710 seconds**. It received HTTP 200 from the protected calendar API, found the completed task in its response, and rendered the completed tag/green legend without page errors.
- `python -m unittest discover -s backend -p 'test*.py' -v`: **PASS** — all **25 tests** in **82.505 seconds**. This includes isolated API/regression tests, the Phase-1 acceptance workflow, and rendered Playwright Chromium UI tests.
- `node --check web/app.js`: **PASS**.
- `python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS**.
- Product SQLite schema inspection: `backend/calendar.db` is **122,880 bytes**; `tasks` contains additive `due_date` alongside `received_date` and `completed_date`; tables `task_attachments`, `notification_preferences`, and `notification_outbox` are present.
- Passing coverage includes server-side authorization/input validation, authorization-scoped status/user statistics, pre-existing SQLite due-date migration, local-only in-app notification preferences/outbox, private document/video attachment authorization, formula-safe filtered XLSX export, received-date and completed-date calendar month/scope validation, all Phase-1 acceptance criteria, and responsive Phase-2 UI controls.
- Incomplete-marker scan: **no** `TODO`, `FIXME`, or `NotImplemented` markers were found in repository Python/JavaScript sources.
- External-service safety: notification coverage validates `IN_APP_OUTBOX_ONLY`. No external service was contacted; browser regression used isolated local `127.0.0.1` Uvicorn servers.

## Roadmap
- **Remaining authorized roadmap:** none.
- **Blockers:** none.
- **Exact next priority:** inspect future source/user changes and run focused or full regression as warranted; do not invent Phase 3, alter production/deployment or product data, expose credentials, or enable external notification dispatch without explicit authorization.

## Latest Scheduled Verification (2026-08-01 14:13:05 UTC)
- Inspected authoritative `PRD.md`, source/tests, and this progress record. The five PRD-authorized Phase-2 slices remain complete in the required order; there is no authorized Phase-3 item and no incomplete slice to implement.
- No product source, SQLite schema/data, private attachment, notification outbox/preference, deployment, credential, or external-service configuration was changed. **Changed files:** `PROGRESS.md` only (this verified status record).
- `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **80.885 seconds**; JavaScript syntax and Python compilation checks also passed.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` exists; `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python/JavaScript incomplete-marker scans found no `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety verification: notification tests remain local `IN_APP_OUTBOX_ONLY`; no external notification or other external service was contacted. `git status --short` remains unavailable because this directory is not a Git repository.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, data, credential, or external-notification changes without explicit authorization.

## Latest Scheduled Verification (2026-08-01 14:17:05 UTC)
- Re-inspected authoritative `PRD.md`, implementation/test sources, and this progress record. Phase 1 and all five PRD-authorized Phase 2 vertical slices remain complete in the mandated order: status/user statistics; task due dates and safe local-only in-app notifications; document/video attachments; authorization-scoped XLSX export; and completed-date report calendar. The PRD defines no Phase 3 item, so no unimplemented authorized slice exists.
- **Changed files:** `PROGRESS.md` only (this verified status record). No product source, schema, live SQLite data, attachment, notification preference/outbox, deployment, credential, or external-service configuration was changed.
- `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **81.921 seconds**; JavaScript syntax and Python compilation checks also passed (the latter two are silent on success and the chained command exited 0).
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks` includes additive `due_date`; Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` are present. Python/JavaScript incomplete-marker scan found no `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: notification tests validate `IN_APP_OUTBOX_ONLY`; browser coverage uses isolated local `127.0.0.1` Uvicorn servers; no external notification or other external service was contacted. `git status --short` remains unavailable because this directory has no `.git` repository.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future source/user changes and run focused/full regression as warranted; do not invent Phase 3, alter deployment/product data, expose credentials, or enable external notification delivery without explicit authorization.

## Latest Scheduled Verification (2026-08-01 14:25:08 UTC)
- Inspected the authoritative `PRD.md`, current implementation and automated coverage, and this progress record. Phase 1 and all five mandated Phase-2 vertical slices remain implemented in the required order: authorization-scoped status/user statistics; due dates with notification preferences and the safe local in-app outbox; private document/video attachments; scoped formula-safe XLSX export; and the completed-date report calendar. The PRD contains no authorized Phase-3 work, no incomplete marker, and no safe unimplemented follow-on item.
- **Changed files:** `PROGRESS.md` only (this verified status record). No product source, SQLite schema/data, private attachment content, notification preferences/outbox, deployment setting, credential, or external-service configuration was changed.
- Real verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py` **PASS** — all **25 tests** passed in **80.122 seconds**; this includes isolated API authorization/validation/migration coverage and local Chromium-rendered UI flows for every Phase-2 surface. The chained JavaScript syntax and Python compilation checks succeeded with exit code 0.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` is present; all Phase-2 tables (`task_attachments`, `notification_preferences`, `notification_outbox`) are present. Python and JavaScript scans found no `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: the verified notification behavior is `IN_APP_OUTBOX_ONLY`; tests start only isolated local `127.0.0.1` Uvicorn servers. No external message, notification, or other external service was contacted. Git metadata remains unavailable because this working directory is not a Git repository.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future user/source changes and run focused or full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 14:29:07 UTC)
- Re-read authoritative `PRD.md`, implementation and test sources, and this status record. Phase 1 plus every Phase-2 item authorized in the prescribed order remain complete: status/user statistics; due dates with safe local-only in-app notifications; document/video attachments; authorization-scoped XLSX export; and completed-date report calendar. The PRD has no Phase-3 scope and no incomplete authorized slice was found.
- **Changed files:** `PROGRESS.md` only (this verification record). No product source, SQLite schema/data, private attachment, notification preference/outbox, deployment, credential, or external-service configuration changed.
- Real verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **82.180 seconds**; JavaScript syntax and Python compilation checks completed successfully. The passing suite covers Phase-1 acceptance, Phase-2 authorization/validation/migration behavior, and isolated local Chromium UI flows.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` and all Phase-2 tables (`task_attachments`, `notification_preferences`, `notification_outbox`) exist. Python and JavaScript scans found no `TODO`, `FIXME`, or `NotImplemented` markers. Notification behavior remains `IN_APP_OUTBOX_ONLY`; no external service was contacted. `git status --short` remains unavailable because the working directory is not a Git repository.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future source/user changes and run focused or full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 14:50:05 UTC)
- Re-read the authoritative `PRD.md`, inspected the implementation, automated coverage, and this progress record. Phase 1 and all five Phase-2 items remain complete in the mandated order: authorization-scoped status/user statistics; due dates with safe local in-app outbox notifications; private document/video attachments; authorization-scoped, formula-safe XLSX export; and the completed-date report calendar. No authorized Phase-3 scope or incomplete authorized slice exists.
- **Changed files:** `PROGRESS.md` only (this verification record). No product source, SQLite schema/data, attachment content, notification preference/outbox, deployment, credential, or external-service configuration was changed.
- Real verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **82.346 seconds**, including Phase-1 acceptance, authorization/validation/migration coverage for every Phase-2 slice, and isolated local Chromium UI flows. JavaScript syntax and Python compilation checks then completed successfully with exit code 0.
- Live SQLite inspection at 2026-08-01 14:50:05 UTC: `backend/calendar.db` is **122,880 bytes**; `tasks` has additive `due_date`; tables `task_attachments`, `notification_preferences`, and `notification_outbox` are present. Python and JavaScript scans found no `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: notification tests validate only `IN_APP_OUTBOX_ONLY`; browser tests use isolated local `127.0.0.1` Uvicorn servers. No external message or other external service was contacted. Git metadata is unavailable because the directory is not a Git repository.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future user/source changes and run focused or full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 15:03:15 UTC)
- Inspected authoritative `PRD.md`, `PROGRESS.md`, backend implementation/API tests, rendered-browser tests, and incomplete-work markers. Phase 1 plus all five strictly ordered, PRD-authorized Phase-2 vertical slices remain complete: status/user statistics; due dates with safe local-only in-app notifications; document/video attachment expansion; authorization-scoped formula-safe XLSX export; and completed-date report calendar. The PRD authorizes no Phase 3 slice.
- **Changed files:** `PROGRESS.md` only (this verified status record). No application source, SQLite schema/data, private attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **81.232 seconds**. This included Phase-1 acceptance, server-side authorization/input validation and legacy SQLite migration coverage, and isolated local Chromium UI flows for each Phase-2 surface. JavaScript syntax and Python compilation checks completed successfully in the same command chain (exit code 0).
- Live SQLite inspection before regression: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` exists; tables `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python/JavaScript scans found no `TODO`, `FIXME`, or `NotImplemented` markers. `git status --short` cannot run because this working directory is not a Git repository.
- Safety evidence: notifications remain `IN_APP_OUTBOX_ONLY`; browser tests started isolated `127.0.0.1` Uvicorn instances only. No external notification, message, or other external service was contacted.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused or full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 15:07:13 UTC)
- Re-read the authoritative `PRD.md`, current `PROGRESS.md`, repository implementation/test inventory, and live SQLite schema. Phase 1 and every strictly ordered PRD-authorized Phase 2 vertical slice remain complete: (1) authorization-scoped status/user statistics, (2) due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachment expansion, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD has no Phase 3 scope and no unimplemented authorized slice was found.
- **Changed files:** `PROGRESS.md` only (this verified status record). No application source, SQLite schema/data, attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **82.477 seconds**. The successful suite includes Phase-1 acceptance, server-side authorization/input validation and legacy SQLite due-date migration, all Phase-2 API slices, and isolated local Chromium UI coverage for statistics, XLSX export, received-date calendar, and completed-date report calendar. JavaScript syntax and Python compilation checks also exited 0.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` exists; tables `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python/JavaScript source scans found no `TODO`, `FIXME`, or `NotImplemented` markers. Git metadata remains unavailable because this working directory is not a Git repository.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; browser coverage uses isolated local `127.0.0.1` Uvicorn servers. No external message, notification, or other external service was contacted.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused or full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 15:46:07 UTC)
- Re-read the authoritative `PRD.md`, inspected the current implementation, API/acceptance/browser coverage, and this status file. Phase 1 and every strictly ordered, PRD-authorized Phase 2 slice remain complete: (1) authorization-scoped status/user statistics, (2) due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments, (4) authorization-scoped formula-safe XLSX export, and (5) the completed-date report calendar. The PRD authorizes no Phase 3 work; no unimplemented authorized slice was found.
- **Changed files:** `PROGRESS.md` only (this verified status record). No application source, SQLite schema/data, private attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration was changed.
- Real verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **80.420 seconds**, including Phase-1 acceptance, Phase-2 server authorization/input validation and legacy SQLite migration coverage, and isolated local Chromium UI tests for statistics, notifications, attachments, XLSX export, received-date calendar, and completed-date reporting. JavaScript syntax and Python compilation checks also completed successfully (the chained command exited 0).
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks` contains additive `due_date`; Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` are present. Python/JavaScript source scan found **0** `TODO`, `FIXME`, or `NotImplemented` markers. `git status --short` remains unavailable because this directory is not a Git repository.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; the verified browser suite starts only isolated local `127.0.0.1` Uvicorn servers. No external notification, message, or service was contacted.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 16:05:07 UTC)
- Re-read the authoritative `PRD.md`, current implementation, tests, and this progress record. Phase 1 and all five strictly ordered, PRD-authorized Phase 2 vertical slices remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD defines no Phase 3 scope and no incomplete authorized item was found.
- **Changed files:** `PROGRESS.md` only (this verified status entry). No product source, SQLite schema/data, private attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration was changed.
- Real verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **81.841 seconds**. The suite includes Phase-1 acceptance, server-side authorization/input validation, legacy SQLite migration coverage, and isolated local Chromium UI coverage for the Phase-2 surfaces; JavaScript syntax and Python compilation checks completed successfully in the same zero-exit command chain.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` exists; Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python/JavaScript incomplete-marker scan found no `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; browser coverage uses only isolated local `127.0.0.1` Uvicorn servers. No external notification, message, or other external service was contacted. Git metadata remains unavailable because this directory is not a Git repository.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 16:35:21 UTC)
- Re-read authoritative `PRD.md`, this progress record, current backend/frontend implementation, and focused API/browser test inventory. Phase 1 and all five strictly ordered, PRD-authorized Phase 2 slices remain implemented: (1) authorization-scoped status/user statistics, (2) due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. No Phase 3 scope is authorized and no incomplete marker or authorized slice was found.
- **Changed files:** `PROGRESS.md` only (this verified status entry). No application source, SQLite schema/data, private attachment, notification preference/outbox, deployment, credential, or external-service configuration changed.
- Real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v` **PASS** — all **25 tests** passed in **82.797 seconds**, including Phase-1 acceptance, Phase-2 server authorization/input validation and migration coverage, and isolated local Chromium UI flows. `node --check web/app.js` and `python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py` also succeeded. The combined diagnostic chain ended non-zero only because `git status --short` correctly reported that this directory is not a Git repository.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` exists; Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python/JavaScript source scans found no `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; automated browser coverage uses isolated local `127.0.0.1` Uvicorn servers. No external notification, message, or external service was contacted.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 16:38:53 UTC)
- Re-read the authoritative `PRD.md`, this status record, and the current implementation/test inventory. Phase 1 and all five strictly ordered Phase-2 slices remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with safe local-only in-app notification preferences/outbox, (3) private document/video attachments, (4) authorization-scoped formula-safe XLSX export, and (5) the completed-date report calendar. The PRD authorizes no Phase 3 scope, and no unimplemented authorized slice or incomplete implementation marker was found.
- **Changed files:** `PROGRESS.md` only (this verified status entry). No application source, SQLite schema/data, attachment content, notification preference/outbox, deployment, credential, or external-service configuration changed.
- Real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **80.362 seconds**. This exercised Phase-1 acceptance, server-side authorization/input validation and migration coverage, and isolated local Chromium UI flows for every Phase-2 surface. JavaScript syntax and Python compilation checks completed successfully in the same zero-exit command chain.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks` contains additive `due_date`; all Phase-2 tables (`task_attachments`, `notification_preferences`, and `notification_outbox`) exist. Python/JavaScript source scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers. `git status --short` remains unavailable because this directory is not a Git repository.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; the automated browser tests use isolated local `127.0.0.1` Uvicorn servers. No external message, notification, or other external service was contacted.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future source/user changes and run focused/full regression as warranted; do not invent Phase 3, alter deployment/product data, expose credentials, or enable external notification delivery without explicit approval.

## Latest Scheduled Verification (2026-08-01 16:43:29 UTC)
- Re-read authoritative `PRD.md`, inspected the current backend/frontend implementation and automated coverage, and scanned Python/JavaScript sources for incomplete markers. Phase 1 and every strictly ordered, PRD-authorized Phase-2 slice remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments, (4) authorization-scoped, formula-safe XLSX export, and (5) completed-date report calendar. The PRD has no authorized Phase-3 work, so no unimplemented roadmap slice exists.
- **Changed files:** `PROGRESS.md` only (this verified status record). No application source, SQLite schema/data, attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration was changed.
- Real verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v`: **PASS** — all **25 tests** passed in **80.538 seconds**, including Phase-1 acceptance, server-side authorization/input validation, legacy SQLite migration coverage, and isolated local Chromium UI tests for Phase-2 statistics, notifications, document/video attachments, XLSX export, received-date calendar, and completed-date report calendar. `node --check web/app.js` and `python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py` also passed (both exit code 0).
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` exists; Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python/JavaScript source scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers. `git status --short` cannot report changes because this directory is not a Git repository.
- Safety evidence: notifications remain `IN_APP_OUTBOX_ONLY`; browser verification uses isolated local `127.0.0.1` Uvicorn servers. No external notification, message, or external service was contacted.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 16:51:14 UTC)
- Re-read authoritative `PRD.md`, current `PROGRESS.md`, backend implementation/API tests, and rendered-browser coverage. Phase 1 and all five strictly ordered, PRD-authorized Phase-2 slices remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments, (4) authorization-scoped, formula-safe XLSX export, and (5) completed-date report calendar. The PRD defines no Phase 3 scope; no incomplete authorized roadmap slice was found.
- **Changed files:** `PROGRESS.md` only (this verified status entry). No application source, SQLite schema/data, attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...SQLite schema inspection..."`: **PASS** — all **25 tests** passed in **80.083 seconds**. JavaScript syntax and Python compilation checks succeeded; live schema inspection confirmed `backend/calendar.db` is **122,880 bytes**, `tasks.due_date` exists, and `task_attachments`, `notification_preferences`, and `notification_outbox` are present.
- Python/JavaScript scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers. The notification behavior tested is `IN_APP_OUTBOX_ONLY`; browser coverage uses isolated local `127.0.0.1` Uvicorn servers. No external notification, message, or other service was contacted. `git status --short` remains unavailable because this directory is not a Git repository.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 17:02:18 UTC)
- Re-read authoritative `PRD.md`, this progress record, current backend/frontend implementation, and API/browser coverage. Phase 1 and all five strictly ordered Phase-2 slices remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with safe local-only notification preferences/outbox, (3) private document/video attachments, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD authorizes no Phase 3 scope; no incomplete authorized item was found.
- **Changed files:** `PROGRESS.md` only (this verified status record). No product source, SQLite schema/data, private attachment content, notification preferences/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...SQLite schema inspection..."`: **PASS** — all **25 tests** passed in **81.607 seconds**; JavaScript syntax and Python compilation checks passed in the same zero-exit command chain. Coverage included Phase-1 acceptance, authorization/input validation and migration coverage, plus isolated local Chromium UI flows for all Phase-2 surfaces.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` exists; Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python/JavaScript scans found no `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; browser tests use only isolated local `127.0.0.1` Uvicorn servers. No external notification, message, or other external service was contacted. Git metadata remains unavailable because this directory is not a Git repository.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 17:48:24 UTC)
- Re-read authoritative `PRD.md`, this progress record, backend/frontend implementation, and API/browser test coverage. Phase 1 and all five strictly ordered, PRD-authorized Phase 2 vertical slices remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD defines no Phase-3 scope; no incomplete authorized item was found.
- **Changed files:** `PROGRESS.md` only (this verification record). No product source, SQLite schema/data, private attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **81.638 seconds**. The suite covered Phase-1 acceptance; Phase-2 server-side authorization, input validation, and migration behavior; and isolated local Chromium UI flows. JavaScript syntax and Python compilation checks completed successfully in the same zero-exit command chain.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks` contains additive `due_date`; Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` are present. Python/JavaScript source scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers. Git metadata remains unavailable because this directory is not a Git repository.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; browser coverage uses only isolated local `127.0.0.1` Uvicorn servers. No external notification, message, or other external service was contacted.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 19:16:19 UTC)
- Re-read authoritative `PRD.md`, current implementation/tests, and this progress record. Phase 1 and all strictly ordered PRD-authorized Phase-2 vertical slices remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD defines no Phase-3 scope and no incomplete authorized item was found.
- **Changed files:** `PROGRESS.md` only (this verified status record). No application source, SQLite schema/data, private attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **25 tests** passed in **80.525 seconds**, including Phase-1 acceptance, Phase-2 server-side authorization/input validation and legacy SQLite migration coverage, and isolated local Chromium UI flows. JavaScript syntax and Python compilation checks completed successfully in the same zero-exit command chain.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` exists; Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python/JavaScript incomplete-marker scan found no `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; browser coverage uses isolated local `127.0.0.1` Uvicorn servers. No external notification, message, or other external service was contacted.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 20:35:28 UTC)
- Re-read authoritative `PRD.md`, this progress record, the current implementation and automated coverage, then scanned Python/JavaScript sources for incomplete-work markers. Phase 1 and every strictly ordered, PRD-authorized Phase 2 vertical slice remain complete: (1) authorization-scoped status/user statistics, (2) due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD authorizes no Phase 3 work; no incomplete authorized slice was found.
- **Changed files:** `PROGRESS.md` only (this verified status record). No application source, SQLite schema/data, attachment content, notification preferences/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...SQLite schema inspection..."`: **PASS** — all **25 tests** passed in **81.872 seconds**. The suite exercised Phase-1 acceptance, Phase-2 server-side authorization/input validation and SQLite migration coverage, plus isolated local Chromium UI flows. JavaScript syntax and Python compilation checks passed in the same zero-exit chain.
- Live SQLite inspection confirmed `backend/calendar.db` is **122,880 bytes**; additive `tasks.due_date` and Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` are present. Python/JavaScript scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: notifications remain `IN_APP_OUTBOX_ONLY`; no external notification, message, or service was contacted. **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or alter production, existing data, credentials, deployment, or external-notification delivery without explicit approval.

## Latest Scheduled Verification (2026-08-01 22:34:25 UTC)
- Inspected authoritative `PRD.md`, current implementation/tests, and `PROGRESS.md`. Phase 1 and all five Phase-2 slices remain complete in the required order: (1) authorization-scoped status/user statistics, (2) due dates with safe local-only in-app notification preferences/outbox, (3) private document/video attachments, (4) authorization-scoped, formula-safe XLSX export, and (5) completed-date report calendar. The PRD provides no Phase-3 scope; no incomplete authorized item was found.
- **Changed files:** `PROGRESS.md` only (this verification entry). No application source, SQLite schema/data, attachment content, notification preferences/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...SQLite schema inspection..."`: **PASS** — all **25 tests** passed in **81.189 seconds**. This includes Phase-1 acceptance, Phase-2 authorization/input validation and legacy SQLite migration coverage, and isolated local Chromium UI flows for statistics, notifications, attachments, XLSX export, received-date calendar, and completed-date report calendar. JavaScript syntax and Python compilation checks completed successfully in the same zero-exit command chain.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` exists; `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python and JavaScript incomplete-marker scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers. `git status --short` remains unavailable because this directory is not a Git repository.
- Safety evidence: notifications remain `IN_APP_OUTBOX_ONLY`; test servers were isolated local `127.0.0.1` Uvicorn instances. No external notification, message, or other service was contacted. **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or alter production, existing data, credentials, deployment, or external-notification delivery without explicit approval.

## Latest Scheduled Verification (2026-08-01 22:50:10 UTC — Seoul calendar timezone correction)
- Re-read authoritative `PRD.md`, implementation/tests, and this status record. All five strictly ordered, PRD-authorized Phase-2 slices remain complete; the PRD defines no Phase-3 scope. A Phase-1/2 conformance bug was found in the responsive calendar controls: browser-side `Date#toISOString()` could move the Korean (`Asia/Seoul`) operational or completed-date calendar to the preceding UTC month, and could show the preceding day as a new task's default received date.
- **Changed files:** `web/app.js` now derives default dates/months explicitly in `Asia/Seoul`, calculates month length in UTC-safe calendar arithmetic, and advances both received-date and completed-date report calendars with timezone-independent `YYYY-MM` math. `backend/test_browser_ui.py` adds an isolated Chromium regression in an `Asia/Seoul` browser context covering June ↔ July navigation for both protected calendars and the Seoul-date helper. `PROGRESS.md` records this verified correction. No SQLite schema/data, attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration changed.
- Focused rendered-browser evidence: `python -m unittest backend.test_browser_ui.BrowserUiRegressionTests.test_calendar_month_navigation_is_safe_in_the_product_seoul_timezone -v`: **PASS** — 1 test in **6.892 seconds**. It exercised protected `/api/calendar` and `/api/completed-calendar` navigation in a Chromium `Asia/Seoul` context without page errors.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **26 tests** passed in **89.395 seconds**; JavaScript syntax and Python compilation checks passed in the same zero-exit chain. Live SQLite inspection preserved `backend/calendar.db` at **122,880 bytes** with additive `tasks.due_date` and the Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` present. `git status` remains unavailable because this directory is not a Git repository.
- Safety evidence: notifications remain `IN_APP_OUTBOX_ONLY`; browser tests used isolated local `127.0.0.1` Uvicorn servers. No external notification, message, or other service was contacted. **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-01 23:47:55 UTC)
- Re-read authoritative `PRD.md`, the implementation/test inventory, and this progress record. Phase 1 and all five strictly ordered, PRD-authorized Phase 2 vertical slices remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD provides no Phase 3 scope; no incomplete authorized item or implementation marker was found.
- **Changed files:** `PROGRESS.md` only (this verified status record). No application source, SQLite schema/data, attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...SQLite schema inspection..."`: **PASS** — all **26 tests** passed in **88.665 seconds**. This includes Phase-1 acceptance; Phase-2 server-side authorization, input validation, legacy SQLite migration coverage; and isolated local Chromium UI flows for statistics, notifications, attachments, XLSX export, received-date calendar, and completed-date report calendar. JavaScript syntax and Python compilation checks completed in the same zero-exit chain.
- Live SQLite inspection: `backend/calendar.db` is **122,880 bytes**; `tasks.due_date` exists; Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python/JavaScript source scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers. `git status` was not invoked; the existing record states this directory is not a Git repository.
- Safety evidence: notifications remain `IN_APP_OUTBOX_ONLY`; browser tests used only isolated local `127.0.0.1` Uvicorn servers. No external notification, message, or other service was contacted. **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-02 02:20:43 UTC — Phase 2 in-app reminder freshness correction)
- Re-read authoritative `PRD.md`, current backend/frontend/test sources, and this progress record. All five Phase-2 slices remain complete in the required order; no Phase-3 scope is authorized. During notification-slice inspection, a correctness gap was found: a local in-app due reminder contains a task description but could retain old text after an authorized description update.
- **Changed files:** `backend/main.py`, `backend/test_main.py`, and `PROGRESS.md`. `PATCH /api/tasks/{id}` now invalidates a task's private local outbox entries when notification-visible task data changes (description, due date, status, or assignees). The recipient's next authenticated notifications read lazily regenerates only eligible current reminders. This does not alter schema or existing task data, and it never invokes external delivery.
- Focused API evidence: `python -m unittest test_main.CalendarApiTests.test_due_dates_local_notification_outbox_preferences_and_authorization -v` (from `backend`) **PASS** — 1 test in **3.449 seconds**. It marked a due-today reminder read, changed the task description, then verified a single unread local reminder was regenerated with the new description.
- Full real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...SQLite schema inspection..."`: **PASS** — all **26 tests** passed in **87.544 seconds**; JavaScript syntax and Python compilation checks exited 0. This includes Phase-1 acceptance, Phase-2 authorization/validation/migration coverage, and isolated local Chromium UI coverage.
- Live SQLite inspection: `backend/calendar.db` remains **122,880 bytes**; `tasks.due_date` and tables `task_attachments`, `notification_preferences`, and `notification_outbox` are present. Python/JavaScript scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers. `git status --short` confirms Git metadata is unavailable because this directory is not a repository.
- Safety evidence: notifications remain `IN_APP_OUTBOX_ONLY`; no external notification, message, or service was contacted. **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Development (2026-08-02 03:03:59 UTC — Phase 2 attachment expansion conformance completion)
- Re-read authoritative `PRD.md`, source, tests, and this record. The Phase-2 attachment-expansion wording in PRD §2.2 also requires **image editing**; the previous implementation had document/video expansion but explicitly deferred image editing. Completed that remaining part of the already-ordered third Phase-2 slice without creating Phase 3 work.
- **Changed files:** `backend/main.py`, `backend/test_main.py`, `backend/test_browser_ui.py`, `web/app.js`, `web/style.css`, `requirements.txt`, `README.md`, and `PROGRESS.md`.
- Added a responsive left/right 90° image-rotation control for task images and `POST /api/tasks/{task_id}/images/{image_id}/edit`. The server enforces the existing task-level authorization and first-password-change requirement, validates a fixed direction enum, decodes only private JPEG/PNG/WEBP within a 40-million-pixel limit, strips metadata on re-encode, validates the derivative signature/10MB ceiling, keeps it outside the static web root with private permissions, and records `TASK_IMAGE_EDITED` audit/history entries. No external service is called.
- Added the additive, idempotent `task_image_edits` SQLite migration. Each rotation records the prior private storage key and replaces only the current presentation revision; all prior image source files remain private and are removed only when the user deliberately deletes that image. The live product migration completed successfully: `backend/calendar.db` changed only for the additive schema from **122,880** to **135,168 bytes**; `task_image_edits` and `idx_task_image_edits_image_created` exist. No task, user, attachment, notification preference/outbox, credential, or deployment data was changed.
- Focused evidence: `python -m unittest test_main.CalendarApiTests.test_private_image_rotation_is_authorized_non_destructive_and_audited test_main.CalendarApiTests.test_due_date_column_migrates_a_preexisting_sqlite_tasks_table -v` **PASS** — 2 tests in **4.109 seconds**. The API test proves a nonparticipant receives 403, invalid direction receives 422, an authorized user gets a 2×3→3×2 private derivative, source provenance is retained, audit/history is written, and deliberate image deletion removes every private revision. `python -m unittest test_browser_ui.BrowserUiRegressionTests.test_admin_task_detail_edit_history_private_preview_and_delete_confirmation_ui -v` **PASS** — 1 rendered Chromium test in **8.870 seconds**, including the confirmation-controlled rotation UI and 200 API response.
- Full verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python - <<'PY' ...`: **PASS** — all **27 tests** passed in **91.749 seconds**; JavaScript syntax and Python compilation checks passed in the same zero-exit chain. Live schema inspection confirmed the new image-revision columns (`id,task_id,image_id,source_storage_key,result_storage_key,direction,edited_by,created_at`), its index, and the existing Phase-2 tables. Python/JavaScript scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety: browser tests used only isolated local `127.0.0.1` Uvicorn processes. Notification behavior remains `IN_APP_OUTBOX_ONLY`; no email/SMS/messenger, external service, production deployment, or credential operation occurred. Git metadata is unavailable because this directory is not a Git repository.
- **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or make production, existing-data, credential, deployment, or external-notification changes without explicit approval.

## Latest Scheduled Verification (2026-08-02 04:39:12 UTC)
- Re-read authoritative `PRD.md`, current `PROGRESS.md`, backend/frontend implementation, and automated test inventory. Phase 1 and every strictly ordered, PRD-authorized Phase-2 vertical slice remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments plus image editing, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD provides no Phase-3 scope and no incomplete authorized slice was found.
- **Changed files:** `PROGRESS.md` only (this verification entry). No application source, SQLite schema/data, attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...SQLite schema inspection..."`: **PASS** — all **27 tests** passed in **91.363 seconds**. This covered Phase-1 acceptance; Phase-2 server-side authorization, input validation, SQLite migration behavior, and isolated local Chromium UI flows. JavaScript syntax and Python compilation checks completed successfully in the same zero-exit command chain.
- Live SQLite inspection: `backend/calendar.db` is **135,168 bytes**; `tasks.due_date` exists; tables `task_attachments`, `notification_preferences`, `notification_outbox`, and `task_image_edits` exist. Python/JavaScript source scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers. Git status remains unavailable because this directory is not a Git repository.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; no external notification, message, or other service was contacted. **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or alter production, existing data, credentials, deployment, or external-notification delivery without explicit approval.

## Latest Scheduled Verification (2026-08-02 04:56:00 UTC)
- Re-read authoritative `PRD.md`, current `PROGRESS.md`, backend/frontend implementation, test inventory, and incomplete-work markers. Phase 1 and all five strictly ordered, PRD-authorized Phase-2 vertical slices remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments plus image editing, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD provides no Phase-3 scope, so no unimplemented authorized slice exists.
- **Changed files:** `PROGRESS.md` only (this verified status record). No application source, SQLite schema/data, attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration was changed.
- Real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py`: **PASS** — all **27 tests** passed in **90.026 seconds**. This exercised Phase-1 acceptance, Phase-2 server-side authorization/input validation and migration behavior, and isolated local Chromium UI flows; JavaScript syntax and Python compilation checks completed successfully in the same zero-exit command chain.
- Live SQLite inspection: `backend/calendar.db` is **135,168 bytes**; `tasks.due_date` exists; Phase-2 tables `task_attachments`, `notification_preferences`, `notification_outbox`, and `task_image_edits` exist. Python/JavaScript source scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; no external notification, message, or other service was contacted. **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or alter production, existing data, credentials, deployment, or external-notification delivery without explicit approval.

## Latest Scheduled Verification (2026-08-02 05:18:10 UTC)
- Re-read authoritative `PRD.md`, current `PROGRESS.md`, source/test inventory, and incomplete-work-marker scans. Phase 1 and all five strictly ordered, PRD-authorized Phase-2 vertical slices remain complete: (1) authorization-scoped status/user statistics, (2) due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments plus image editing, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD contains no Phase-3 scope, so no unimplemented authorized slice exists.
- **Changed files:** `PROGRESS.md` only (this verified status entry). No application source, SQLite schema/data, attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration was changed.
- Real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...SQLite schema inspection..."`: **PASS** — all **27 tests** passed in **92.436 seconds**; JavaScript syntax and Python compilation checks passed in the same zero-exit chain. Coverage includes Phase-1 acceptance, server-side authorization/input validation, legacy SQLite migration behavior, and isolated local Chromium UI flows.
- Live SQLite inspection: `backend/calendar.db` is **135,168 bytes**; `tasks.due_date` exists; Phase-2 tables `notification_outbox`, `notification_preferences`, `task_attachments`, and `task_image_edits` exist. Python/JavaScript scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: notification behavior remains `IN_APP_OUTBOX_ONLY`; no external notification, message, or other service was contacted. **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or alter production, existing data, credentials, deployment, or external-notification delivery without explicit approval.

## Latest Scheduled Verification (2026-08-02 06:24:04 UTC)
- Re-read authoritative `PRD.md`, current `PROGRESS.md`, backend/frontend implementation, test inventory, and incomplete-work-marker scans. Phase 1 and all five strictly ordered, PRD-authorized Phase-2 vertical slices remain complete: (1) authorization-scoped status/user statistics, (2) task due dates with notification preferences and safe local-only in-app outbox behavior, (3) private document/video attachments plus non-destructive image editing, (4) authorization-scoped formula-safe XLSX export, and (5) completed-date report calendar. The PRD defines no Phase-3 scope, so no unimplemented authorized slice exists.
- **Changed files:** `PROGRESS.md` only (this verified status record). No application source, SQLite schema/data, attachment content, notification preference/outbox, deployment setting, credential, or external-service configuration changed.
- Real verification from repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...SQLite schema inspection..."`: **PASS** — all **27 tests** passed in **91.033 seconds**. JavaScript syntax and Python compilation checks passed in the same zero-exit command chain. Coverage includes Phase-1 acceptance; Phase-2 server-side authorization/input validation and legacy SQLite migration behavior; and isolated local Chromium UI flows.
- Live SQLite inspection: `backend/calendar.db` is **135,168 bytes**; `tasks.due_date` exists; Phase-2 tables `task_attachments`, `notification_preferences`, and `notification_outbox` exist. Python/JavaScript scans found **0** `TODO`, `FIXME`, or `NotImplemented` markers.
- Safety evidence: notifications remain `IN_APP_OUTBOX_ONLY`; no external notification, message, or other service was contacted. **Remaining authorized roadmap:** none. **Blockers:** none. **Exact next priority:** inspect future PRD/source/user changes and run focused/full regression as warranted; do not invent Phase 3 or alter production, existing data, credentials, deployment, or external-notification delivery without explicit approval.

## Codex Execution PRD — Phase 1 slice (2026-08-06 08:31:52 UTC)
Completed:
- Read `docs/Codex_Execution_PRD_backend_refactoring.md` and this record before changes. Confirmed the starting `backend/main.py` was 1,724 lines, while `core/config.py`, `core/logging.py`, and encrypted `database.py` were already separated.
- Moved the unchanged FastAPI implementation to `backend/app/main.py` and replaced `backend/main.py` with a 16-line compatibility ASGI shim. Existing `import main`, `main:app`, and repository-root `backend.main:app` import styles resolve to the same implementation module, so API URLs and request/response contracts are unchanged.
- Preserved the pre-move backend-root static and private-upload paths after the move. The test-only legacy migration setup now creates a SQLCipher-backed legacy-shaped SQLite database instead of an unsupported plaintext database opened with an encryption key; it continues to assert the additive `due_date` migration and preserved legacy row.
- No database schema, live database data, DPAPI key, plaintext backup, secret, `.env`, private upload, API URL, request/response model, or application behavior was changed.

Modified Files:
- `backend/main.py` — minimal backward-compatible ASGI shim.
- `backend/app/main.py` — moved existing application implementation without endpoint logic changes; adjusted only module-import and original backend-root path resolution.
- `backend/test_main.py` — corrected encrypted SQLite migration fixture.
- `PROGRESS.md` — this verified phase record.

Tests:
- `python -m unittest test_acceptance.PhaseOneAcceptanceTests.test_phase_one_task_authorization_status_images_calendar_and_audit_acceptance -v` (from `backend`): PASS — 1 test in 7.576s.
- `python -m unittest test_main.CalendarApiTests.test_due_date_column_migrates_a_preexisting_sqlite_tasks_table -v` (from `backend`): PASS — 1 test in 1.027s.
- `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: PASS — all 27 tests in 108.491s; JavaScript syntax, Python compilation, and whitespace checks passed.
- Import verification: `import main` from `backend/` and `import backend.main` from repository root both expose `Shared Work Calendar MVP` with 44 routes.
- Git status was checked before and after verification; working changes are only the four files listed above (with `backend/app/main.py` new). No commit was made.

Risk:
- This is an entrypoint/physical-module move only; routers, service boundaries, repository SQL, middleware, exception handling, and schemas are still concentrated in `backend/app/main.py`. Completion conditions are not yet met.
- The working tree has uncommitted but fully verified source/test/progress changes. Do not commit database files, DPAPI key files, plaintext backups, secrets, or `.env` files.

Next Phase:
- Phase 2, next small slice: identify and extract one router group (starting with auth) behind the unchanged application instance, with no SQL in its router, then run focused auth and full regression coverage before updating this record.

## Codex Execution PRD — schema extraction slice (2026-08-06 08:37:14 UTC)
Completed:
- Extracted all existing Pydantic HTTP request models and their validators from `backend/app/main.py` into `backend/schemas/requests.py`. Validation text, constraints, defaults, PATCH omitted-vs-null behavior, and model names are preserved exactly; the application imports the same names for its existing endpoints.
- Added the target `backend/schemas/` package. This is an internal module-boundary move only: no API URL, request/response format, database schema/data, key material, secret, `.env`, private upload, external service, or notification behavior changed.
- `backend/main.py` remains 16 lines; `backend/app/main.py` is now 1,569 lines. Completion conditions remain unmet because endpoints still contain router/service/repository concerns and SQL.

Modified Files:
- `backend/app/main.py` — replaced inline request model definitions with schema imports.
- `backend/schemas/__init__.py` — package marker.
- `backend/schemas/requests.py` — moved Pydantic request schemas and validators.
- `PROGRESS.md` — this verified status entry.

Tests:
- Focused schema-boundary regression: `python -m unittest test_main.CalendarApiTests.test_first_login_requires_password_change_and_blocks_work_apis test_main.CalendarApiTests.test_admin_user_lifecycle_validation_authorization_and_last_admin_protection test_main.CalendarApiTests.test_task_list_server_filters_pagination_and_calendar_month_validation -v` (from `backend`): PASS — 3 tests in 6.827s.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: PASS — all 27 tests in 101.054s; JavaScript syntax, Python compilation, and whitespace checks passed.
- Git status verified before progress update; no commit was made. The working tree contains only `PROGRESS.md`, `backend/main.py`, `backend/app/main.py`, `backend/schemas/`, and `backend/test_main.py`; no database, DPAPI key, plaintext backup, secret, or `.env` file is staged or tracked by this work.

Risk:
- Service, repository, router, middleware, exception-handler, and response-helper separation are still pending. SQL remains outside repositories, so the PRD completion conditions are not met.
- The schema move relies on dual absolute/package import paths solely to preserve both established backend-directory and repository-root ASGI imports; both were verified earlier in this run.

Next Phase:
- Extract the auth endpoint group into a router backed by an auth service, preserving the existing application instance and all auth URLs/request/response behavior. Keep router SQL-free, run focused auth tests plus full regression, then update this record.

## Codex Execution PRD — auth router/service slice (2026-08-06 08:54:51 UTC)
Completed:
- Extracted the existing `POST /api/auth/login`, `POST /api/auth/logout`, and `GET /api/me` endpoint group into `backend/routers/auth.py`. The router performs HTTP request/dependency handling and delegates every operation to `AuthService`; it contains no SQL.
- Added `backend/services/auth_service.py`, preserving the established SQLCipher transaction provider, Argon2id/PBKDF2-on-login upgrade behavior, eight-hour in-memory session lifetime, exact Korean error response, audit events, authorization header parsing, and user response object.
- Registered the router on the same `FastAPI` application after the existing authentication dependency is defined. Import verification reports the unchanged application title and **44 routes**, including the same login, logout, and me method/path pairs.
- This is an internal boundary move only: no API URL, request/response shape, database schema/data, DB key/DPAPI file, upload, secret, `.env`, notification behavior, deployment, or external service changed.

Modified Files:
- `backend/app/main.py` — registers the extracted auth router and removes only the moved endpoint bodies.
- `backend/routers/__init__.py` and `backend/routers/auth.py` — router package and SQL-free auth endpoint boundary.
- `backend/services/__init__.py` and `backend/services/auth_service.py` — injected auth business service.
- `PROGRESS.md` — this verified status entry.

Tests:
- Focused existing authentication regression: `python -m unittest test_main.CalendarApiTests.test_first_login_requires_password_change_and_blocks_work_apis test_main.CalendarApiTests.test_argon2id_is_used_for_new_passwords_and_legacy_pbkdf2_upgrades_on_login test_main.CalendarApiTests.test_admin_user_lifecycle_validation_authorization_and_last_admin_protection -v` (from `backend`): **PASS** — 3 tests in **5.648s**. It exercised login failure/success, legacy password upgrade/audit, `/api/me`, and logout.
- Route/import and syntax verification: `python -m compileall -q app/main.py routers/auth.py services/auth_service.py main.py && python -c "import main; ..."` (from `backend`): **PASS** — application title unchanged, 44 routes, and `POST /api/auth/login`, `POST /api/auth/logout`, and `GET /api/me` remain registered.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** in **101.253s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- The `current_user` dependency and password-change route still remain in `backend/app/main.py`; User, Task, Dashboard, and Admin endpoint groups also remain monolithic. Repository extraction, global exception handling, response helpers, middleware, validators, and notification/scheduler layering are still pending, so PRD completion conditions are not met.
- The working tree contains only verified source/test/progress changes. No database, DPAPI/key, plaintext backup, upload, secret, or `.env` file is included.

Next Phase:
- Extract the user endpoint group as the next small vertical slice behind a SQL-free router and service, preserving all existing API behavior, then run focused user lifecycle/password tests and the full regression suite.

## Codex Execution PRD — user router/service slice (2026-08-06 09:12:33 UTC)
Completed:
- Extracted the unchanged user-account endpoint group into `backend/routers/users.py`: `GET /api/assignees`, `POST /api/me/password`, and `GET`/`POST`/`PATCH` `/api/admin/users`. The router handles only HTTP validation/dependencies and delegates to `UserService`; it contains no SQL.
- Added `backend/services/user_service.py`, preserving active-assignee selection, current-password verification, Argon2id hashing, forced password-change clearing, administrator-only lifecycle checks, last-active-admin protection, session invalidation after administrative credential/role/activation changes, exact Korean errors, and audit history.
- Registered the router on the same FastAPI application after the existing authentication/password-change/admin dependencies. Route verification confirms the application title remains `Shared Work Calendar MVP`, the route count remains **44**, and every moved method/path pair remains registered.
- This is an internal boundary move only: no API URL, request/response shape, database schema/data, DB key/DPAPI file, upload, secret, `.env`, notification behavior, deployment, or external service changed.

Modified Files:
- `backend/app/main.py` — registers the extracted user router and removes only the moved endpoint bodies.
- `backend/routers/users.py` — SQL-free HTTP boundary for the existing user endpoints.
- `backend/services/user_service.py` — injected user-account business service.
- `PROGRESS.md` — this verified status entry.

Tests:
- Focused user/auth/task-boundary regression: `python -m unittest test_main.CalendarApiTests.test_first_login_requires_password_change_and_blocks_work_apis test_main.CalendarApiTests.test_admin_user_lifecycle_validation_authorization_and_last_admin_protection test_main.CalendarApiTests.test_task_detail_update_history_and_deletion_authorization -v` (from `backend`): **PASS** — 3 tests in **7.217s**.
- Router contract and syntax verification: `python -m compileall -q app/main.py routers/users.py services/user_service.py main.py && python -c "...route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/users.py` (from `backend`): **PASS** — title unchanged, 44 routes, all five moved method/path pairs present, and no SQL/DB execution token in the router.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** in **108.654s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- Task, Dashboard, and Admin endpoint groups remain in `backend/app/main.py`. Repository extraction, global exception handling, response helpers, middleware, validators, notification layering, and scheduler separation remain pending, so the Codex Execution PRD completion conditions are not met.
- The working tree contains only verified source/progress changes from this slice; no database, DPAPI/key, plaintext backup, upload, secret, or `.env` file is included.

Next Phase:
- Extract the task endpoint group as the next small vertical slice behind a SQL-free router and task service, preserving all existing API behavior, then run focused task authorization/CRUD tests and the full regression suite.

## Codex Execution PRD — task read router/service slice (2026-08-06 09:30:41 UTC)
Completed:
- Extracted the unchanged `GET /api/tasks` and `GET /api/tasks/{task_id}` endpoints into `backend/routers/tasks.py`. The router retains request parsing and authentication/password-change dependencies only, delegates to `TaskService`, and has no SQL/DB execution token.
- Added `backend/services/task_service.py`, preserving the existing server-side task visibility scope, validation messages and status codes, filters, pagination, ordering, summary, detailed response view, and task-level direct-URL authorization behavior.
- Registered the extracted read routes after existing static task paths, preserving literal `/api/tasks/export.xlsx` precedence. Import verification confirms `Shared Work Calendar MVP`, the unchanged **44** routes, and registration of `GET /api/tasks`, `GET /api/tasks/{task_id}`, and `GET /api/tasks/export.xlsx`.
- This is an internal boundary move only: no API URL, request/response schema, database schema/data, DB key/DPAPI file, upload, secret, `.env`, notification behavior, deployment, or external service changed. `backend/main.py` remains **16** lines.

Modified Files:
- `backend/app/main.py` — imports/registers the extracted task-read router and removes only the moved endpoint bodies.
- `backend/routers/tasks.py` — SQL-free HTTP boundary for the existing task list/detail reads.
- `backend/services/task_service.py` — injected task-read business service.
- `PROGRESS.md` — this verified status entry.

Tests:
- Focused task regression: `python -m unittest test_main.CalendarApiTests.test_member_cannot_see_other_members_task test_main.CalendarApiTests.test_task_list_server_filters_pagination_and_calendar_month_validation test_main.CalendarApiTests.test_task_detail_update_history_and_deletion_authorization -v` (from `backend`): **PASS** — 3 tests in **8.295s**.
- Router contract and syntax verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py` (from `backend`): **PASS** — title unchanged, 44 routes, all three relevant GET routes present, and no SQL/DB execution token in the router.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** in **102.152s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- Task write/upload/history/calendar endpoints, Dashboard, and Admin endpoint groups remain in `backend/app/main.py`. Repository extraction, global exception handling, response helpers, middleware, validators, notification layering, and scheduler separation remain pending, so the Codex Execution PRD completion conditions are not met.
- The working tree contains only verified source/progress changes from this slice; no database, DPAPI/key, plaintext backup, upload, secret, or `.env` file is included.

Next Phase:
- Continue the task endpoint group in a small, behavior-preserving write or attachment slice behind the same SQL-free router/service boundary, then run focused task tests and the full regression suite.

## Codex Execution PRD — task create router/service slice (2026-08-06 09:50:09 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. The completion conditions remain unmet: task write/upload/history/calendar endpoints, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `POST /api/tasks` endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated its operation to `TaskService.create_task`.
- Preserved task request validation, status code **201**, Seoul-date defaults (including test-time dynamic calendar binding), due-date validation, active-assignee validation, reusable contact/master-record behavior, transactional task/assignee writes, audit event/data, and task response view. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification behavior, deployment, and external-service behavior did not change.
- Route/import verification confirms the title is still `Shared Work Calendar MVP`, the route count remains **44**, and `POST /api/tasks` remains registered. The task router has no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved task-create endpoint body and supplies existing helpers to `TaskService`.
- `backend/routers/tasks.py` — adds the existing task-create HTTP endpoint with unchanged dependency and status-code behavior.
- `backend/services/task_service.py` — adds the injected task-create business operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused evidence (separate isolated invocations to honor the test modules' documented DB isolation ordering): `python -m unittest test_main.CalendarApiTests.test_automatic_task_dates_use_the_asia_seoul_calendar_date -v`: **PASS** — 1 test in **1.087s**; and `python -m unittest test_acceptance.PhaseOneAcceptanceTests.test_phase_one_task_authorization_status_images_calendar_and_audit_acceptance -v`: **PASS** — 1 test in **4.934s**. Together these verify automatic Seoul dates and the complete task create/authorization/CRUD acceptance workflow.
- Route/static boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...POST /api/tasks route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, POST route registration, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **92.889s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` currently contains repository SQL as an intentional intermediate Phase-3 boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Only the four source/progress files listed above are modified. No database, DPAPI/key file, plaintext backup, private upload, secret, or `.env` is included.

Next Phase:
- Continue the task group with one small behavior-preserving write/history/calendar or attachment slice behind the existing SQL-free router/service boundary, then run focused task coverage and the full regression suite.

## Codex Execution PRD — task update router/service slice (2026-08-06 10:07:45 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task upload/history/calendar endpoints, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `PATCH /api/tasks/{task_id}` endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated its operation to `TaskService.update_task`.
- Preserved task-level access scope; member creator-only received-date protection; due/completed-date behavior; active-assignee validation; reusable-contact handling; transactions; notification-outbox invalidation; task view; audit payload/event; error status/text; and request client IP handling. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still has 44 routes and registers exactly one extracted PATCH task route. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved task-update endpoint body and supplies the existing task-change helper to `TaskService`.
- `backend/routers/tasks.py` — adds the existing PATCH task HTTP endpoint with unchanged dependency behavior.
- `backend/services/task_service.py` — adds the injected task-update business operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused regression: `python -m unittest test_main.CalendarApiTests.test_task_detail_update_history_and_deletion_authorization test_main.CalendarApiTests.test_due_dates_local_notification_outbox_preferences_and_authorization test_acceptance.PhaseOneAcceptanceTests.test_phase_one_task_authorization_status_images_calendar_and_audit_acceptance -v` (from `backend`): **PASS** — 3 tests in **11.049s**.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...route assertions..." && git diff --check` (from `backend`): **PASS** — unchanged title/44-route contract and PATCH route registration confirmed. A separate router source token check also passed with no SQL/DB execution token.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **91.856s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Only the verified source/progress files named above will be committed. `backend/calendar.db` and detected plaintext DB backups are ignored and will not be added; no DPAPI/key file, private upload, secret, or `.env` is included.

Next Phase:
- Continue the task group with the smallest remaining behavior-preserving endpoint slice (delete, history/calendar, or one attachment operation) behind the existing SQL-free router/service boundary, then run focused task coverage and the full regression suite.

## Codex Execution PRD — task delete router/service slice (2026-08-06 10:24:36 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task upload/history/calendar endpoints, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `DELETE /api/tasks/{task_id}` endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated soft deletion to `TaskService.delete_task`.
- Preserved the administrator-only dependency (including forced first-password change), task existence/access behavior, soft-delete fields, private local notification-outbox cleanup, audit event/payload/client IP, response status and `{\"ok\": true}` schema. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still has 44 routes and registers `DELETE /api/tasks/{task_id}`. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved task-delete endpoint body and injects the existing administrator dependency into the task router.
- `backend/routers/tasks.py` — adds the unchanged DELETE task HTTP endpoint with existing dependency behavior.
- `backend/services/task_service.py` — adds the injected task soft-delete business operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused deletion regression: `python -m unittest test_main.CalendarApiTests.test_task_detail_update_history_and_deletion_authorization -v` (from `backend`): **PASS** — 1 test in **3.732s**. It verifies member deletion is forbidden, administrator soft deletion succeeds, and later task retrieval is 404.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, DELETE route registration, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **93.761s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Only verified source/progress files are modified. `git status --short --untracked-files=all` lists `backend/app/main.py`, `backend/routers/tasks.py`, and `backend/services/task_service.py` before this progress update; no database, DPAPI/key file, plaintext backup, private upload, secret, or `.env` is included.

Next Phase:
- Continue the task group with the smallest remaining behavior-preserving endpoint slice (history or calendar read) behind the existing SQL-free router/service boundary, then run focused task coverage and the full regression suite.

## Codex Execution PRD — task history router/service slice (2026-08-06 10:41:10 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task calendar and file endpoints, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/tasks/{task_id}/history` endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated it to `TaskService.get_task_history`.
- Preserved first-password-change enforcement, task-level authorization, audit-history query/order, decoded before/after payloads, changed-field labels, error status/text, and response schema. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still has 44 routes and registers exactly one extracted GET task-history route. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved task-history endpoint body and supplies the existing history helper to `TaskService`.
- `backend/routers/tasks.py` — adds the unchanged GET task-history HTTP endpoint with existing dependency behavior.
- `backend/services/task_service.py` — adds the injected task-history business operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused regression: `python -m unittest test_main.CalendarApiTests.test_task_detail_update_history_and_deletion_authorization test_main.CalendarApiTests.test_due_dates_local_notification_outbox_preferences_and_authorization test_acceptance.PhaseOneAcceptanceTests.test_phase_one_task_authorization_status_images_calendar_and_audit_acceptance -v` (from `backend`): **PASS** — 3 tests in **11.152s**. This covers history authorization, updated audit-field history, due-date history, and Phase-1 direct-URL authorization behavior.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...route assertions..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, task-history route registration, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **93.940s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Only verified source/progress files are modified. `backend/calendar.db` and detected plaintext DB backups are ignored and will not be added; no DPAPI/key file, private upload, secret, or `.env` is included.

Next Phase:
- Continue the task group with the smallest remaining behavior-preserving endpoint slice (received-date calendar read) behind the existing SQL-free router/service boundary, then run focused task coverage and the full regression suite.

## Codex Execution PRD — task received-date calendar router/service slice (2026-08-06 10:57:10 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task file endpoints, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/calendar` received-date calendar endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated it to `TaskService.get_received_date_calendar`.
- Preserved first-password-change enforcement, strict `YYYY-MM` validation and error text, month-boundary calculation, authorization-scoped non-deleted task query, received-date ordering, and the response list schema including all three live statuses. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still has **44** routes and registers exactly one `GET /api/calendar` route. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved received-date calendar endpoint body.
- `backend/routers/tasks.py` — adds the unchanged calendar HTTP endpoint with existing dependency behavior.
- `backend/services/task_service.py` — adds the injected calendar business operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused regression: `python -m unittest test_main.CalendarApiTests.test_task_list_server_filters_pagination_and_calendar_month_validation test_acceptance.PhaseOneAcceptanceTests.test_phase_one_task_authorization_status_images_calendar_and_audit_acceptance -v` (from `backend`): **PASS** — 2 tests in **7.248s**. This verifies invalid-month rejection, all three received-date calendar statuses, authorization scope, and the Phase-1 calendar acceptance workflow.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...calendar route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one calendar route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **92.882s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Only verified source/progress files are modified. No database, DPAPI/key file, plaintext backup, private upload, secret, or `.env` is included.

Next Phase:
- Continue the task group with the smallest remaining behavior-preserving file-endpoint slice behind the existing SQL-free router/service boundary, then run focused task coverage and the full regression suite.

## Codex Execution PRD — task image-download router/service slice (2026-08-06 11:12:59 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: remaining task file endpoints, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/tasks/{task_id}/images/{image_id}` private-image endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated it to `TaskService.get_task_image`.
- Preserved first-password-change enforcement, task-level authorization before image lookup, image/task matching, both established Korean 404 messages, private path traversal guard, file-existence handling, original media type, and `Cache-Control: private, no-store` / `X-Content-Type-Options: nosniff` response headers. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still has **44** routes and registers exactly one `GET /api/tasks/{task_id}/images/{image_id}` route. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved private-image endpoint body and supplies the existing private-image path helper to `TaskService`.
- `backend/routers/tasks.py` — adds the unchanged image-download HTTP endpoint with existing dependency behavior.
- `backend/services/task_service.py` — adds the injected authorized image-download operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused image regression: `python -m unittest test_main.CalendarApiTests.test_private_image_upload_validation_authorization_and_deletion test_main.CalendarApiTests.test_private_image_rotation_is_authorized_non_destructive_and_audited test_acceptance.PhaseOneAcceptanceTests.test_phase_one_task_authorization_status_images_calendar_and_audit_acceptance -v` (from `backend`): **PASS** — 3 tests in **9.958s**. This covers private image access authorization, upload validation, metadata, image deletion, non-destructive rotation, audit events, and Phase-1 direct-URL authorization behavior.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...route assertions..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one image-download route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **93.245s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Only verified source/progress files are modified. `git status --short --untracked-files=all` lists only `backend/app/main.py`, `backend/routers/tasks.py`, and `backend/services/task_service.py` before this progress update; no database, DPAPI/key file, plaintext backup, private upload, secret, or `.env` is included.

Next Phase:
- Continue the task group with the smallest remaining behavior-preserving file-endpoint slice (image edit or delete) behind the existing SQL-free router/service boundary, then run focused task coverage and the full regression suite.

## Codex Execution PRD — task image-delete router/service slice (2026-08-06 11:29:54 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: remaining task file endpoints, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `DELETE /api/tasks/{task_id}/images/{image_id}` private-image deletion endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated it to `TaskService.delete_task_image`.
- Preserved first-password-change enforcement, task-level authorization, image/task matching, the established Korean 404 message, private source-revision cleanup after a committed deletion, image metadata redaction in the audit event, client IP handling, and the `{\"ok\": true}` response schema. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still has **44** routes and registers exactly one `DELETE /api/tasks/{task_id}/images/{image_id}` route. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved private-image deletion endpoint body and supplies the existing image metadata helper to `TaskService`.
- `backend/routers/tasks.py` — adds the unchanged DELETE image HTTP endpoint with existing dependency behavior.
- `backend/services/task_service.py` — adds the injected authorized image-deletion operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused image regression: `python -m unittest test_main.CalendarApiTests.test_private_image_upload_validation_authorization_and_deletion test_main.CalendarApiTests.test_private_image_rotation_is_authorized_non_destructive_and_audited test_acceptance.PhaseOneAcceptanceTests.test_phase_one_task_authorization_status_images_calendar_and_audit_acceptance -v` (from `backend`): **PASS** — 3 tests in **9.964s**. This covers deletion authorization, 404 after deletion, image-upload/deletion audit events, and deletion of both current and retained source-revision files.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one image-delete route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **94.785s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- `git status --short --untracked-files=all` listed only the three verified source files before this progress update. No database, DPAPI/key file, plaintext backup, private upload, secret, or `.env` is included.

Next Phase:
- Continue the task group with the smallest remaining behavior-preserving file-endpoint slice (image edit) behind the existing SQL-free router/service boundary, then run focused task coverage and the full regression suite.

## Codex Execution PRD — task image-edit router/service slice (2026-08-06 11:48:16 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task image-upload and attachment endpoints, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `POST /api/tasks/{task_id}/images/{image_id}/edit` private-image revision endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated it to `TaskService.edit_task_image`.
- Preserved first-password-change enforcement, task-level authorization before private-file access, Pydantic direction validation, both established Korean 404 messages, safe local rotation, unique private derivative storage, 0700 parent / best-effort 0600 file permissions, non-destructive source revision tracking, atomic SQL transaction behavior, cleanup on failure, metadata redaction, audit payload/event/client IP, and the `{image, direction, non_destructive}` response schema. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still has **44** routes and registers exactly one `POST /api/tasks/{task_id}/images/{image_id}/edit` route. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved private-image edit endpoint body and supplies existing rotation/suffix helpers to `TaskService`.
- `backend/routers/tasks.py` — adds the unchanged image-edit HTTP endpoint with existing dependency behavior.
- `backend/services/task_service.py` — adds the injected authorized non-destructive image-edit operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused image regression: `python -m unittest test_main.CalendarApiTests.test_private_image_rotation_is_authorized_non_destructive_and_audited test_main.CalendarApiTests.test_private_image_upload_validation_authorization_and_deletion test_acceptance.PhaseOneAcceptanceTests.test_phase_one_task_authorization_status_images_calendar_and_audit_acceptance -v` (from `backend`): **PASS** — 3 tests in **9.854s**. This covers direct-URL authorization, invalid edit direction validation, private rotation, non-destructive source retention, image metadata redaction, audit events, and Phase-1 image authorization behavior.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check && python -c "...route assertions..."` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one image-edit route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **95.170s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified source files. A tracked sensitive-file scan found no database, DPAPI/key, certificate, `.env`, or private-upload path; none is included.

Next Phase:
- Continue the task group with the smallest remaining behavior-preserving file-endpoint slice (image upload or one attachment operation) behind the existing SQL-free router/service boundary, then run focused task coverage and the full regression suite.

## Codex Execution PRD — task image-upload router/service slice (2026-08-06 12:06:28 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: attachment endpoints, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `POST /api/tasks/{task_id}/images` private-image upload endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated it to `TaskService.upload_task_images`.
- Preserved first-password-change enforcement, authorization before private file writes, 1–5 request limit, 10MB per-file limit, MIME/signature validation, five-images-per-task limit and DB-trigger translation, private storage paths, filename sanitization, 0700 parent / best-effort 0600 file permissions, atomic transaction and cleanup-on-failure behavior, metadata redaction, audit event/client IP, multipart upload closure, and the `{"images": [...]}` response schema. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `POST /api/tasks/{task_id}/images` route. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved private-image upload endpoint body and supplies its existing helpers/settings to `TaskService`.
- `backend/routers/tasks.py` — adds the unchanged multipart image-upload HTTP endpoint with existing dependency behavior.
- `backend/services/task_service.py` — adds the injected authorized private-image upload operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused image regression: `python -m unittest test_main.CalendarApiTests.test_private_image_upload_validation_authorization_and_deletion test_main.CalendarApiTests.test_private_image_rotation_is_authorized_non_destructive_and_audited test_acceptance.PhaseOneAcceptanceTests.test_phase_one_task_authorization_status_images_calendar_and_audit_acceptance -v` (from `backend`): **PASS** — 3 tests in **10.227s**. This covers upload authorization, MIME/signature rejection, metadata redaction, private image access, the five-image limit, upload audit events, retained image revisions, and Phase-1 direct-URL authorization behavior.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check && python -c "...route assertions..."` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one image-upload route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **104.398s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified source files. A tracked sensitive-file scan found no database, DPAPI/key, certificate, `.env`, or private-upload path; none is included.

Next Phase:
- Continue the task group with the smallest remaining behavior-preserving attachment endpoint slice behind the existing SQL-free router/service boundary, then run focused attachment coverage and the full regression suite.

## Codex Execution PRD — task attachment-download router/service slice (2026-08-06 12:23:39 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: attachment upload/delete endpoints, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/tasks/{task_id}/attachments/{attachment_id}` private attachment download endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated it to `TaskService.download_task_attachment`.
- Preserved first-password-change enforcement, task-level authorization before private-file access, the established Korean 404 behavior for missing attachment metadata or content, forced download disposition with UTF-8 filename encoding, original MIME type, `private, no-store` cache policy, and `nosniff` response header. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `GET /api/tasks/{task_id}/attachments/{attachment_id}` route. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved private attachment download endpoint body and supplies the existing guarded private-upload path helper to `TaskService`.
- `backend/routers/tasks.py` — adds the unchanged attachment-download HTTP endpoint with existing dependency behavior.
- `backend/services/task_service.py` — adds the injected authorized private attachment download operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused attachment regression: `python -m unittest test_main.CalendarApiTests.test_private_document_video_attachment_validation_authorization_and_deletion -v` (from `backend`): **PASS** — 1 test in **3.058s**. This covers attachment upload validation, direct-URL authorization, forced private download headers and content, deletion, and attachment audit behavior.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...route assertion..." && git diff --check` (from `backend`) plus a source-token assertion (from repository root): **PASS** — compilation, unchanged title/44-route contract, exactly one attachment-download route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **95.905s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified source files. No database, DPAPI/key file, plaintext backup, private upload, secret, or `.env` is included.

Next Phase:
- Continue the task group with the smallest remaining behavior-preserving attachment endpoint slice (delete or upload) behind the existing SQL-free router/service boundary, then run focused attachment coverage and the full regression suite.

## Codex Execution PRD — task attachment-delete router/service slice (2026-08-06 12:39:47 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: attachment upload, Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `DELETE /api/tasks/{task_id}/attachments/{attachment_id}` private attachment-delete endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated it to `TaskService.delete_task_attachment`.
- Preserved first-password-change enforcement, task-level authorization before private-file or metadata access, the established Korean 404 behavior, attachment metadata redaction, audit payload/event/client IP, post-transaction private-file cleanup, and the existing success response schema. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one each of `GET` and `DELETE /api/tasks/{task_id}/attachments/{attachment_id}`. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved private attachment-delete endpoint body and supplies the existing attachment metadata projection to `TaskService`.
- `backend/routers/tasks.py` — adds the unchanged attachment-delete HTTP endpoint with existing dependency behavior.
- `backend/services/task_service.py` — adds the injected authorized private attachment-delete operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused attachment regression: `python -m unittest test_main.CalendarApiTests.test_private_document_video_attachment_validation_authorization_and_deletion -v` (from `backend`): **PASS** — 1 test in **3.001s**. This covers attachment upload validation, direct-URL authorization, forced private download headers and content, deletion, and attachment audit behavior.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...route assertions..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one attachment-download and attachment-delete route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **95.871s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified source files. A tracked sensitive-file scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the task group with the smallest remaining behavior-preserving attachment endpoint slice (upload) behind the existing SQL-free router/service boundary, then run focused attachment coverage and the full regression suite.

## Codex Execution PRD — task attachment-upload router/service slice (2026-08-06 12:58:24 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: Dashboard/Admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `POST /api/tasks/{task_id}/attachments` private document/video upload endpoint into the existing SQL-free `backend/routers/tasks.py` boundary and delegated it to `TaskService.upload_task_attachments`.
- Preserved first-password-change enforcement; authorization before private-byte inspection; attachment count and per-MIME limits; MIME/signature validation; task limit/trigger translation; private paths/permissions; transaction and cleanup behavior; filename sanitation; SHA-256 storage; metadata redaction; audit payload/event/client IP; multipart-upload closure; status **201**; and the `{\"attachments\": [...]}` response schema. API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `POST /api/tasks/{task_id}/attachments` route. The task router contains no `SELECT`, `INSERT`, `UPDATE`, `DELETE`, or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved private attachment-upload endpoint body and supplies its existing helpers/settings to `TaskService`.
- `backend/routers/tasks.py` — adds the unchanged multipart attachment-upload HTTP endpoint with existing dependency behavior.
- `backend/services/task_service.py` — adds the injected authorized private document/video upload operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused attachment regression: `python -m unittest test_main.CalendarApiTests.test_private_document_video_attachment_validation_authorization_and_deletion -v` (from `backend`): **PASS** — 1 test in **3.008s**. It covers upload authorization, validation rejection, private direct-URL download headers/content, deletion, and attachment audit events.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/tasks.py services/task_service.py main.py && python -c "...route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one attachment-upload route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **92.601s**; JavaScript syntax, Python compilation, package import, route assertion, and whitespace checks passed.

Risk:
- `TaskService` still contains repository SQL as an intentional intermediate service boundary. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified source files. A tracked sensitive-file scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; no sensitive file will be included. `backend/calendar.db` and plaintext DB backups are ignored.

Next Phase:
- Continue the dashboard group with the smallest remaining behavior-preserving endpoint slice (completed-date calendar or XLSX export) behind an SQL-free router/service boundary, then run focused dashboard coverage and the full regression suite.

## Codex Execution PRD — dashboard statistics router/service slice (2026-08-06 13:15:27 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: completed-calendar/export/notification/master/admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/statistics` dashboard endpoint into the new SQL-free `backend/routers/dashboard.py` boundary and delegated aggregation/filtering to `DashboardService`.
- Preserved first-password-change enforcement; authenticated date/query validation; existing server-side authorized task scope; member self-only assignee filtering and 403 rejection of other-user filters; status and per-assignee aggregate semantics; response field names/values; and the existing API URL. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `GET /api/statistics` route. `backend/routers/dashboard.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved statistics endpoint and wires the dashboard router/service.
- `backend/routers/dashboard.py` — adds the unchanged statistics HTTP endpoint with existing dependency behavior.
- `backend/services/dashboard_service.py` — adds the extracted authorized dashboard aggregation operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused dashboard regression: `python -m unittest test_main.CalendarApiTests.test_statistics_scope_status_user_aggregation_and_validation -v` (from `backend`): **PASS** — 1 test in **2.359s**. It covers filtered admin aggregates, member-only aggregate visibility, forbidden direct foreign-assignee filtering, and invalid date-range validation.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/dashboard.py services/dashboard_service.py main.py && python -c "...route and SQL-free router assertions..." && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one statistics route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...package import and route assertions..." && git diff --check`: **PASS** — all **27 tests** passed in **95.672s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, and whitespace checks passed.

Risk:
- `TaskService` and `DashboardService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified source files. A tracked sensitive-file scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the dashboard group with the smallest remaining behavior-preserving endpoint slice (completed-date calendar or XLSX export) behind an SQL-free router/service boundary, then run focused dashboard coverage and the full regression suite.

## Codex Execution PRD — completed-date calendar router/service slice (2026-08-06 13:34:36 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: XLSX export, notification/master/admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/completed-calendar` endpoint into the existing SQL-free `backend/routers/dashboard.py` boundary and delegated completed-month filtering and task projection to `DashboardService.completed_calendar`.
- Preserved first-password-change enforcement; exact required `month` query parameter behavior; strict `YYYY-MM` validation and Korean 422 response; inclusive month-boundary semantics; completed-status filtering; existing server-side authorized task scope; task projection and response list schema; and the existing API URL. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `GET /api/completed-calendar` route. `backend/routers/dashboard.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved completed-date calendar endpoint body and supplies the existing task projection helper to `DashboardService`.
- `backend/routers/dashboard.py` — adds the unchanged completed-date calendar HTTP endpoint with existing dependency behavior.
- `backend/services/dashboard_service.py` — adds the extracted authorized completed-month calendar operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused completed-calendar regression: `python -m unittest test_main.CalendarApiTests.test_completed_date_report_calendar_uses_task_scope_and_month_validation -v` (from `backend`): **PASS** — 1 test in **2.196s**. It covers member scope, admin scope, completed-month filtering, and malformed-month rejection.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/dashboard.py services/dashboard_service.py main.py && python -c "...route assertions..." && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one completed-calendar route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...package import and route assertions..." && git diff --check`: **PASS** — all **27 tests** passed in **96.215s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, and whitespace checks passed.

Risk:
- `TaskService` and `DashboardService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified source files. A tracked sensitive-file scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the dashboard group with the smallest remaining behavior-preserving endpoint slice (XLSX export) behind an SQL-free router/service boundary, then run focused export coverage and the full regression suite.
