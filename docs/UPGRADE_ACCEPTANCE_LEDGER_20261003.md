# UPGRADE ACCEPTANCE LEDGER

| ID | Description | Source | Test | Log | Status |
|---|---|---|---|---|---|
| UPG-BASE-001 | 기준 계약과 증거 원장 | backend/main.py, web/app.js, backend/fixtures/upg_base_contract.json | backend/test_upg_base_001.py, backend/test_browser_ui.py | C:/Users/HODI/AppData/Local/hermes/automation/calendar-upgrade-20261007-codex-aipro/runs/001-upg-base-001/attempt-7/checkpoint.json | IN_PROGRESS |
| UPG-PERF-001 | 읽기 성능과 경계 회귀 | backend/main.py | backend/test_upg_perf_001.py | - | NOT_STARTED |
| UPG-UX-001 | 프런트 공통 요청과 화면 수명 | web/app.js | - | - | NOT_STARTED |
| UPG-UX-002 | 사용자별 보드의 제한된 요청과 로딩 | web/app.js | backend/test_browser_ui.py | - | IN_PROGRESS |
| UPG-UX-003 | 사용자별 필터 복원과 저장 보기 | - | - | - | NOT_STARTED |
| UPG-CAL-001 | 실제 요일 월간 보기와 주간 보기 | - | - | - | NOT_STARTED |
| UPG-TASK-001 | 입력·저장 안정성과 상세 복귀 | - | - | - | NOT_STARTED |
| UPG-FILE-001 | 비공개 첨부의 수명과 오류 처리 | - | - | - | NOT_STARTED |
| UPG-OPS-001 | 알림·통계·내보내기 연결성 | - | - | - | NOT_STARTED |
| UPG-SEC-001 | 현재 권한·보안의 부정 경로 | - | - | - | NOT_STARTED |
| UPG-RUN-001 | 재현 환경과 완전한 검증 명령 | - | - | - | NOT_STARTED |
| UPG-OPS-002 | 운영 진단과 복구 준비 | - | - | - | NOT_STARTED |
| UPG-E2E-001 | 실서비스 통합·반응형 수용 | - | - | - | NOT_STARTED |
| UPG-DONE-001 | 최종 재검증과 종료 | - | - | - | NOT_STARTED |

### PROGRESS
Observed failures regarding duplicate `\\?\` prefix and Playwright download cancelation in actual namespaced test environments. Repairs for idempotence and explicit browser `downloads_path` have been implemented and are currently UNDER_VERIFICATION. Driver attempt-5 prepared.
