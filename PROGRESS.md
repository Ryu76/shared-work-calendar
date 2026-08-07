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

## Codex Execution PRD — XLSX export router/service slice (2026-08-06 13:52:33 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: notification/master/admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/tasks/export.xlsx` endpoint into the existing SQL-free `backend/routers/dashboard.py` boundary and delegated its authorized filtering, export-size validation, local workbook invocation, and audit write to `DashboardService.export_tasks_xlsx`.
- Preserved first-password-change enforcement; all existing status, keyword, received-date, due-date, and assignee filters; member self-only assignee filtering and 403 rejection of other-user filters; authorized server-side task scope; the 10,000-row limit and Korean validation responses; spreadsheet formula neutralization through the existing workbook helper; `TASKS_EXPORTED` audit payload/client IP; XLSX MIME type; attachment filename; `private, no-store` and `nosniff` response headers; and the existing API URL. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/import verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `GET /api/tasks/export.xlsx` route. `backend/routers/dashboard.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved XLSX endpoint body and injects the existing workbook/audit helpers into `DashboardService`.
- `backend/routers/dashboard.py` — adds the unchanged XLSX export HTTP endpoint with existing dependencies and download response headers.
- `backend/services/dashboard_service.py` — adds the extracted authorized XLSX export operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused XLSX regression: `python -m unittest test_main.CalendarApiTests.test_excel_export_matches_authorized_filtered_scope_and_is_spreadsheet_safe -v` (from `backend`): **PASS** — 1 test in **2.552s**. It covers authorized filtering, workbook contents, spreadsheet-safe text, download response behavior, audit logging, and foreign-member assignee rejection.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/dashboard.py services/dashboard_service.py main.py && python -c "...route assertions..." && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one XLSX-export route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...package import and route assertions..." && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **91.268s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, and whitespace checks passed.

Risk:
- `TaskService` and `DashboardService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified source files. No database, DPAPI/key file, plaintext backup, private upload, secret, or `.env` is included.

Next Phase:
- Continue the master/admin group with the smallest remaining behavior-preserving endpoint slice behind an SQL-free router/service boundary, then run focused coverage and the full regression suite.

## Codex Execution PRD — local notification router/service slice (2026-08-06 14:11:11 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: master/admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged local-only notification preference and outbox endpoints into the new SQL-free `backend/routers/notifications.py` boundary and delegated preference storage, due-date refresh, caller-scoped listing/pagination, and read acknowledgement to `NotificationService`.
- Preserved first-password-change enforcement; all four existing endpoints and request/response schemas; lazy preference creation; per-user private outbox scope; unread filtering/pagination; local preference audit event and client IP; 404 handling for another user's notification; and `IN_APP_OUTBOX_ONLY` behavior. The injected Seoul-date callback remains patchable by the existing isolated regression suite. No external notification was dispatched, and database schema/data, key material, uploads, secrets, `.env`, deployment, and external-service behavior did not change.
- Route/static verification confirms `Shared Work Calendar MVP` still registers **44** routes, with exactly one route each for `GET`/`PATCH /api/me/notification-preferences`, `GET /api/notifications`, and `POST /api/notifications/{notification_id}/read`. The notification router contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved notification endpoint/helper bodies and injects/registers `NotificationService`.
- `backend/routers/notifications.py` — adds unchanged local notification HTTP endpoints with existing dependency behavior.
- `backend/services/notification_service.py` — adds the extracted local-only preference/outbox operations.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused notification regression: `python -m unittest test_main.CalendarApiTests.test_due_dates_local_notification_outbox_preferences_and_authorization -v` (from `backend`): **PASS** — 1 test in **3.401s**. It covers due-date validation, caller-only outbox visibility, Seoul-date reminder generation, read authorization, stale-message refresh, preference disabling, and the audit event.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/notifications.py services/notification_service.py main.py && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/notifications.py && python -c "...route contract..." && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && git diff --check`: **PASS** — all **27 tests** passed in **92.053s**; JavaScript syntax, Python compilation, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `AuthService`, and `NotificationService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified source files. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the master/admin group with the smallest remaining behavior-preserving endpoint slice behind an SQL-free router/service boundary, then run focused coverage and the full regression suite.

## Codex Execution PRD — organization autocomplete router/service slice (2026-08-06 14:29:22 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: remaining master/admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/organizations` active-organization autocomplete endpoint into the new SQL-free `backend/routers/master.py` boundary and delegated database lookup/projection to `MasterService.organizations`.
- Preserved authenticated first-password-change enforcement; the existing `q` query parameter/default; whitespace-trimmed partial matching; active-only filtering; name ordering; 20-row limit; `is_active` boolean response value; and the existing API URL/request-response schema. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/static verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `GET /api/organizations` route. `backend/routers/master.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved organization-autocomplete endpoint body and wires `MasterService`/the master router.
- `backend/routers/master.py` — adds the unchanged organization-autocomplete HTTP endpoint with existing dependency behavior.
- `backend/services/master_service.py` — adds the extracted active-organization lookup operation.
- `backend/test_main.py` — extends master lifecycle coverage to assert the authenticated public organization autocomplete response.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused master regression: `python -m unittest test_main.CalendarApiTests.test_request_master_management_authorization_lifecycle_and_audit -v` (from `backend`): **PASS** — 1 test in **2.183s**.
- Router contract/static-boundary verification: compilation, unchanged title/44-route contract, exactly one organization-autocomplete route, SQL-free router check, and whitespace check: **PASS**.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...package route assertion..." && git diff --check`: **PASS** — all **27 tests** passed in **96.384s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `AuthService`, `NotificationService`, and the new `MasterService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the four verified source/test files. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the master/admin group with the smallest remaining behavior-preserving endpoint slice behind an SQL-free router/service boundary, then run focused coverage and the full regression suite.

## Codex Execution PRD — organization creation router/service slice (2026-08-06 14:47:48 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: remaining master/admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `POST /api/organizations` endpoint into the existing SQL-free `backend/routers/master.py` boundary and delegated create-or-reuse behavior and audit writing to `MasterService.create_organization`.
- Preserved authenticated first-password-change enforcement; existing `OrganizationIn` validation; status **201** for both a newly created organization and a same-name reuse; active boolean response projection; `ORGANIZATION_CREATED` audit actor/IP/payload behavior only for a new row; and the existing API URL/request-response schema. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/static verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `POST /api/organizations` route. `backend/routers/master.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved organization-creation endpoint body and injects existing time/audit helpers into `MasterService`.
- `backend/routers/master.py` — adds the unchanged organization-creation HTTP endpoint with existing authentication behavior.
- `backend/services/master_service.py` — adds the extracted create-or-reuse organization operation.
- `backend/test_main.py` — extends master lifecycle coverage for direct organization creation and same-name reuse.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused master regression: `python -m unittest test_main.CalendarApiTests.test_request_master_management_authorization_lifecycle_and_audit -v` (from `backend`): **PASS** — 1 test in **2.332s**. It covers direct member organization creation/reuse plus the existing master authorization, lifecycle, and audit flow.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/master.py services/master_service.py main.py && python -c "...route contract..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one organization-create route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...package route assertion..." && git diff --check`: **PASS** — all **27 tests** passed in **92.615s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `AuthService`, `NotificationService`, and `MasterService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the four verified non-sensitive source/test files. No database, DPAPI/key file, plaintext backup, private upload, secret, or `.env` is included.

Next Phase:

## Codex Execution PRD — request-contact autocomplete router/service slice (2026-08-06 15:05:29 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: remaining master/admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/request-contacts` active request-contact autocomplete endpoint into the existing SQL-free `backend/routers/master.py` boundary and delegated database lookup/projection to `MasterService.contacts`.
- Preserved authenticated first-password-change enforcement; the existing `q` query parameter/default; whitespace-trimmed name-or-organization partial matching; contact/organization active-only filtering; name and organization ordering; 20-row limit; contact response projection; and the existing API URL/request-response schema. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/static verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `GET /api/request-contacts` route. `backend/routers/master.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved request-contact autocomplete endpoint body and injects the existing contact projection helper into `MasterService`.
- `backend/routers/master.py` — adds the unchanged request-contact autocomplete HTTP endpoint with existing authentication behavior.
- `backend/services/master_service.py` — adds the extracted active request-contact lookup operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused master regression: `python -m unittest test_main.CalendarApiTests.test_request_master_management_authorization_lifecycle_and_audit -v` (from `backend`): **PASS** — 1 test in **2.312s**. It covers request-contact autocomplete along with master authorization, lifecycle, and audit behavior.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/master.py services/master_service.py main.py && python -c "...route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one request-contact autocomplete route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...package route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **92.149s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `AuthService`, `NotificationService`, and `MasterService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified non-sensitive source files. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the master/admin group with the smallest remaining behavior-preserving endpoint slice behind an SQL-free router/service boundary, then run focused coverage and the full regression suite.

## Codex Execution PRD — request-contact creation router/service slice (2026-08-06 15:23:54 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: remaining master/admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `POST /api/request-contacts` endpoint into the existing SQL-free `backend/routers/master.py` boundary and moved its shared contact-create-or-reuse helper into `MasterService`.
- Preserved authenticated first-password-change enforcement; existing `ContactIn` validation; status **201**; create-or-reuse behavior for the same name, phone, and organization; automatic organization creation; unchanged contact response projection; master creation audit events, actor/IP values, and transaction behavior. Task creation and update continue to use the same helper through the injected `MasterService` method.
- Preserved all API URLs, request/response schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior.
- Route/static verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `POST /api/request-contacts` route. `backend/routers/master.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved request-contact creation route/helper, creates the shared master service once, and injects its contact operation into task handling.
- `backend/routers/master.py` — adds the unchanged request-contact creation HTTP endpoint with existing authentication behavior.
- `backend/services/master_service.py` — adds the moved create-or-reuse master operation and contact response operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused master regression: `python -m unittest test_main.CalendarApiTests.test_request_master_management_authorization_lifecycle_and_audit -v` (from `backend`): **PASS** — 1 test in **2.362s**. It covers request-contact creation, contact/organization autocomplete, master authorization, lifecycle, and audit behavior.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/master.py services/master_service.py main.py && python -c "...route contract..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one request-contact-create route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...package route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **93.524s**; JavaScript syntax, Python compilation, unchanged 44-route contract, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `AuthService`, `NotificationService`, and `MasterService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified non-sensitive source files. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the master/admin group with the smallest remaining behavior-preserving endpoint slice behind an SQL-free router/service boundary, then run focused coverage and the full regression suite.

