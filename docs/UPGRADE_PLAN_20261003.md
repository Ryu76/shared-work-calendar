# 공유 업무 캘린더 — 1차 고도화 범위

## 기준과 목적

- 사용자 요청: 기존 SQLite 기반 일정 공유 사이트 고도화.
- 기준 커밋: `a847c24e19f840e9478c54d3422eb7da4f1c0db9`.
- 원본: `E:\python\shared-work-calendar` (원본의 미커밋 `PROGRESS.md` 보존).
- 작업공간: `E:\worktrees\shared-work-calendar\performance-20261003`.
- 브랜치: `ai-pro/calendar-performance-20261003`.
- 기존 백엔드 모듈화는 구현된 상태이다. 이를 다시 대규모로 재작성하지 않는다.
- 첫 개선은 업무별 반복 조회(N+1)를 제거하는 읽기 성능 개선과 재현 가능한 검증 환경이다.

## 불변 계약

기존 API URL, 요청/응답 필드, ADMIN/MEMBER 권한, 목록 필터와 페이지네이션,
접수일/처리일 캘린더 정렬, XLSX 필드와 수식 주입 방어, 감사 로그,
DB 스키마와 SQLCipher/DPAPI 정책은 유지한다.
운영 DB, 기존 키, 평문 복구본, 비공개 첨부, `.env`는 읽거나 복사하거나 수정하지 않는다.
운영 프로세스 교체, 외부 알림, 자동 commit/push/merge/deploy는 이번 범위가 아니다.

## 구현 단위와 수용 조건

### UPG-001: 관련정보 일괄 조회

- 이미 권한 필터가 적용된 업무 행의 ID만 받아 생성자, 요청 담당자/기관,
  처리자, 이미지 메타데이터, 첨부 메타데이터를 일괄 조회한다.
- SQLite 바인드 변수 상한을 고려한 보수적인 청크 처리를 적용한다.
- 빈 결과는 관련정보 SQL을 실행하지 않는다.
- 목록, 접수일 캘린더, 처리일 캘린더, XLSX 내보내기에 적용한다.
- 상세와 변경/감사 경로의 기존 단건 응답은 보존한다.
- SQL은 Repository에만 둔다. 투영/응답 매핑은 독립적인 읽기 서비스에서 담당한다.

### UPG-002: 호환성·성능 회귀

- 기존 단건 응답과 일괄 응답의 완전한 필드/정렬 동일성을 검증한다.
- 여러 업무와 복수 처리자, 비활성 이력, 이미지/첨부 순서, 빈 목록을 검증한다.
- 조회 수를 SQL 실행 단위로 측정하여 업무 수마다 증가하는 N+1 재발을 차단한다.
- 청크 경계를 넘는 큰 목록, 권한 범위, 페이지/필터, 두 캘린더,
  XLSX 값과 수식 방어를 검증한다.
- 가능한 성능 회귀는 구현 전 실패(RED)를 확인한 후 구현으로 통과시킨다.

### UPG-003: 실행 가능한 검증 경로

- 전용 Conda `shared_calendar`, Python 3.11을 사용한다.
- 사용자 site-packages 혼용을 금지한다 (`PYTHONNOUSERSITE=1`).
- 개발/테스트 의존성 및 환경 생성 방법을 문서화한다.
- 실제 DB/키를 사용하지 않는 프로젝트 루트 검증 스크립트를 제공한다.
- 전체 회귀, 실제 Chromium UI, Python 컴파일, JS 구문 검사 및 whitespace 검사를 실행한다.
- 독립 read-only QA 결과를 검토하고 차단 결함을 수정한다.

## 기준선 검증 — 2026-10-03

- `shared_calendar` 환경 생성, 기존 `requirements.txt` 및 테스트용 `httpx` 설치.
- 사용자 패키지 유입을 발견하여 환경 변수로 차단 후 의존성을 환경 내부에 설치.
- `python -m pip check`: PASS (`No broken requirements found.`).
- 기존 전체 회귀: **30 tests, OK (97.955s)**, Chromium 실제 렌더링 포함.
- 검증은 생성된 테스트 전용 DB/임시 키/비공개 업로드 경로만 사용했다.
- 기준선 로그: `C:\Users\HODI\AppData\Local\hermes\cache\scratch\calendar-upgrade-20261003\baseline.log`.

## 완료 판정

이 문서는 범위/기준선 기록이다. 고도화 구현 완료를 의미하지 않는다.
UPG-001~003은 실제 변경·회귀·독립 검토 근거가 확보된 뒤 각각 판정한다.
개선된 조회 수와 테스트 수는 실측값만 기재하고 전체 제품 완료율로 확대하지 않는다.

## 구현 검증 현황

- UPG-001: 구현 및 자동 회귀 검증 완료, 독립 QA 대기.
- UPG-002: 새 테스트 13개를 포함한 전체 43개 회귀와 실제 Chromium 검증 PASS.
- UPG-003: `scripts/verify.py --mode all` 및 `--mode frontend` 실제 실행 PASS;
  Conda manifest 및 `pip check` PASS. 독립 검토는 아직 대기 중이다.
- 추가 테스트 파일: `backend/test_projection_integration.py` (API 및 검증 환경 계약).
- 실측 관련정보 조회: 20건의 기존 100 SELECT가 5 SELECT로 감소.
  목록 API는 1건/20건 모두 인증 포함 9 SELECT, XLSX는 인증 포함 7 SELECT.
- 최종 전체 검증: 43 tests, 108.056s, exit 0. 상세는 `PROGRESS.md` 최신 항목.
- 원본 변경, 커밋, push, merge, 배포는 하지 않았다. 이 상태는 독립 QA 전 최종 완료가 아니다.
