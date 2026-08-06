# 공유 업무 캘린더

`공유 업무 캘린더 PRD (MVP)` 기반의 내부 업무 관리 프로젝트입니다.

## 현재 구현 범위

- 로그인·로그아웃·Bearer 세션, ADMIN/MEMBER 권한, 최초 로그인 비밀번호 변경 강제
- 모든 신규·변경 비밀번호는 Argon2id 해시로 저장하며, 기존 로컬 PBKDF2 해시는 성공적인 로그인 시 Argon2id로 안전하게 자동 전환
- 관리자 사용자 생성·수정·비활성화, 마지막 활성 관리자 보호
- 기관·요청 담당자 자동완성, 신규 입력 시 재사용 마스터 자동 생성, 관리자 검색·수정·사용 중지
- 업무 등록·조회·수정·관리자 소프트 삭제, 비공개 이미지 첨부/미리보기/삭제
- 이미지: 업무당 최대 5개, 파일당 10MB, JPG/PNG/WEBP MIME·시그니처 이중 검증, 업무 권한 확인 후 서버 제공
- 복수 처리자, 상태/처리일 규칙, 서버측 내 업무 권한 필터, 상태·접수일·키워드·관리자 처리자 필터 및 페이지네이션(기본 20건/최대 100건)
- 월별 접수일 캘린더 API(엄격한 `YYYY-MM` 입력 검증)
- Phase 2 상태별·사용자별 통계: 접수일 기간과 관리자 처리자 필터, 권한 범위별 상태 집계 및 처리자별 배정 집계(공동 처리 건은 처리자별 1건)
- Phase 2 업무 마감일: 기존 SQLite 업무를 보존하는 `due_date` 마이그레이션, 접수일 이후 검증, 등록/수정/목록 마감일 기간 필터, 상세·목록 표시
- 개인별 마감 알림 설정 및 권한 범위의 안전한 로컬 인앱 알림함(오늘/3일 이내/지난 마감, 읽음 처리). 이메일·문자·메신저 등의 외부 전송은 구현하거나 호출하지 않습니다.
- Phase 2 첨부 확장: 기존 이미지는 그대로 유지하면서 비공개 PDF/TXT/DOCX/XLSX 문서(파일당 25MB) 및 MP4/WEBM 동영상(파일당 100MB)을 업무당 최대 10개 추가 첨부, MIME·실제 파일 구조 이중 검증, 권한 확인 후 다운로드 전용 제공·삭제·감사 이력
- Phase 2 엑셀 내보내기: 현재 로그인 사용자의 서버 권한 범위와 상태·검색·접수일·마감일·처리자 필터를 그대로 적용한 XLSX 다운로드(최대 10,000건), 수식 주입 방지, 다운로드 전용 보안 헤더 및 감사 기록
- Phase 2 처리일 리포트 캘린더: 접수일 캘린더와 독립된 월별 처리일 기준 완료 업무 보기, 엄격한 월 입력 검증 및 기존 ADMIN/MEMBER 업무 접근 범위 적용
- Phase 2 이미지 편집: 권한 있는 업무 참여자가 JPG/PNG/WEBP 이미지를 왼쪽/오른쪽 90° 회전할 수 있으며, 원본은 비공개 편집 이력으로 보존합니다. 디코딩 픽셀 수와 결과 크기를 제한하고 EXIF 메타데이터를 복사하지 않으며, 편집/삭제는 감사 로그에 기록합니다.
- 기존 SQLite 데이터에 안전하게 적용되는 통계 조회 인덱스 마이그레이션
- 감사 로그 기록 및 관리자 조회
- 반응형 단일 페이지 UI: 로그인, 내 업무, 캘린더, 통계, 마감 알림, 업무 등록/수정, 사용자 관리

## 실행

```bash
python -m pip install -r requirements.txt
cd backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8010
```

브라우저에서 `http://127.0.0.1:8010`을 엽니다.

새 데이터베이스를 초기화하기 전에 8자 이상의 초기 관리자 비밀번호를 환경 변수로 제공해야 합니다. 예: `WORK_CALENDAR_INITIAL_ADMIN_PASSWORD`를 배포 비밀 관리 도구에서 설정하십시오. 초기 관리자 계정은 첫 실행 시 생성되고, 초기 비밀번호는 첫 로그인 직후 반드시 변경해야 업무 기능을 이용할 수 있습니다. 초기 계정 정보는 저장소·문서·로그에 노출하지 마십시오. 새 관리자 계정과 일반 이용자 계정은 사용자 관리 화면에서 만드십시오.

## 테스트

```bash
cd backend
python -m unittest -v test_main.py test_acceptance.py test_browser_ui.py
node --check ../web/app.js
```

One-time browser-test setup after installing the Python requirements:

```bash
python -m playwright install chromium
```

`test_acceptance.py` starts from an isolated temporary SQLite database and private upload directory, then verifies all PRD acceptance criteria through independently authenticated API clients. `test_browser_ui.py` starts a separate isolated Uvicorn process and uses Playwright Chromium to verify the rendered administrator master-management and task-filter/pagination flows. Neither test modifies the repository database.

## 보안·운영 전제

이 초기 프로젝트는 로컬 MVP입니다. 비공개 이미지 저장·권한 확인·형식/크기 검증은 구현되어 있지만, CSRF 보호, 영속 세션 저장, HTTPS, PostgreSQL 전환, 파일 악성코드 검사, 운영 비밀 관리 및 배포 구성은 운영 배포 전에 추가해야 합니다.