## Codex Execution PRD — admin organization-list router/service slice (2026-08-06 15:44:42 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: the remaining admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/admin/organizations` endpoint into the existing SQL-free `backend/routers/master.py` boundary and delegated the existing administrator organization-management lookup/projection to `MasterService.admin_organizations`.
- Preserved the administrator dependency (including forced-password-change enforcement); whitespace-trimmed `q` filtering; active-first/name ordering; 100-row limit; organization response projection; and the existing API URL/request-response schema. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/static verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `GET /api/admin/organizations` route. `backend/routers/master.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved administrator organization-list endpoint and supplies the existing administrator dependency to the master router.
- `backend/routers/master.py` — adds the unchanged administrator organization-list HTTP boundary.
- `backend/services/master_service.py` — adds the extracted organization-management list operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused master regression: `python -m unittest test_main.CalendarApiTests.test_request_master_management_authorization_lifecycle_and_audit -v` (from `backend`): **PASS** — 1 test in **2.296s**. It covers member rejection and the administrator organization-list query together with the existing master lifecycle/audit flow.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/master.py services/master_service.py main.py && python -c "...route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py && git diff --check` (from `backend`): **PASS** — compilation, unchanged title/44-route contract, exactly one administrator organization-list route, SQL-free router check, and whitespace check passed.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **93.942s**; JavaScript syntax, Python compilation, unchanged 44-route contract, SQL-free router check, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `AuthService`, `NotificationService`, and `MasterService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified non-sensitive source files. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the master/admin group with the smallest remaining behavior-preserving endpoint slice (`GET /api/admin/request-contacts`) behind the existing SQL-free router/service boundary, then run focused coverage and the full regression suite.

## Codex Execution PRD — admin request-contact-list router/service slice (2026-08-06 16:02:37 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: remaining admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `GET /api/admin/request-contacts` endpoint into the existing SQL-free `backend/routers/master.py` boundary and delegated the existing administrator request-contact-management lookup/projection to `MasterService.admin_contacts`.
- Preserved the administrator dependency (including forced-password-change enforcement); whitespace-trimmed name/phone/organization filtering; active-first/name/organization ordering; 100-row limit; contact response projection; and the existing API URL/request-response schema. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/static verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `GET /api/admin/request-contacts` route. `backend/routers/master.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved administrator request-contact-list endpoint body.
- `backend/routers/master.py` — adds the unchanged administrator request-contact-list HTTP boundary.
- `backend/services/master_service.py` — adds the extracted request-contact-management list operation.
- `backend/test_main.py` — extends master lifecycle coverage to assert the administrator request-contact-list response.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused master regression: `python -m unittest test_main.CalendarApiTests.test_request_master_management_authorization_lifecycle_and_audit -v` (from `backend`): **PASS** — 1 test in **2.346s**.
- Router contract/static-boundary verification: compilation, unchanged title/44-route contract, exactly one administrator request-contact-list route, SQL-free router check, and whitespace check: **PASS**.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...package route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' backend/routers/master.py && git diff --check`: **PASS** — all **27 tests** passed in **92.944s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, SQL-free router check, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `AuthService`, `NotificationService`, and `MasterService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the four verified non-sensitive source/test files. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the master/admin group with the smallest remaining behavior-preserving endpoint slice (`PATCH /api/admin/organizations/{organization_id}`) behind the existing SQL-free router/service boundary, then run focused coverage and the full regression suite.

## Codex Execution PRD — admin organization-update router/service slice (2026-08-06 16:20:32 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: remaining admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `PATCH /api/admin/organizations/{organization_id}` endpoint into the existing SQL-free `backend/routers/master.py` boundary and delegated the existing administrator organization update operation to `MasterService.patch_organization`.
- Preserved the administrator dependency (including forced-password-change enforcement); `OrganizationPatch` validation; not-found and duplicate-name status/detail behavior; partial-name/active updates; organization response projection including timestamps; audit-before/after content, actor/IP values, and audit-on-change-only behavior; transaction behavior; and the existing API URL/request-response schema. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/static verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `PATCH /api/admin/organizations/{organization_id}` route. `backend/routers/master.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved administrator organization-update endpoint body and its no-longer-needed request-model import.
- `backend/routers/master.py` — adds the unchanged administrator organization-update HTTP boundary.
- `backend/services/master_service.py` — adds the extracted organization update operation.
- `backend/test_main.py` — strengthens master lifecycle coverage for the unchanged organization update response.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused master regression: `python -m unittest test_main.CalendarApiTests.test_request_master_management_authorization_lifecycle_and_audit -v` (from `backend`): **PASS** — 1 test in **2.323s**.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/master.py services/master_service.py main.py`; then package import/title/44-route/single-PATCH-route assertion; `! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py`; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...package route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **93.651s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, SQL-free router check, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `AuthService`, `NotificationService`, and `MasterService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the four verified non-sensitive source/test files. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the master/admin group with the smallest remaining behavior-preserving endpoint slice (`GET /api/admin/audit-logs`) behind an SQL-free router/service boundary, then run focused coverage and the full regression suite.

## Codex Execution PRD — admin request-contact-update router/service slice (2026-08-06 16:37:53 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: remaining admin routes, repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering are still pending.
- Extracted the unchanged `PATCH /api/admin/request-contacts/{contact_id}` endpoint into the existing SQL-free `backend/routers/master.py` boundary and delegated the existing administrator request-contact update operation to `MasterService.patch_contact`.
- Preserved the administrator and forced-password-change dependency; `ContactPatch` validation; not-found, missing-organization, and duplicate-combination status/detail behavior; partial name/phone/organization/active updates; contact response projection; audit before/after content, actor/IP values, audit-on-change-only behavior; transaction behavior; and existing API URL/request-response schemas. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/static verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `PATCH /api/admin/request-contacts/{contact_id}` route. `backend/routers/master.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved administrator request-contact update endpoint and its no-longer-needed request-model imports.
- `backend/routers/master.py` — adds the unchanged administrator request-contact update HTTP boundary.
- `backend/services/master_service.py` — adds the extracted request-contact update operation.
- `backend/test_main.py` — strengthens master lifecycle coverage for unchanged updated-contact response fields.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused master regression: `python -m unittest test_main.CalendarApiTests.test_request_master_management_authorization_lifecycle_and_audit -v` (from `backend`): **PASS** — 1 test in **2.423s**.
- Router contract/static-boundary verification: compilation; package import/title/44-route/single-PATCH-route assertion; SQL-free router check; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/main.py backend/app/main.py backend/routers backend/services backend/schemas backend/database.py backend/core backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...package route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' backend/routers/master.py && git diff --check`: **PASS** — all **27 tests** passed in **93.160s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, SQL-free router check, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `AuthService`, `NotificationService`, and `MasterService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the four verified non-sensitive source/test files. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the master/admin group with the smallest remaining behavior-preserving endpoint slice (`GET /api/admin/audit-logs`) behind an SQL-free router/service boundary, then run focused coverage and the full regression suite.

## Codex Execution PRD — admin audit-log router/service slice (2026-08-06 16:54:24 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: repository-only SQL, global exception handling, response helpers, validator/middleware/notification/scheduler layering, and `main.py` minimization are still pending.
- Extracted the unchanged `GET /api/admin/audit-logs` endpoint into the existing SQL-free `backend/routers/master.py` boundary and delegated its audit lookup, inclusive UTC date filtering, and response projection to `MasterService.audit_logs`.
- Preserved the administrator dependency (including forced-password-change enforcement); `action`, `actor_user_id`, `created_from`, and `created_to` query validation; invalid date-range 422 detail; action/actor/date filtering; descending-ID ordering; 100-row limit; sensitive audit-value redaction; and the existing API URL/request-response schema. Database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- Route/static verification confirms `Shared Work Calendar MVP` still registers **44** routes and exactly one `GET /api/admin/audit-logs` route. `backend/routers/master.py` contains no SQL operation or `.execute(` token.

