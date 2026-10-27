# 공유 업무 캘린더 고도화 PRD — AI Pro 연속 개발

- 승인 근거: 2026-10-03 사용자의 고도화 PRD 생성, AI Pro 기반 개발, 프로젝트 최상위 권한 및 별도 재실행 없이 완료까지 지속 개발 요청.
- 제품: 기존 SQLite/SQLCipher 공유 업무 캘린더. 재작성·신규 서비스가 아니라 현재 제품의 기능·사용성·안전성 개선이다.
- 원본: `E:\python\shared-work-calendar` (원본의 미커밋 `PROGRESS.md` 보존).
- 전용 작업공간: `E:\worktrees\shared-work-calendar\performance-20261003`.
- 브랜치: `ai-pro/calendar-performance-20261003`; 기준 HEAD: `a847c24e19f840e9478c54d3422eb7da4f1c0db9`.
- 구현: Antigravity CLI / Google AI Pro `gemini-3.1-pro-high`, 최고 추론 수준, 사용자 승인 전용 privileged 실행기.
- 검증: Conda `shared_calendar` / Python 3.11, 실제 Chromium, 독립 Hermes QA.
- 요구사항 상태의 원장: 저장소 밖 controller manifest/state와 실행 로그. 이 문서의 설명만으로 완료 판정하지 않는다.

## 1. 목표와 현재 확인된 사실

관리자와 일반 이용자가 업무를 등록·배정·처리하고 접수일/처리일 캘린더, 통계, 비공개 첨부, 로컬 알림함, XLSX를 사용하는 기존 제품을 유지한다. 이미 있는 기능을 새로 만들었다고 보고하지 않는다.

첫 성능 slice는 구현되어 변경 전 30개, 변경 후 43개 테스트 및 실제 Chromium 검증을 실행했다. 20건 업무의 관련정보 SELECT는 100회에서 5회로 감소했다. 이는 조회 수 증거이며 응답시간 개선률은 아직 측정하지 않았다. 독립 QA 완료 여부는 현재 전체 PRD 첫 단계에서 새 소스와 실행 증거로 다시 판정한다.

현재 UI에는 단일 파일에 밀집한 요청/화면 처리, 일반 오류와 인증 만료를 구분하지 않는 최상위 catch, 사용자·상태별 동시 요청 확장, 필터의 새로고침 복원 부재, 월 캘린더의 요일 배치와 주간 보기 부재 등이 개선 후보로 확인되었다. 나머지 후보는 구현 단계에서 재현하고, 이미 만족된 항목에는 증거를 남기며 불필요한 재작성을 하지 않는다.

## 2. 권한과 불변 계약

### 자동 승인 범위

- 이 전용 worktree의 제품 코드·문서·테스트·정적 자산 수정, 필요한 프로젝트 의존성 설치, 임시 fixture 생성, loopback 서버 실행·종료, 테스트·벤치마크·QA·재시도는 사용자 재확인 없이 수행한다.
- privileged AI Pro 실행은 `--dangerously-skip-permissions`를 명시적으로 사용하는 별도 이름의 controller에 한정한다. `--sandbox`는 유지한다. CLI 전역 설정, 다른 프로필·프로젝트의 권한은 바꾸지 않는다.
- 코드·인프라 오류를 자동 복구한다. 제한된 단발 실행 종료는 프로젝트 완료가 아니며 다음 slice 또는 수정 작업으로 이어진다.

### 보존 및 제외 범위

- 기존 API URL, 요청/응답 필드, ADMIN/MEMBER 권한, 상태 전환, 서버 권한 필터, 목록 정렬, 페이지네이션, 감사 로그와 DB 스키마를 보존한다. 추가 UI 보기와 프런트 내부 모듈화는 허용한다.
- 실제 제품 DB, DPAPI 키, 평문 복구본, 비공개 첨부, `.env`, 사용자 비밀값을 읽기·복사·변경하지 않는다. 테스트는 정확한 `WORK_CALENDAR_*` 설정을 제거한 일회성 SQLCipher DB·키·업로드 경로만 쓴다.
- 다른 저장소, 원본 dirty worktree, GateMigration·통합관제 스케줄은 수정하지 않는다. 새로운 Windows 관리자/OS 권한 상승이나 전역 도구 설치는 하지 않는다.
- 자동 commit/stage/push/merge, 원본 프로세스 교체, 운영 배포, 외부 이메일·문자·Discord 알림 발송은 수행하지 않는다. 납품은 테스트와 QA를 마친 이 전용 브랜치의 변경분이다.
- 반복 업무·새 역할·외부 캘린더 양방향 연동처럼 DB/API 계약 변경이 필요한 기능은 이번 계약 보존 고도화의 수용 대상이 아니다. 미래 후보로 구분하고 미구현을 완료로 표시하지 않는다.
- 테스트 삭제/skip/조건부 클릭/인증 우회/더미 운영 키로 실패를 숨기지 않는다.

## 3. 사용자 경험과 설계 원칙

- 관리자 사용자 패널은 세로로 쌓는다. 각 상태 행은 데스크톱 3개 초기 카드, 다음 페이지는 넘김 또는 더 보기 후에만 로드한다. 한 사용자 상태 필터가 다른 사용자 패널을 바꾸면 안 된다.
- 일반 이용자는 생성자 또는 처리자로 권한이 있는 업무만 서버에서 받는다. 화면 숨김은 보안 수단이 아니다.
- 접수일 캘린더와 처리일 리포트는 의미와 데이터 소스를 분리한다. Asia/Seoul 날짜 기준을 유지한다.
- 로딩·빈 결과·네트워크 실패·검증 실패·권한 거절·세션 만료를 분리하고, 재시도 가능한 실패에서 입력과 정상 세션을 보존한다.
- 현재 정적 HTML/JS/CSS와 FastAPI 모듈 구조를 유지한다. 근거 없는 프레임워크/ORM 교체나 빌드 체인 증설은 하지 않는다.

## 4. 순서별 요구사항과 수용 기준

### UPG-BASE-001 — 기준 계약과 증거 원장

현 소스의 mounted API/대표 응답/fixture DB 스키마를 독립 테스트로 동결한다. `docs/UPGRADE_ACCEPTANCE_LEDGER_20261003.md`에 이 PRD의 모든 ID, 소스·테스트·실행 로그·상태를 연결한다. 허용 상태는 `NOT_STARTED`, `IN_PROGRESS`, `LOCAL_VERIFIED`, `LOCAL_FAILED`, `EXTERNAL_BLOCKED`, `OUT_OF_SCOPE`다. 43개 기존 테스트 및 browser가 현재 코드에서도 실행되고, 기존 성능 slice에 미결함이 없는지 독립 QA를 통과한다. DB/키의 제품 경로를 사용하지 않음을 검사한다.

### UPG-PERF-001 — 읽기 성능과 경계 회귀

기존 bulk projection을 보존·보완한다. 빈 결과 related query 0회, 1~20건 related query 5회 이하, 305 distinct ID chunk 경계, 반복 입력 dedupe, 단건과 bulk 필드/순서 동일성을 검증한다. ADMIN/MEMBER 목록·두 캘린더·XLSX 필터/권한과 감사 계약을 실제 API에서 검사한다. fixture 기반 벤치마크에는 규모·반복 횟수·환경·관측값을 적고 SELECT 감소와 latency 결과를 구분한다.

### UPG-UX-001 — 프런트 공통 요청과 화면 수명

`web/app.js`의 요청·오류·날짜/escape 등 공통 책임을 작은 정적 모듈로 추출하되 기존 진입점과 DOM 기능은 유지한다. fetch timeout/취소, 최신 요청만 화면 반영, 화면 이동·logout 후 stale 응답 폐기, 사용자별 수명 초기화를 구현한다. 401만 정상 만료 흐름으로 보내고 403/422/500/network 실패에서 무조건 logout하지 않는다. 오류 메시지 escape, 재시도와 busy/aria-live 상태를 실제 화면에서 검증한다. 모든 새 JS 자산 syntax 검사 및 실제 서버 제공 여부를 확인한다.

### UPG-UX-002 — 사용자별 보드의 제한된 요청과 로딩

사용자·상태별 요청을 최대 6개 동시 실행으로 제한하고 요청 실패를 해당 그룹의 재시도 상태로 표시한다. 초기 각 그룹은 `page_size=3`, 후속 페이지는 사용자 상호작용 뒤에만 조회한다. 중복 in-flight/중복 카드/늦은 응답 혼입을 방지한다. 한 사용자의 상태 선택·전체 보기와 전체 검색 필터를 구분한다. 2명 이상·상태당 7건 이상 fixture로 초기/다음 페이지 네트워크·DOM 계약을 검사한다.