Modified Files:
- `backend/app/main.py` — removes only the moved audit-log endpoint body, removes now-unused imports, and supplies the existing audit response projection to `MasterService`.
- `backend/routers/master.py` — adds the unchanged administrator audit-log HTTP boundary.
- `backend/services/master_service.py` — adds the extracted administrator audit lookup/filter operation.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused audit regression: `python -m unittest test_main.CalendarApiTests.test_audit_log_filters_authorization_validation_and_sensitive_redaction -v` (from `backend`): **PASS** — 1 test in **2.011s**. It covers administrator-only direct access, validation, all query filters, inclusive date bounds, and sensitive-field redaction.
- Router contract/static-boundary verification: `python -m compileall -q app/main.py routers/master.py services/master_service.py main.py`; package import/title/44-route/single-audit-route assertion; `! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py`; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...package route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/master.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **93.995s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, SQL-free router check, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `AuthService`, `NotificationService`, and `MasterService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only the three verified non-sensitive source files. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Begin the repository phase with one small, behavior-preserving database-operation extraction behind an existing service boundary, then run focused coverage and the full regression suite.

## Codex Execution PRD — authentication repository slice (2026-08-06 17:11:41 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: most service SQL is still not repository-only, global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization are pending.
- Created the first persistence-only repository boundary, `AuthRepository`, and moved the authentication service's existing login-ID lookup and legacy-password-hash upgrade write into it.
- Preserved the existing `POST /api/auth/login` URL and request/response schema; login failure/success audit behavior; disabled-account rejection; Argon2id upgrade timing and audit; eight-hour session behavior; database transaction behavior; and all existing external-service behavior. Database schema/data, DPAPI/key material, uploads, secrets, `.env`, notification delivery, and deployment did not change.
- `AuthService` now contains no SQL operation or `.execute(` token; SQL for this auth slice is confined to `backend/repositories/auth_repository.py`. The application title, 44-route contract, and exactly one login route remain unchanged.

Modified Files:
- `backend/repositories/__init__.py` — declares the repository package.
- `backend/repositories/auth_repository.py` — adds authentication user lookup and password-hash update persistence operations.
- `backend/services/auth_service.py` — delegates those database operations through `AuthRepository` while retaining business logic and transaction/audit control.
- `backend/app/main.py` — wires the repository into the existing authentication service composition root.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused authentication regression: `python -m unittest test_main.CalendarApiTests.test_argon2id_is_used_for_new_passwords_and_legacy_pbkdf2_upgrades_on_login -v` (from `backend`): **PASS** — 1 test in **2.052s**. It covers new Argon2id password use, rejection on wrong legacy password, successful legacy-password login, hash upgrade, and upgrade audit logging.
- Static/contract verification: `python -m compileall -q app/main.py services/auth_service.py repositories`; package title/44-route/single-login-route assertion; SQL-free `AuthService` check; repository import assertion; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...package route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' services/auth_service.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **91.024s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, SQL-free service check, and whitespace checks passed.

Risk:
- `TaskService`, `DashboardService`, `UserService`, `NotificationService`, and `MasterService` still contain repository SQL as intentional intermediate service boundaries. The PRD requirement that SQL reside only in repositories remains unfulfilled; `AuthRepository` is the first small migrated slice.
- Before the progress update, `git status --short --untracked-files=all` listed only `backend/app/main.py`, `backend/services/auth_service.py`, and the new `backend/repositories/` Python package. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining authentication-adjacent behavior-preserving slice (move active-user lookup from `current_user` into a repository boundary), then run focused authorization coverage and the full regression suite.

## Codex Execution PRD — user-assignee repository slice (2026-08-06 17:28:20 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: most service SQL is still not repository-only, global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization are pending.
- Added the small persistence-only `UserRepository` boundary and moved only the active assignee-selection query from `UserService.assignees` into `UserRepository.active_assignees`.
- Preserved the existing `GET /api/assignees` URL, authentication and first-password-change enforcement in its router, active-user-only filtering, name/login-ID ordering, list response projection, SQLCipher transaction behavior, API schemas, database schema/data, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior.
- The unchanged 44-route application contract contains exactly one `GET /api/assignees` route. `UserService.assignees` now delegates to the repository and no longer contains the extracted active-assignee SQL query.

Modified Files:
- `backend/repositories/user_repository.py` — adds the active-assignee persistence operation.
- `backend/services/user_service.py` — injects and delegates only the active-assignee database lookup to `UserRepository`.
- `backend/app/main.py` — wires `UserRepository` into the existing user-service composition root.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused user/task regression: `python -m unittest test_main.CalendarApiTests.test_task_detail_update_history_and_deletion_authorization -v` (from `backend`): **PASS** — 1 test in **3.843s**. It exercises the unchanged authenticated assignee-selection response before creating and updating a joint task, as well as task authorization/history/deletion behavior.
- Static/contract verification: compilation; package title/44-route/single-assignees-route assertion; repository delegation and extracted-query-absence assertions; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...44-route assertion..." && ... && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **92.544s**; JavaScript syntax, Python compilation, unchanged 44-route/single-assignees-route contract, repository delegation check, and whitespace checks passed.

Risk:
- `UserService` still contains password-change, user-list, user-create, and user-update SQL; `TaskService`, `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before the progress update, `git status --short --untracked-files=all` listed only the three verified non-sensitive source files. A changed-path scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining authentication-adjacent behavior-preserving slice: move the password-change update from `UserService` into `UserRepository`, then run focused authorization coverage and the full regression suite.

## Codex Execution PRD — current-user repository slice (2026-08-06 17:44:33 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: most service SQL is still not repository-only, global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization are pending.
- Added the small persistence-only `UserRepository.find_active_by_id` operation and moved only the active authenticated-user lookup used by `current_user` out of `backend/app/main.py`.
- Preserved the existing bearer-token parsing, eight-hour session expiry check, inactive-account session invalidation, 401 status/detail behavior, all API URLs/request-response schemas, database schema/data, SQLCipher transaction behavior, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior.
- The existing `UserRepository` is now composed once and shared by `current_user` and `UserService`; the unchanged application contract still registers 44 routes and exactly one `GET /api/assignees` route. The direct active-user SQL is absent from `backend/app/main.py`.

Modified Files:
- `backend/app/main.py` — composes the shared user repository and delegates the active authenticated-user lookup.
- `backend/repositories/user_repository.py` — adds the active-user-by-ID persistence operation.
- `backend/test_main.py` — extends user-lifecycle regression coverage to verify a just-deactivated account's existing bearer token is rejected by `/api/me`.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused authorization regression: `python -m unittest test_main.CalendarApiTests.test_admin_user_lifecycle_validation_authorization_and_last_admin_protection -v` (from `backend`): **PASS** — 1 test in **2.450s**. It covers administrator-only lifecycle actions, last-admin protection, and the newly asserted invalidation of an already-issued token after account deactivation.
- Static/contract verification: `python -m compileall -q app/main.py repositories/user_repository.py services/user_service.py main.py`; package title/44-route/single-assignees-route assertion; active-user repository delegation and extracted-query-absence assertions; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...package route/repository assertion..." && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **97.017s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, repository delegation/query-absence checks, and whitespace checks passed.

Risk:
- `UserService` still contains password-change, user-list, user-create, and user-update SQL; `TaskService`, `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before the progress update, `git status --short --untracked-files=all` listed only `backend/app/main.py`, `backend/repositories/user_repository.py`, and `backend/test_main.py`. A changed-path sensitive-file scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining authentication-adjacent behavior-preserving slice: move the password-change update from `UserService` into `UserRepository`, then run focused authorization coverage and the full regression suite.

## Codex Execution PRD — user password-update repository slice (2026-08-06 17:59:38 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: most service SQL is still not repository-only, global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization are pending.
- Added the small persistence-only `UserRepository.update_password` operation and moved only the password-change write from `UserService.change_password` into it.
- Preserved the existing `POST /api/me/password` URL and request/response schema; current-password verification; same-password validation; Argon2id hashing; forced-password-change clearing; password-change audit content/actor/IP behavior; transaction behavior; and existing session behavior. Database schema/data, SQLCipher behavior, key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior did not change.
- The unchanged application contract still registers 44 routes and exactly one `POST /api/me/password` route. `UserService.change_password` delegates its extracted write to `UserRepository`; the extracted password-update SQL is absent from the service.

Modified Files:
- `backend/repositories/user_repository.py` — adds the password-change persistence operation.
- `backend/services/user_service.py` — delegates only the password-change write through `UserRepository` while retaining validation, transaction, and audit behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused password regression: `python -m unittest test_main.CalendarApiTests.test_first_login_requires_password_change_and_blocks_work_apis -v` (from `backend`): **PASS** — 1 test in **2.365s**. It covers required password change, wrong-current-password rejection, successful change, work-API access after change, old-password rejection, new-password login, and password-change auditing.
- Static/contract verification: compilation; repository delegation/extracted-SQL-absence assertion; package title/44-route/single-password-route assertion; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...repository/password boundary and 44-route assertion..." && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **90.569s**; JavaScript syntax, Python compilation, package import, unchanged 44-route/single-password-route contract, repository delegation/extracted-query-absence check, and whitespace checks passed.

Risk:
- `UserService` still contains user-list, user-create, and user-update SQL; `TaskService`, `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/user_repository.py` and `backend/services/user_service.py`. A changed-path sensitive-file scan is required before commit; database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, and secret files must remain excluded.

Next Phase:
- Continue the repository phase with the smallest remaining user-service behavior-preserving slice: move the administrator user-list query into `UserRepository`, then run focused authorization coverage and the full regression suite.

## Codex Execution PRD — administrator user-list repository slice (2026-08-06 18:16:12 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: most service SQL is still not repository-only, global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization are pending.
- Added the small persistence-only `UserRepository.list_users` operation and moved only the administrator user-list query from `UserService.list_users` into it.
- Preserved the existing `GET /api/admin/users` URL and request/response schema; administrator and forced-password-change dependency; active-first/name ordering; response fields; integer-to-boolean projection for `is_active` and `must_change_password`; SQLCipher transaction behavior; database schema/data; key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- The unchanged application contract still registers 44 routes with exactly one `GET /api/admin/users` route. `UserService.list_users` delegates its extracted lookup to `UserRepository`; the extracted user-list SQL is absent from the service.

Modified Files:
- `backend/repositories/user_repository.py` — adds the administrator user-list persistence operation.
- `backend/services/user_service.py` — delegates only the administrator user-list lookup through `UserRepository` while retaining the established response projection.
- `backend/test_main.py` — extends administrator lifecycle coverage to assert the unchanged user-list status and full created-user projection.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused user lifecycle regression: `python -m unittest test_main.CalendarApiTests.test_admin_user_lifecycle_validation_authorization_and_last_admin_protection -v` (from `backend`): **PASS** — 1 test in **2.661s**. It now covers the administrator list response together with administrator-only lifecycle actions, validation, last-admin protection, audit behavior, and invalidation of a deactivated account's existing token.
- Static/contract verification: `python -m compileall -q app/main.py services/user_service.py repositories/user_repository.py routers/users.py main.py`; package title/44-route/single-GET-user-list/single-POST-user-create assertions; extracted-user-list-SQL absence assertion; SQL-free user-router check; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...package route/repository assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/users.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **94.339s**; JavaScript syntax, Python compilation, package import, unchanged 44-route contract, repository delegation/extracted-query-absence checks, SQL-free router check, and whitespace checks passed.

Risk:
- `UserService` still contains user-create and user-update SQL; `TaskService`, `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/user_repository.py`, `backend/services/user_service.py`, and `backend/test_main.py`. A tracked sensitive-path scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining user-service behavior-preserving slice: move the administrator user-create insert into `UserRepository`, then run focused authorization coverage and the full regression suite.

## Codex Execution PRD — administrator user-create repository slice (2026-08-06 18:31:14 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: user-update and most non-user service SQL are still outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `UserRepository.create_user` operation and moved only the administrator user-creation insert from `UserService.create_user` into it.
- Preserved the existing `POST /api/admin/users` URL/status/request-response schema; administrator and forced-password-change dependencies; Argon2id temporary-password hashing; duplicate-login `409` detail; generated user ID/result projection; `USER_CREATED` audit action, actor, target, after-data and IP behavior; transaction behavior; SQLCipher behavior; database schema/data; key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- The unchanged application contract still registers 44 routes with exactly one `POST /api/admin/users` route. `UserService.create_user` delegates its extracted persistence to `UserRepository`; the extracted `INSERT INTO users` SQL is absent from the service.

Modified Files:
- `backend/repositories/user_repository.py` — adds the administrator user-creation persistence operation.
- `backend/services/user_service.py` — delegates only the user-creation write through `UserRepository` while retaining existing validation, duplicate handling, audit, and response behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused user-lifecycle regression: `python -m unittest test_main.CalendarApiTests.test_admin_user_lifecycle_validation_authorization_and_last_admin_protection -v` (from `backend`): **PASS** — 1 test in **2.569s**. It covers administrator-only creation/lifecycle actions, created-user projection, validation, last-admin protection, audit behavior, and invalidation of a deactivated account's existing token.
- Static/contract verification: `python -m compileall -q app/main.py services/user_service.py repositories/user_repository.py routers/users.py main.py`; repository-delegation/extracted-SQL-absence assertions; package 44-route/single-POST-user-create assertion; SQL-free user-router check; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...repository/create boundary and 44-route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/users.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **92.132s**; JavaScript syntax, Python compilation, unchanged 44-route contract, repository boundary assertions, SQL-free user-router check, and whitespace checks passed.

Risk:
- `UserService` still contains user-update SQL; `TaskService`, `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before updating this record, `git status --short --untracked-files=all` listed only `backend/repositories/user_repository.py` and `backend/services/user_service.py`. The changed-path sensitive-file scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining user-service behavior-preserving slice: move the administrator user-update lookup into `UserRepository`, then run focused authorization coverage and the full regression suite.

## Codex Execution PRD — administrator user-update lookup repository slice (2026-08-06 18:45:35 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: user-update count/write and most non-user service SQL are still outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `UserRepository.find_by_id` operation and moved only the administrator user-update target lookup from `UserService.patch_user` into it.
- Preserved the existing `PATCH /api/admin/users/{user_id}` URL and request/response schema; administrator and forced-password-change dependencies; unknown-user 404 detail; last-active-admin protection; partial field update logic; password hashing/session invalidation; audit before/after content and actor/IP behavior; transaction behavior; SQLCipher behavior; database schema/data; key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- The unchanged application contract still registers 44 routes with exactly one `PATCH /api/admin/users/{user_id}` route. `UserService.patch_user` delegates its extracted target lookup to `UserRepository`; the extracted `SELECT * FROM users WHERE id=?` SQL is absent from the service.

Modified Files:
- `backend/repositories/user_repository.py` — adds the administrator user-update target lookup persistence operation.
- `backend/services/user_service.py` — delegates only the user-update target lookup through `UserRepository` while retaining existing business, transaction, session, and audit behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused user-lifecycle regression: `python -m unittest test_main.CalendarApiTests.test_admin_user_lifecycle_validation_authorization_and_last_admin_protection -v` (from `backend`): **PASS** — 1 test in **2.590s**. It covers administrator-only lifecycle actions, update behavior, last-admin protection, audit behavior, and invalidation of a deactivated account's existing token.
- Static/contract verification: `python -m compileall -q app/main.py services/user_service.py repositories/user_repository.py routers/users.py main.py`; package 44-route/single-PATCH-user-route assertion; repository delegation/extracted-SQL-absence assertion; SQL-free user-router check; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...repository/update-lookup boundary and 44-route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/users.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **94.036s**; JavaScript syntax, Python compilation, unchanged 44-route contract, repository boundary assertions, SQL-free router check, and whitespace checks passed.

Risk:
- `UserService` still contains user-update count/write SQL; `TaskService`, `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/user_repository.py` and `backend/services/user_service.py`; the changed-path sensitive-file scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path. None is included.

Next Phase:
- Continue the repository phase with the smallest remaining user-service behavior-preserving slice: move the active-administrator count used by user updates into `UserRepository`, then run focused authorization coverage and the full regression suite.

## Codex Execution PRD — active-administrator count repository slice (2026-08-06 19:00:31 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: the user-update write and most non-user service SQL are still outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `UserRepository.active_admin_count` operation and moved only the active-administrator count used by `UserService.patch_user` into it.
- Preserved the existing `PATCH /api/admin/users/{user_id}` URL and request/response schema; administrator and forced-password-change dependencies; unknown-user 404 detail; last-active-admin 409 protection; partial user-update logic; password hashing/session invalidation; audit before/after content and actor/IP behavior; transaction behavior; SQLCipher behavior; database schema/data; key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- The unchanged application contract still registers 44 routes with exactly one `PATCH /api/admin/users/{user_id}` route. The active-administrator count SQL is absent from `UserService` and confined to `UserRepository`.

Modified Files:
- `backend/repositories/user_repository.py` — adds the active-administrator count persistence operation.
- `backend/services/user_service.py` — delegates only the last-active-admin count lookup through `UserRepository`.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused user-lifecycle regression: `python -m unittest test_main.CalendarApiTests.test_admin_user_lifecycle_validation_authorization_and_last_admin_protection -v` (from `backend`): **PASS** — 1 test in **2.541s**. It exercises administrator-only lifecycle updates and last-active-admin protection.
- Static/contract verification: `python -m compileall -q app/main.py services/user_service.py repositories/user_repository.py routers/users.py main.py`; package 44-route/single-PATCH-user-route assertion; repository delegation/extracted-SQL-absence assertion; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...repository/count boundary and 44-route assertion..." && ! grep -nE "SELECT COUNT\\(\\*\\) FROM users WHERE role='ADMIN' AND is_active=1" services/user_service.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **93.776s**; JavaScript syntax, Python compilation, unchanged 44-route contract, repository delegation/query-absence checks, and whitespace checks passed.

Risk:
- `UserService` still contains the user-update SQL write; `TaskService`, `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/user_repository.py` and `backend/services/user_service.py`. A changed-path sensitive-file scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining user-service behavior-preserving slice: move the administrator user-update write into `UserRepository`, then run focused authorization coverage and the full regression suite.

## Codex Execution PRD — administrator user-update write repository slice (2026-08-06 19:15:54 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: most non-user service SQL is still outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `UserRepository.update_user` operation and moved only the administrator user-update write from `UserService.patch_user` into it.
- Preserved the existing `PATCH /api/admin/users/{user_id}` URL and request/response schema; administrator and forced-password-change dependencies; unknown-user 404 detail; last-active-admin 409 protection; partial user-update logic; Argon2id password hashing; password-reset forced-password-change behavior; session invalidation; audit before/after content and actor/IP behavior; transaction behavior; SQLCipher behavior; database schema/data; key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `UserService.patch_user` delegates the extracted persistence to `UserRepository`; the extracted `UPDATE users` statement is absent from the service. The unchanged application has exactly one `PATCH /api/admin/users/{user_id}` route.

Modified Files:
- `backend/repositories/user_repository.py` — adds the administrator user-update persistence operation.
- `backend/services/user_service.py` — delegates only the user-update write through `UserRepository` while retaining business, transaction, session, and audit behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused user-lifecycle regression: `python -m unittest test_main.CalendarApiTests.test_admin_user_lifecycle_validation_authorization_and_last_admin_protection -v` (from `backend`): **PASS** — 1 test in **2.584s**. It exercises administrator-only lifecycle updates, password reset/session invalidation, last-active-admin protection, and audit behavior.
- Static/contract verification: `python -m compileall -q app/main.py services/user_service.py repositories/user_repository.py routers/users.py main.py`; repository delegation/extracted-SQL-absence assertions; one-PATCH-user-route assertion; SQL-free user-router check; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...repository/update boundary and route assertion..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/users.py && git diff --check` (from `backend`): **PASS** — all **27 tests** passed in **93.036s**; JavaScript syntax, Python compilation, repository-boundary assertions, unchanged PATCH-user route, SQL-free router check, and whitespace checks passed.

Risk:
- `UserService` no longer contains user-account SQL; `TaskService`, `DashboardService`, `NotificationService`, and `MasterService` still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/user_repository.py` and `backend/services/user_service.py`. The changed-path sensitive-file scan produced no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving slice: inspect the remaining service SQL and move one cohesive `TaskService` persistence operation into its existing repository, then run focused authorization coverage and the full regression suite.

## Codex Execution PRD — task active-assignee lookup repository slice (2026-08-06 19:34:08 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: most Task/Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.active_user_ids` operation and moved the active-user lookup used by both `TaskService.create_task` and `TaskService.update_task` into it.
- Preserved `POST /api/tasks` and `PATCH /api/tasks/{task_id}` URLs, request/response schemas, validation detail, active-assignee policy, task authorization, task/contact/audit/notification transaction behavior, SQLCipher behavior, database schema/data, DPAPI/key material, uploads, secrets, `.env`, notification delivery, deployment, and external-service behavior.
- The extracted `SELECT id FROM users WHERE is_active=1` SQL is absent from `TaskService` and exists only in `TaskRepository`. The application still has exactly one POST and one GET `/api/tasks` route, and `routers/tasks.py` remains SQL-free.

Modified Files:
- `backend/repositories/task_repository.py` — adds the persistence-only active task-assignee ID lookup.
- `backend/services/task_service.py` — injects `TaskRepository` and delegates create/update active-assignee validation lookup to it.
- `backend/app/main.py` — composes the new repository into the existing task service without changing routes.
- `backend/test_main.py` — adds HTTP regression coverage that inactive assignees are rejected with the existing 422 behavior on both create and update.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused task-assignee regression: `python -m unittest test_main.CalendarApiTests.test_task_rejects_inactive_assignees_on_create_and_update -v && python -m compileall -q app/main.py services/task_service.py repositories/task_repository.py test_main.py && git diff --check` (from `backend`): **PASS** — 1 test in **1.404s**; Python compilation and whitespace validation passed.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...task active-user repository boundary and API route contract..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS** — all **28 tests** passed in **96.100s**; JavaScript syntax, Python compilation, extracted-SQL boundary, unchanged task route contract, SQL-free task router, and whitespace checks passed.

Risk:
- `TaskService` still contains task, attachment, image, calendar, and listing SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/app/main.py`, `backend/repositories/task_repository.py`, `backend/services/task_service.py`, and `backend/test_main.py`. The changed-path sensitive-file scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move the task-create insert/read persistence into `TaskRepository`, then run focused task creation/authorization coverage and the full regression suite.

## Codex Execution PRD — task-create repository persistence slice (2026-08-06 19:50:43 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: Task/Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.create_task` operation and moved only the task-create insert, task-assignee inserts, and created-task row lookup from `TaskService.create_task` into it.
- Preserved `POST /api/tasks` URL/status/request-response schema; existing input and active-assignee validation; contact/master/audit transaction behavior; multi-assignee behavior; status/date rules; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `TaskService.create_task` delegates the extracted persistence to `TaskRepository`; the extracted `INSERT INTO tasks`, `INSERT INTO task_assignees`, and created-task `SELECT` are absent from the create operation in the service. The application task routes remain unchanged and `routers/tasks.py` remains SQL-free.

Modified Files:
- `backend/repositories/task_repository.py` — adds task-create, task-assignee, and created-task-row persistence.
- `backend/services/task_service.py` — delegates only the task-create persistence operation through `TaskRepository` while retaining validation, contact resolution, response projection, audit, and transaction behavior.
- `backend/test_main.py` — adds HTTP/database/audit regression coverage for a multiple-assignee task creation response and persistence result.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused task-create regression: `python -m unittest test_main.CalendarApiTests.test_task_create_preserves_multiple_assignees_and_audit_result -v` (from `backend`): **PASS** — 1 test in **1.473s**. It covers the unchanged `201` task response, multiple assignees, persisted task and assignment rows, and `TASK_CREATED` audit record.
- Static/boundary verification: `python -m compileall -q app/main.py services/task_service.py repositories/task_repository.py test_main.py`; a create-operation repository-delegation/extracted-SQL-absence assertion; and `git diff --check`: **PASS**.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...task-create repository boundary..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **114.497s**; JavaScript syntax, Python compilation, extracted-SQL boundary, SQL-free task router, and whitespace checks passed.

Risk:
- `TaskService` still contains task update/delete, attachment, image, calendar, and listing SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/task_repository.py`, `backend/services/task_service.py`, and `backend/test_main.py`. The changed-path sensitive-file scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move the task-update write/read persistence into `TaskRepository`, then run focused task-update/authorization coverage and the full regression suite.

## Codex Execution PRD — task-update repository persistence slice (2026-08-06 20:06:34 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: Task/Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.update_task` operation and moved only the task-update write, notification-outbox invalidation, optional task-assignee replacement, and updated-task row lookup from `TaskService.update_task` into it.
- Preserved `PATCH /api/tasks/{task_id}` URL/status/request-response schema; existing task authorization, active-assignee and date/status validation; contact/master/audit transaction behavior; notification invalidation behavior; multi-assignee replacement; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `TaskService.update_task` delegates the extracted persistence to `TaskRepository`; its update operation no longer contains the extracted task update, notification-outbox delete, or task-assignee insert/delete SQL. The application still has exactly one `PATCH /api/tasks/{task_id}` and one `POST /api/tasks` route, and `routers/tasks.py` remains SQL-free.

Modified Files:
- `backend/repositories/task_repository.py` — adds task-update, outbox-refresh, optional assignee-replacement, and updated-row persistence.
- `backend/services/task_service.py` — delegates only task-update persistence through `TaskRepository` while retaining authorization, validation, task-view, audit, and transaction behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused task-update regressions: `python -m unittest test_main.CalendarApiTests.test_task_detail_update_history_and_deletion_authorization test_main.CalendarApiTests.test_due_dates_local_notification_outbox_preferences_and_authorization -v` (from `backend`): **PASS** — 2 tests in **6.600s**. They cover authorized updates, history/audit, deletion authorization, due-date update/clearing, and local-notification outbox refresh behavior.
- Static/boundary verification: `node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...AST-scoped update-task repository boundary and route assertions..." && ! grep -nE 'SELECT|INSERT|UPDATE|DELETE|\\.execute\\(' routers/tasks.py && git diff --check` (from `backend`): **PASS**.
- Full regression: `python -m unittest discover -s . -p 'test*.py' -v` (from `backend`): **PASS** — all **29 tests** passed in **99.155s**. JavaScript syntax, Python compilation, task-update repository-boundary assertions, unchanged task-route contract, SQL-free task router, and whitespace checks then passed in the static/boundary verification above.

Risk:
- `TaskService` still contains task delete, attachment, image, calendar, and listing SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/task_repository.py` and `backend/services/task_service.py`. A changed-path sensitive-file scan is required before commit; database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, and secret files must remain excluded.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move the task soft-delete/outbox-cleanup persistence into `TaskRepository`, then run focused deletion/authorization coverage and the full regression suite.

## Codex Execution PRD — task soft-delete repository persistence slice (2026-08-06 20:22:26 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: Task/Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.soft_delete_task` operation and moved only the task soft-delete write and local notification-outbox cleanup from `TaskService.delete_task` into it.
- Preserved `DELETE /api/tasks/{task_id}` URL/status/response schema; administrator and forced-password-change dependency; existing task lookup/authorization; `deleted_at`, `deleted_by`, and `updated_at` values; notification cleanup; `TASK_DELETED` audit action/before payload/actor/IP behavior; transaction behavior; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `TaskService.delete_task` delegates the extracted persistence to `TaskRepository`; the extracted task update and notification-outbox delete SQL are absent from the delete operation. The application still registers 44 routes with exactly one `DELETE /api/tasks/{task_id}` route, and `routers/tasks.py` remains SQL-free.

Modified Files:
- `backend/repositories/task_repository.py` — adds soft-delete and notification-outbox cleanup persistence.
- `backend/services/task_service.py` — delegates only task deletion persistence through `TaskRepository` while retaining authorization, task view, audit, and transaction behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused deletion/notification regressions: `python -m unittest test_main.CalendarApiTests.test_task_detail_update_history_and_deletion_authorization test_main.CalendarApiTests.test_due_dates_local_notification_outbox_preferences_and_authorization -v` (from `backend`): **PASS** — 2 tests in **6.413s**. They cover administrator task deletion authorization/history and local due-notification outbox behavior.
- Full regression: `python -m unittest discover -s . -p 'test*.py' -v` (from `backend`): **PASS** — all **29 tests** passed in **96.102s**.
- Static/contract verification: `node --check ../web/app.js`; Python compilation; application title/44-route/single-delete-route assertion; AST-scoped delete-service repository-delegation/query-absence assertion; SQL-free task-router check; and `git diff --check`: **PASS**.

Risk:
- `TaskService` still contains task listing, calendar, image, and attachment SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/task_repository.py` and `backend/services/task_service.py`. The changed-path sensitive-file scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move the task image count/upload persistence into `TaskRepository`, then run focused image authorization coverage and the full regression suite.

## Codex Execution PRD — task-list repository persistence slice (2026-08-06 20:40:11 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: Task/Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.list_tasks` operation and moved only the authorized task-list query composition, count, status summary, ordering, pagination, and row retrieval from `TaskService.list_tasks` into it.
- Preserved `GET /api/tasks` URL/status/request-response schema; date-range and member assignee-filter validation; server-side administrator/member task visibility; status, received-date, due-date, assignee, and keyword filters; status-first ordering; pagination metadata; status summary; task-view projection; transaction behavior; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `TaskService.list_tasks` delegates the extracted database work to `TaskRepository`; the service list operation contains no `.execute(` call. `routers/tasks.py` remains SQL-free.

Modified Files:
- `backend/repositories/task_repository.py` — adds task-list query, visibility scope, aggregate, ordering, pagination, and row-retrieval persistence.
- `backend/services/task_service.py` — delegates only list persistence through `TaskRepository` while retaining input validation and task response projection.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused task-list regression: `python -m unittest test_main.CalendarApiTests.test_task_list_server_filters_pagination_and_calendar_month_validation -v && python -m compileall -q app/main.py services/task_service.py repositories/task_repository.py test_main.py && git diff --check` (from `backend`): **PASS** — 1 test in **2.386s**. It exercises server-side filtering, pagination, summary metadata, and calendar validation; compilation and whitespace validation passed.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...AST-scoped task-list repository delegation/query-absence and SQL-free router assertions..." && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **95.551s**; JavaScript syntax, Python compilation, task-list repository boundary, SQL-free task router, and whitespace checks passed.

Risk:
- `TaskService` still contains calendar, image, and attachment SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/task_repository.py` and `backend/services/task_service.py`. The changed-path sensitive-file scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move the received-date calendar row retrieval into `TaskRepository`, then run focused calendar visibility coverage and the full regression suite.

## Codex Execution PRD — received-date calendar repository persistence slice (2026-08-06 20:57:04 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: Task image/attachment persistence plus Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.received_date_calendar` operation and moved only the authorized received-date calendar row query from `TaskService.get_received_date_calendar` into it.
- Preserved `GET /api/calendar` URL/status/request-response schema; existing strict `YYYY-MM` validation; all-status received-date behavior and ordering; server-side administrator/member task visibility; task response projection; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `TaskService.get_received_date_calendar` delegates row retrieval to `TaskRepository` and contains no `.execute(` call. The application still registers 44 routes with exactly one `GET /api/calendar` and one `GET /api/tasks` route; `routers/tasks.py` remains SQL-free.

Modified Files:
- `backend/repositories/task_repository.py` — adds authorized received-date calendar persistence.
- `backend/services/task_service.py` — delegates only received-date calendar row retrieval through `TaskRepository`.
- `backend/app/main.py` — removes the no-longer-needed calendar SQL helper dependency from task-service composition without changing routes.
- `backend/test_main.py` — extends direct API authorization regression coverage to confirm a member cannot enumerate another member's task through the calendar.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused calendar authorization and behavior regression: `python -m unittest test_main.CalendarApiTests.test_member_cannot_see_other_members_task test_main.CalendarApiTests.test_task_list_server_filters_pagination_and_calendar_month_validation -v && python -m compileall -q app/main.py services/task_service.py repositories/task_repository.py routers/tasks.py test_main.py && git diff --check` (from `backend`): **PASS** — 2 tests in **4.086s**; compilation and whitespace validation passed.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python - <<'PY' ...calendar repository-boundary, SQL-free router, and 44-route contract assertions... PY && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **93.789s**; JavaScript syntax, Python compilation, one-calendar-route/one-task-route contract, extracted-SQL boundary, SQL-free task router, and whitespace checks passed.

Risk:
- `TaskService` still contains task image and attachment SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/app/main.py`, `backend/repositories/task_repository.py`, `backend/services/task_service.py`, and `backend/test_main.py`. A changed-path sensitive-file scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move task image-count/upload persistence into `TaskRepository`, then run focused image authorization coverage and the full regression suite.

## Codex Execution PRD — task image-upload repository persistence slice (2026-08-06 21:12:33 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task attachment persistence plus Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.image_count` and `TaskRepository.create_task_image` operations, and moved only the existing task-image count plus metadata insert/read persistence from `TaskService.upload_task_images` into them.
- Preserved the `POST /api/tasks/{task_id}/images` URL/status/request-response schema; existing task authorization; image MIME/signature and size validation; five-image limits and database trigger behavior; private file creation/cleanup/modes; image response projection; audit behavior; transaction/rollback behavior; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `TaskService.upload_task_images` delegates image count and metadata persistence to `TaskRepository`; its scoped upload operation no longer contains the extracted `SELECT COUNT(*) FROM task_images`, `INSERT INTO task_images`, or created-image `SELECT` SQL. `routers/tasks.py` remains SQL-free.

Modified Files:
- `backend/repositories/task_repository.py` — adds task-image count and metadata create/read persistence.
- `backend/services/task_service.py` — delegates only task-image upload persistence through `TaskRepository` while retaining validation, private-file lifecycle, authorization, audit, and transaction behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused image authorization/upload regression: `python -m unittest test_main.CalendarApiTests.test_private_image_upload_validation_authorization_and_deletion -v && python -m compileall -q app/main.py services/task_service.py repositories/task_repository.py routers/tasks.py test_main.py && git diff --check` (from `backend`): **PASS** — 1 test in **2.964s**. It covers unauthorized upload/download/deletion rejection, MIME/signature validation, private delivery headers, uploaded image detail/history/audit behavior, and the per-task image limit.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...AST-scoped image-upload repository delegation/query-absence and SQL-free router assertions..." && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **96.152s**; JavaScript syntax, Python compilation, image repository boundary, SQL-free task router, and whitespace checks passed.

Risk:
- `TaskService` still contains task attachment, image retrieval/edit/delete, and history SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/task_repository.py` and `backend/services/task_service.py`. The changed-path sensitive-file scan must include this progress file before commit; database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, and secret files must remain excluded.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move task attachment count/upload persistence into `TaskRepository`, then run focused attachment authorization coverage and the full regression suite.

## Codex Execution PRD — task attachment-upload repository persistence slice (2026-08-06 21:28:21 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task attachment retrieval/deletion, image retrieval/edit/delete, and history persistence plus Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.attachment_count` and `TaskRepository.create_task_attachment` operations, and moved only the existing task-attachment count plus metadata insert/read persistence from `TaskService.upload_task_attachments` into them.
- Preserved the `POST /api/tasks/{task_id}/attachments` URL/status/request-response schema; existing task authorization before private-byte inspection; document/video MIME/signature and size validation; ten-attachment limits and database trigger behavior; private file creation/cleanup/modes; attachment response projection; SHA-256 metadata; audit behavior; transaction/rollback behavior; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `TaskService.upload_task_attachments` delegates attachment count and metadata persistence to `TaskRepository`; its scoped upload operation no longer contains the extracted `SELECT COUNT(*) FROM task_attachments`, attachment `INSERT`, or created-attachment `SELECT` SQL. `routers/tasks.py` remains SQL-free.

Modified Files:
- `backend/repositories/task_repository.py` — adds task-attachment count and metadata create/read persistence.
- `backend/services/task_service.py` — delegates only task-attachment upload persistence through `TaskRepository` while retaining validation, private-file lifecycle, authorization, SHA-256 calculation, audit, and transaction behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused attachment authorization/upload regression: `python -m unittest test_main.CalendarApiTests.test_private_document_video_attachment_validation_authorization_and_deletion -v && python -m compileall -q app/main.py services/task_service.py repositories/task_repository.py routers/tasks.py test_main.py && python - <<'PY' ...AST-scoped attachment-upload repository delegation/query-absence and 44-route attachment contract assertions... PY && git diff --check` (from `backend`): **PASS** — 1 test in **2.899s**. It covers unauthorized upload/download/deletion rejection, MIME/signature validation, private download headers, uploaded attachment detail/history/audit behavior, and deletion.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python - <<'PY' ...attachment repository boundary, SQL-free task router, and 44-route contract assertions... PY && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **95.659s**; JavaScript syntax, Python compilation, attachment repository boundary, SQL-free task router, route contract, and whitespace checks passed.

Risk:
- `TaskService` still contains task attachment retrieval/deletion, image retrieval/edit/delete, and history SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/task_repository.py` and `backend/services/task_service.py`. The changed-path sensitive-file scan must include this progress file before commit; database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, and secret files must remain excluded.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move authorized task-attachment retrieval/deletion persistence into `TaskRepository`, then run focused attachment authorization coverage and the full regression suite.

## Codex Execution PRD — task attachment retrieval/deletion repository persistence slice (2026-08-06 21:46:22 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task image retrieval/edit/delete and history persistence plus Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.task_attachment` and `TaskRepository.delete_task_attachment` operations, and moved only the authorized task-attachment metadata lookup and metadata delete from `TaskService.download_task_attachment` and `TaskService.delete_task_attachment` into them.
- Preserved `GET /api/tasks/{task_id}/attachments/{attachment_id}` and `DELETE /api/tasks/{task_id}/attachments/{attachment_id}` URLs/status/request-response schemas; authorization before metadata and private-byte access; 404 behavior; forced private-download headers; private file removal after the database transaction; attachment projection; audit behavior; transaction behavior; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- The two attachment retrieval/deletion service operations delegate the extracted persistence to `TaskRepository` and contain no `connection.execute(` call. `routers/tasks.py` remains SQL-free; it has exactly one GET and one DELETE attachment route.

Modified Files:
- `backend/repositories/task_repository.py` — adds task-attachment metadata lookup and deletion persistence.
- `backend/services/task_service.py` — delegates only attachment download/delete persistence through `TaskRepository` while retaining authorization, private-file lifecycle, response headers, and audit behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused attachment authorization/download/deletion regression: `python -m unittest test_main.CalendarApiTests.test_private_document_video_attachment_validation_authorization_and_deletion -v` (from `backend`): **PASS** — 1 test in **3.041s**. It covers unauthorized upload/download/deletion rejection, MIME/signature validation, private download headers, attachment detail/history/audit behavior, and deletion.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...attachment retrieval/deletion repository boundary, SQL-free router, and single GET/DELETE attachment-route assertions..." && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **93.884s**; JavaScript syntax, Python compilation, repository-boundary, SQL-free router, attachment-route contract, and whitespace checks passed.

Risk:
- `TaskService` still contains task image retrieval/edit/delete and history SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/task_repository.py` and `backend/services/task_service.py`. The changed-path sensitive-file scan must include this progress file before commit; database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, and secret files must remain excluded.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move authorized task-image retrieval persistence into `TaskRepository`, then run focused image authorization coverage and the full regression suite.

## Codex Execution PRD — task image retrieval repository persistence slice (2026-08-06 22:04:17 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task image edit/delete and history persistence plus Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.task_image` operation and moved only the authorized task-image metadata lookup from `TaskService.get_task_image` into it.
- Preserved `GET /api/tasks/{task_id}/images/{image_id}` URL/status/request-response schema; authorization before metadata and private-byte access; 404 behavior; private-image response MIME type and `Cache-Control`/`X-Content-Type-Options` headers; private file behavior; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `TaskService.get_task_image` delegates metadata lookup to `TaskRepository` and contains no `connection.execute(` call. `routers/tasks.py` remains SQL-free; the application retains exactly one GET and one DELETE route at the unchanged image item URL.

Modified Files:
- `backend/repositories/task_repository.py` — adds task-image metadata lookup persistence.
- `backend/services/task_service.py` — delegates only private-image retrieval persistence through `TaskRepository` while retaining authorization, private-file lifecycle, response headers, and error behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused image authorization/download regression: `python -m unittest test_main.CalendarApiTests.test_private_image_upload_validation_authorization_and_deletion -v && python -m compileall -q app/main.py services/task_service.py repositories/task_repository.py routers/tasks.py test_main.py && python -c "...AST-scoped task-image retrieval repository delegation/query-absence assertions..." && git diff --check` (from `backend`): **PASS** — 1 test in **3.056s**; compilation, repository-boundary, and whitespace checks passed. It covers unauthorized upload/download/deletion rejection, MIME/signature validation, private delivery headers, image detail/history/audit behavior, and the per-task image limit.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...task-image retrieval repository boundary, SQL-free task router, and GET/DELETE image-route contract assertions..." && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **94.605s**; JavaScript syntax, Python compilation, repository boundary, SQL-free task router, image-route contract, and whitespace checks passed.

Risk:
- `TaskService` still contains task image edit/delete and history SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/task_repository.py` and `backend/services/task_service.py`. The changed-path sensitive-file scan must include this progress file before commit; database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, and secret files must remain excluded.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move authorized task-image edit/revision persistence into `TaskRepository`, then run focused image-edit authorization coverage and the full regression suite.

## Codex Execution PRD — task image-edit/revision repository persistence slice (2026-08-06 22:19:28 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task image deletion and history persistence plus Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.revise_task_image` operation and moved only the existing task-image revision insert, image metadata update, and updated-image read from `TaskService.edit_task_image` into it. The pre-existing image lookup now reuses `TaskRepository.task_image`.
- Preserved `POST /api/tasks/{task_id}/images/{image_id}/edit` URL/status/request-response schema; authorization before private-byte access; 404 behavior; bounded image rotation; private revision file creation/cleanup/modes; non-destructive source retention; image response projection; audit behavior; transaction/rollback behavior; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `TaskService.edit_task_image` delegates all task-image persistence to `TaskRepository` and contains no `.execute(` call. `routers/tasks.py` remains SQL-free; image edit and item-route URLs remain unchanged.

Modified Files:
- `backend/repositories/task_repository.py` — adds non-destructive image-revision persistence.
- `backend/services/task_service.py` — delegates only image lookup/revision persistence while retaining authorization, private-file lifecycle, transform, response, and audit behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused image-edit authorization/revision regression: `python -m unittest test_main.CalendarApiTests.test_private_image_rotation_is_authorized_non_destructive_and_audited -v && python -m compileall -q app/main.py services/task_service.py repositories/task_repository.py routers/tasks.py test_main.py && python -c "...AST-scoped image-edit query-absence and repository-operation assertions..." && git diff --check` (from `backend`): **PASS** — 1 test in **2.791s**; compilation, repository-boundary, and whitespace checks passed. It covers unauthorized editing rejection, rendered rotation, non-destructive source retention, audit/history, and cleanup on deletion.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...AST-scoped image-edit repository boundary and SQL-free task router assertions..." && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **97.697s**; JavaScript syntax, Python compilation, repository boundary, SQL-free task router, and whitespace checks passed.

Risk:
- `TaskService` still contains task image deletion and history SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/task_repository.py` and `backend/services/task_service.py`. These source paths and this progress file contain no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move authorized task-image deletion persistence into `TaskRepository`, then run focused image authorization/deletion coverage and the full regression suite.

## Codex Execution PRD — task image-deletion repository persistence slice (2026-08-06 22:35:03 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: task history plus Dashboard/Notification/Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the small persistence-only `TaskRepository.delete_task_image` operation and moved only the task-image revision-source-key lookup and task-image metadata deletion from `TaskService.delete_task_image` into it. The existing authorized metadata lookup continues through `TaskRepository.task_image`.
- Preserved `DELETE /api/tasks/{task_id}/images/{image_id}` URL/status/response schema; authorization before metadata and private-byte access; 404 behavior; removal of the current and retained revision-source private files after the database transaction; audit behavior; transaction behavior; SQLCipher behavior; database schema/data; DPAPI/key material; uploads; secrets; `.env`; notification delivery; deployment; and external-service behavior.
- `TaskService.delete_task_image` now delegates all task-image persistence to `TaskRepository` and contains no `.execute(` call. `routers/tasks.py` remains SQL-free.

Modified Files:
- `backend/repositories/task_repository.py` — adds task-image revision-source lookup and metadata deletion persistence.
- `backend/services/task_service.py` — delegates only image-deletion persistence while retaining authorization, private-file lifecycle, response, and audit behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused image deletion/revision regression: `python -m unittest test_main.CalendarApiTests.test_private_image_upload_validation_authorization_and_deletion test_main.CalendarApiTests.test_private_image_rotation_is_authorized_non_destructive_and_audited -v && python -m compileall -q app/main.py services/task_service.py repositories/task_repository.py routers/tasks.py test_main.py && python -c "...AST-scoped image-delete query-absence and repository-delegation assertions..." && git diff --check` (from `backend`): **PASS** — 2 tests in **5.095s**; compilation, repository-boundary, and whitespace checks passed. It covers unauthorized image deletion, 404 behavior after deletion, audit behavior, non-destructive revision-source retention before deletion, and current/revision-source private-file cleanup after deletion.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...AST-scoped image-delete repository boundary and SQL-free task router assertions..." && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **95.003s**; JavaScript syntax, Python compilation, image-deletion repository boundary, SQL-free task router, and whitespace checks passed.

Risk:
- `TaskService` still contains task history SQL; `DashboardService`, `NotificationService`, and `MasterService` also still contain repository SQL. The PRD requirement that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/task_repository.py` and `backend/services/task_service.py`. The changed-path sensitive-file scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving TaskService slice: move authorized task-history persistence into `TaskRepository`, then run focused task-history authorization coverage and the full regression suite.

## Codex Execution PRD — task-history repository persistence slice (2026-08-06 22:56:04 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before this slice. Completion conditions remain unmet: Dashboard, Notification, and Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the persistence-only `TaskRepository.task_history_rows` operation and moved only the task audit-history query from `app.main.task_history` into it. JSON parsing, field-change labeling, returned rows/order, and every existing HTTP route/schema remain unchanged.
- Preserved task-detail authorization, audit-history rendering, SQLCipher transaction behavior, database schema/data, uploads, DPAPI/key material, credentials, `.env`, notifications, deployment, and external-service behavior. No database or private-upload file was changed.

Modified Files:
- `backend/repositories/task_repository.py` — adds the legacy-ordered task audit-history persistence query.
- `backend/app/main.py` — delegates only task-history persistence to `TaskRepository`.
- `PROGRESS.md` — this verified slice record.

Tests:
- Full verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/app/main.py backend/services/task_service.py backend/repositories/task_repository.py backend/routers/tasks.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...AST-scoped task-history query-absence and repository-operation assertions..." && git diff --check`: **PASS** — all **29 tests** passed in **95.845s**; JavaScript syntax, Python compilation, task-history repository boundary, and whitespace checks passed. This includes task-detail/history/deletion authorization coverage plus isolated rendered Chromium task-detail coverage.

Risk:
- `DashboardService`, `NotificationService`, and `MasterService` still contain SQL. The Codex PRD condition that SQL reside only in repositories remains unfulfilled; `app/main.py` also remains above the recommended 50 lines.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/app/main.py` and `backend/repositories/task_repository.py`. The changed-path scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving DashboardService slice: move the authorized statistics aggregates into `DashboardRepository`, then run focused statistics authorization coverage and the full regression suite.

## Codex Execution PRD — dashboard statistics repository persistence slice (2026-08-06 23:12:45 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: Dashboard completed-calendar/export, Notification, and Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added persistence-only `DashboardRepository.statistics_rows` and moved the authorized statistics status and per-assignee aggregate queries from `DashboardService.statistics` into it.
- Preserved `GET /api/statistics` URL, request/response schema, status aggregation, per-user ordering, active-state projection, member visibility scope, member assignee-filter restriction, validation status/messages, database schema/data, SQLCipher transaction behavior, uploads, DPAPI/key material, credentials, `.env`, notification delivery, deployment, and external-service behavior.
- `DashboardService.statistics` now delegates aggregate persistence to `DashboardRepository` and contains zero `.execute(` calls; `routers/dashboard.py` remains SQL-free. The completed-calendar and XLSX-export SQL remains deliberately unchanged for later small slices.

Modified Files:
- `backend/repositories/dashboard_repository.py` — adds authorized statistics aggregation persistence.
- `backend/services/dashboard_service.py` — retains statistics validation/projection and delegates aggregate reads to `DashboardRepository`.
- `backend/app/main.py` — wires the dashboard repository into the existing dashboard service without changing routes.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused statistics regression: `python -m compileall -q app/main.py services/dashboard_service.py repositories/dashboard_repository.py && python -m unittest test_main.CalendarApiTests.test_statistics_scope_status_user_aggregation_and_validation -v` (from `backend`): **PASS** — 1 test in **2.011s**. It covers authorized status/user aggregation, date filtering, member visibility, member filter bypass rejection, and date-range validation.
- Full verification from the repository root: `python -m unittest discover -s backend -p 'test*.py' -v && node --check web/app.js && python -m compileall -q backend/app/main.py backend/services/dashboard_service.py backend/repositories/dashboard_repository.py backend/routers/dashboard.py backend/test_main.py backend/test_acceptance.py backend/test_browser_ui.py && python -c "...AST-scoped statistics query-absence and repository-operation assertions..." && git diff --check`: **PASS** — all **29 tests** passed in **93.560s**; JavaScript syntax, Python compilation, dashboard statistics repository boundary, and whitespace checks passed. This includes the Phase 1 acceptance workflow and rendered statistics-dashboard regression coverage.

Risk:
- `DashboardService` still contains completed-calendar and XLSX-export SQL; `NotificationService` and `MasterService` also still contain SQL. The Codex PRD condition that SQL reside only in repositories remains unfulfilled; `app/main.py` also remains above the recommended 50 lines.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/app/main.py`, `backend/services/dashboard_service.py`, and `backend/repositories/dashboard_repository.py`. The changed-path scan found no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path; none is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving DashboardService slice: move authorized completed-date report-calendar persistence into `DashboardRepository`, then run focused completed-calendar authorization coverage and the full regression suite.

## Codex Execution PRD — completed-date report-calendar repository persistence slice (2026-08-06 23:29:36 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: Dashboard XLSX-export, Notification, and Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the persistence-only `DashboardRepository.completed_calendar_rows` operation and moved only the authorized completed-date report-calendar task query from `DashboardService.completed_calendar` into it.
- Preserved `GET /api/completed-calendar` URL, month request/response schema, strict `YYYY-MM` validation, member and administrator visibility scope, completed-status and completed-date month filtering, legacy completed-date/id ordering, task-view response projection, database schema/data, SQLCipher transaction behavior, uploads, DPAPI/key material, credentials, `.env`, notification delivery, deployment, and external-service behavior.
- `DashboardService.completed_calendar` now delegates row retrieval to `DashboardRepository` and contains no `connection.execute(` call; `routers/dashboard.py` remains SQL-free and retains exactly one completed-calendar route.

Modified Files:
- `backend/repositories/dashboard_repository.py` — adds authorized completed-date calendar row persistence.
- `backend/services/dashboard_service.py` — delegates only completed-date calendar persistence while retaining validation and response projection.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused completed-calendar regression: `python -m compileall -q app/main.py services/dashboard_service.py repositories/dashboard_repository.py routers/dashboard.py && python -m unittest test_main.CalendarApiTests.test_completed_date_report_calendar_uses_task_scope_and_month_validation -v && git diff --check` (from `backend`): **PASS** — 1 test in **2.156s**; Python compilation and whitespace validation passed. It covers member scope, administrator scope, completed-month filtering, and invalid month rejection.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python - <<'PY' ...AST-scoped completed-calendar repository-delegation/query-absence plus SQL-free dashboard-router/single-route assertions... PY && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **95.449s**; JavaScript syntax, Python compilation, completed-calendar repository boundary, SQL-free dashboard router, completed-calendar route contract, and whitespace checks passed.

Risk:
- `DashboardService` still contains XLSX-export SQL; `NotificationService` and `MasterService` also still contain SQL. The Codex PRD condition that SQL reside only in repositories remains unfulfilled; `app/main.py` also remains above the recommended 50 lines.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/repositories/dashboard_repository.py` and `backend/services/dashboard_service.py`. The changed-path sensitive-file scan passed: no database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving DashboardService slice: move authorized XLSX-export task-row retrieval into `DashboardRepository`, then run focused export authorization coverage and the full regression suite.

## Codex Execution PRD — XLSX-export repository persistence slice (2026-08-06 23:46:23 UTC)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: Notification and Master service SQL remains outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `main.py` minimization remain pending.
- Added the persistence-only `DashboardRepository.export_task_rows` operation and moved only the authorized XLSX task-row query from `DashboardService.export_tasks_xlsx` into it.
- Preserved `GET /api/tasks/export.xlsx` URL, request/response schema, private/no-store download headers, status/date/due-date/assignee/keyword filtering, administrator and member visibility scope, member assignee-filter restriction, result ordering, 10,000-row limit, spreadsheet-safe rendering, audit data, validation status/messages, database schema/data, SQLCipher transaction behavior, uploads, DPAPI/key material, credentials, `.env`, notification delivery, deployment, and external-service behavior.
- `DashboardService.export_tasks_xlsx` delegates row retrieval to `DashboardRepository` and contains no `.execute(` call; `routers/dashboard.py` remains SQL-free and retains the XLSX route contract.

Modified Files:
- `backend/repositories/dashboard_repository.py` — adds authorized XLSX task-row retrieval.
- `backend/services/dashboard_service.py` — delegates only export-row persistence while retaining validation, workbook rendering, and audit behavior.
- `backend/app/main.py` — wires the existing dashboard service to its simplified constructor without changing routes.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused XLSX-export regression: `python -m compileall -q app/main.py services/dashboard_service.py repositories/dashboard_repository.py routers/dashboard.py test_main.py && python -m unittest test_main.CalendarApiTests.test_excel_export_matches_authorized_filtered_scope_and_is_spreadsheet_safe -v && python - <<'PY' ...AST-scoped export query-absence/repository-operation and SQL-free-router assertions... PY && git diff --check` (from `backend`): **PASS** — 1 test in **2.544s**; compilation, repository-boundary, route-contract, and whitespace checks passed. It covers authorized filtered scope, private response headers, spreadsheet formula escaping, member filter-bypass rejection, date-range validation, and export audit logging.
- Full verification: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python - <<'PY' ...AST-scoped export repository-delegation/query-absence plus SQL-free dashboard-router assertions... PY && git diff --check` (from `backend`): **PASS** — all **29 tests** passed in **92.357s**; JavaScript syntax, Python compilation, XLSX repository boundary, SQL-free dashboard router, and whitespace checks passed. This includes the Phase 1 acceptance workflow and rendered XLSX-download regression coverage.

Risk:
- `NotificationService` and `MasterService` still contain SQL, while `app/main.py` remains above the recommended 50 lines. The Codex PRD condition that SQL reside only in repositories remains unfulfilled.
- Before this progress update, `git status --short --untracked-files=all` listed only `backend/app/main.py`, `backend/repositories/dashboard_repository.py`, and `backend/services/dashboard_service.py`. The changed-path sensitive-file scan must include this progress file before commit; database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, and secret files must remain excluded.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving NotificationService slice: move local notification-preference persistence into a repository, then run focused notification authorization coverage and the full regression suite.

## Codex Execution PRD — notification-preference repository persistence slice (2026-08-07)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: the remaining notification outbox queries and all Master service SQL remain outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `app/main.py` minimization remain pending.
- Added the persistence-only `NotificationRepository.preference` operation and moved only lazy notification-preference creation/read from `NotificationService._preferences` into it.
- Preserved `GET/PATCH /api/me/notification-preferences` URLs, request/response schema, default enabled values, lazy record creation, update and audit behavior, local-only delivery marker, authorization, SQLCipher transaction behavior, database schema/data, uploads, DPAPI/key material, credentials, `.env`, notification delivery, deployment, and external-service behavior.
- `NotificationService._preferences` now delegates its persistence operation to `NotificationRepository`; `routers/notifications.py` remains SQL-free.

Modified Files:
- `backend/repositories/notification_repository.py` — adds lazy notification-preference persistence.
- `backend/services/notification_service.py` — delegates only lazy preference creation/read to the repository.
- `backend/app/main.py` — wires the existing notification service to its repository without changing routes.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused notification-preference regression from `backend`: `python -m compileall -q app/main.py services/notification_service.py repositories/notification_repository.py routers/notifications.py && python -c "...AST-scoped preference query-absence and repository-operation assertions..." && python -c "...isolated HTTP preference default/update/read regression..." && git diff --check`: **PASS** — compilation, repository-boundary, endpoint default/update/read behavior, and whitespace checks passed.
- Full verification from `backend`: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...AST-scoped preference repository-boundary and SQL-free notification-router assertions..." && git diff --check`: **PASS** — all **29 tests** passed in **107.037s**; JavaScript syntax, Python compilation, notification-preference repository boundary, SQL-free notification router, and whitespace checks passed. This includes due-date/local notification outbox preference and authorization coverage.

Risk:
- `NotificationService` still contains local outbox refresh/list/read/update persistence SQL, and `MasterService` still contains SQL. The Codex PRD condition that SQL reside only in repositories remains unfulfilled; `app/main.py` also remains above the recommended 50 lines.
- The verified changed paths are source files plus this progress record. No database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, or secret path is included.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving NotificationService slice: move notification-preference update and disabled-kind local outbox cleanup into `NotificationRepository`, then run focused due-date notification authorization coverage and the full regression suite.

## Codex Execution PRD — notification-preference update repository persistence slice (2026-08-07)
Completed:
- Re-read `PROGRESS.md` and the authoritative `docs/Codex_Execution_PRD_backend_refactoring.md` before starting this slice. Completion conditions remain unmet: notification outbox refresh/list/read persistence and all Master service SQL remain outside repositories; global exception handling, response helpers, validator/middleware/notification/scheduler layering, and further `app/main.py` minimization remain pending.
- Added the persistence-only `NotificationRepository.update_preferences` operation and moved only notification-preference update plus disabled due-soon/overdue local-outbox cleanup from `NotificationService.update_preferences` into it.
- Preserved `PATCH /api/me/notification-preferences` URL, request/response schema, default/lazy preference behavior, update ordering, audit behavior, due-soon and overdue disabled-kind cleanup, local-only delivery marker, authorization, SQLCipher transaction behavior, database schema/data, uploads, DPAPI/key material, credentials, `.env`, notification delivery, deployment, and external-service behavior.
- `NotificationService.update_preferences` now delegates all of its persistence to `NotificationRepository`; `routers/notifications.py` remains SQL-free.

Modified Files:
- `backend/repositories/notification_repository.py` — adds notification preference update and disabled-kind local-outbox cleanup persistence.
- `backend/services/notification_service.py` — delegates only preference update/cleanup persistence while retaining response and audit behavior.
- `PROGRESS.md` — this verified slice record.

Tests:
- Focused notification-preference regression from `backend`: `python -m compileall -q services/notification_service.py repositories/notification_repository.py routers/notifications.py app/main.py && python -m unittest test_main.CalendarApiTests.test_due_dates_local_notification_outbox_preferences_and_authorization -v && python -c "...AST-scoped update-preference query-absence and repository-operation assertions..." && git diff --check`: **PASS** — 1 test in **4.790s**; compilation, endpoint authorization/default/update/read behavior, repository-boundary, and whitespace checks passed.
- Full verification from `backend`: `python -m unittest discover -s . -p 'test*.py' -v && node --check ../web/app.js && python -m compileall -q main.py app/main.py routers services repositories schemas database.py core test_main.py test_acceptance.py test_browser_ui.py && python -c "...AST-scoped update-preference repository-boundary and SQL-free notification-router assertions..." && git diff --check`: **PASS** — all **29 tests** passed in **101.835s**; JavaScript syntax, Python compilation, notification preference update repository boundary, SQL-free notification router, and whitespace checks passed. This includes Phase 1 acceptance, due-date/local outbox preference and authorization, rendered notification behavior, statistics, completed-calendar, and XLSX regressions.

Risk:
- `NotificationService` still contains local outbox refresh/list/read persistence SQL, and `MasterService` still contains SQL. The Codex PRD condition that SQL reside only in repositories remains unfulfilled; `app/main.py` also remains above the recommended 50 lines.
- The verified changed paths are source files plus this progress record. A final changed-path sensitive-file scan is required before committing; database, DPAPI/key, certificate, `.env`, plaintext backup, private-upload, and secret files must remain excluded.

Next Phase:
- Continue the repository phase with the smallest remaining behavior-preserving NotificationService slice: move local outbox read-mark persistence into `NotificationRepository`, then run focused notification authorization coverage and the full regression suite.