### UPG-UX-003 — 사용자별 필터 복원과 저장 보기

목록 검색·상태·접수일/마감일·처리자·페이지 크기, 캘린더 보기/월을 새로고침·상세 복귀 시 복원한다. 현재 로그인 사용자 ID와 역할로 분리한 sessionStorage에만 UI 상태와 최대 10개 이름 붙인 저장 보기를 둔다. 사용자 변경/logout에서 해당 탭의 제품 상태를 초기화하며 업무 응답·연락처·첨부·비밀번호를 저장하지 않는다. 잘못된 JSON/날짜/역전 기간/비활성 처리자/권한 변경을 안전한 기본값으로 복구한다. 필터 초기화는 목록·보드·내보내기에 동일하게 적용한다.

### UPG-CAL-001 — 실제 요일 월간 보기와 주간 보기

월 캘린더에 요일 헤더·월 시작 offset·오늘/선택일 표시·오늘 이동을 제공한다. 접수일/처리일 의미를 유지한 주간 agenda 보기를 추가한다. 월 경계 주간은 필요한 월을 최대 3개만 조회하고 응답은 현재 권한 범위 안에서 날짜별로 집계한다. 월간 +N건과 주간 항목에서 상세 및 원래 보기로 돌아온다. 윤년·12월/1월·서울 자정 경계·완료 업무의 기존 접수 캘린더 정책을 회귀 검증한다.

### UPG-TASK-001 — 입력·저장 안정성과 상세 복귀

등록/수정/마스터/사용자 저장 버튼을 실제 요청 중 잠그고 이중 제출을 방지한다. 실패 시 사용자가 입력한 값을 유지하며 필드별 검증과 수정 가능한 재시도를 제공한다. 업무 생성 후 첨부 일부 실패는 이미 생성된 업무의 상세/추가 업로드로 이어지고 동일 업무를 다시 생성하지 않는다. 상태 전환 시 처리일/접수일 수정 권한과 soft delete 확인·감사 이력을 보존한다. 상세에서 원래 필터·페이지·캘린더 위치로 돌아온다.

### UPG-FILE-001 — 비공개 첨부의 수명과 오류 처리

다운로드/이미지 로딩/회전/삭제의 busy·실패·재시도 표시를 일관화한다. 성공·실패·화면 이탈에서 object URL을 해제한다. 파일 수·MIME·크기·실제 파일 내용 검증과 서버 접근 제어를 유지한다. 외부 정적 공개 경로나 민감 파일 캐시는 만들지 않는다. 임시 fixture 파일로 정상 업로드/다운로드, 금지 형식, 타인 접근, 부분 실패·정리와 기존 편집 이력을 API/browser에서 검증한다.

### UPG-OPS-001 — 알림·통계·내보내기 연결성

기존 로컬 알림함의 페이지·읽음 상태·환경설정 저장 및 재시도를 사용 가능하게 연결한다. 미확인 API를 임의로 추가하지 말고 이미 mounted 계약을 사용한다. 통계·목록·XLSX에 같은 권한/기간/처리자 의미가 적용됨을 검사한다. 다중 처리 업무의 집계 의미를 유지하고 완료/재개·마감 변경의 로컬 알림 중복/누락 회귀를 추가한다. 외부 채널은 전송하지 않는다.

### UPG-SEC-001 — 현재 권한·보안의 부정 경로

login → Bearer → 즉시 protected route, logout/revoked/비활성/비밀번호 변경, 마지막 활성 관리자, MEMBER 타인 업무·첨부·감사/관리자 접근을 동결 계약으로 검증한다. UI의 일반 실패와 401/403을 구분한다. XSS·XLSX 수식·path traversal·다운로드 헤더·감사 민감값 마스킹·SQLCipher 무키 읽기 거부를 fixture로 검증한다. 기존 스키마/권한 모델을 바꾸거나 테스트 전용 우회를 운영 코드에 넣지 않는다.

### UPG-RUN-001 — 재현 환경과 완전한 검증 명령

Conda `shared_calendar` manifest·runtime/test dependency·Chromium 설치 방법을 일치시킨다. `scripts/verify.py --mode all`은 모든 backend/API/browser 테스트, 새 JS 자산 syntax, compile, tracked/untracked whitespace, 누락/0/all-skipped 검사, 안전 artifact 정리를 실행한다. 필요하면 Windows `.bat` 래퍼를 CRLF 및 `call conda`로 제공한다. CI는 disposable 설정만 사용하며 fixture key/env 값을 출력하지 않는다. 프로젝트 범위 dependency 진단을 남기고 검사할 수 없었던 보안 정보를 PASS로 만들지 않는다.

### UPG-OPS-002 — 운영 진단과 복구 준비

비밀값을 읽거나 제품 DB에 연결하지 않는 환경 진단 명령을 제공한다. runtime/package/필수 자산·설정 키 이름·검증 명령을 점검하고 원인별 실패를 구분한다. SQLCipher/DPAPI 백업·복구·업데이트·rollback runbook은 개발 fixture에서 가능한 절차만 실제 실행 증거로 연결하고, 운영 키/DB/첨부 이동·교체는 별도 승인 작업으로 구분한다. 임시 서버·파일 handle·키 artifact가 납품 경로에 남지 않음을 검사한다.

### UPG-E2E-001 — 실서비스 통합·반응형 수용

실제 임시 SQLCipher FastAPI + Chromium에서 ADMIN/MEMBER 각각 로그인·비밀번호 변경·보드/필터·새 업무/수정·월/주 보기·첨부·로컬 알림·통계·XLSX·logout을 검증한다. 1280/768/390px에서 대표 화면을 캡처하고 overflow·잘림·키보드 focus를 검사한다. network 오류/403/401/빈 결과/부분 첨부 실패도 실제 DOM과 요청 계약으로 확인한다. API mock은 해당 실패 주입에만 표시하고, 정상 서비스 E2E를 대신하지 않는다.

### UPG-DONE-001 — 최종 재검증과 종료

앞선 모든 ID가 `LOCAL_VERIFIED`이고 미결 local criterion/중대·중간 QA 결함/실패 gate가 0인 현재 소스에서 전체 검증을 다시 실행한다. `docs/FINAL_UPGRADE_REPORT_20261003.md`에 실제 테스트 수·명령·결과·조회/벤치마크·화면 증거·변경 경로·원본 보존·배포 제외를 기록한다. 최종 보고를 code fingerprint, task-state digest, 구현 revision, report hash로 묶고 이후 변경 시 무효화한다. 결과를 이 대화에 전달하고 실제 delivery receipt 확인 후 controller를 pause한다. 단순 AI Pro exit 0 또는 선언 문장만으로 종료하지 않는다.

## 5. 자동 진행과 실패 처리

- 한 전용 worktree에는 writer가 정확히 1개다. 실행 중 watchdog은 새 writer를 만들지 않는다.
- `AI Pro 구현 → 부모 전체 gate 실행 → 독립 read-only QA → 수용 또는 자동 수정 → 다음 ID` 순서를 반복한다.
- 단발 구현 제한은 20분, QA 제한은 12분이다. timeout은 부분 변경·로그를 보존하여 자동 재개한다. 알려진 일시 quota는 cooldown 후 재시도하며 인증 만료나 scope 위반은 정확한 차단 원인을 보고한다.
- 5분 script-only watchdog은 복구 확인용이다. 정상 worker는 다음 slice를 즉시 이어가므로 실제 개발은 5분마다만 하는 구조가 아니다.
- `STOP`을 생성하면 cooldown/실행 중에도 감지하여 이 작업 소유 프로세스만 중지한다. 안전 차단·진짜 실행 불가 외에는 사용자 재실행을 기다리지 않는다.
- 최종 인수는 이번 PRD의 로컬 개발·검증 완료다. 미수행 운영 배포나 외부 승인까지 완료했다고 말하지 않는다.

## 6. 명령과 산출물

```bat
conda run --no-capture-output -n shared_calendar python -s scripts/verify.py --mode all
conda run --no-capture-output -n shared_calendar python -s scripts/verify.py --mode frontend
```

- 이 PRD, acceptance ledger, 현재 `PROGRESS.md`, 최종 보고와 재현 가능한 테스트/fixture/browser 증거.
- 저장소 밖 versioned controller·manifest·state·slice별 구현/검증/QA 로그.
- 원본 데이터/키/첨부/dirty 변경은 보존. 작업공간의 변경분을 자동 운영 반영하지 않는다.
