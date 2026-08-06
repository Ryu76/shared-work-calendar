# 카카오워크 연동 설계 (로컬 기반)

## 범위
이 단계는 실제 카카오워크 API 호출·토큰 저장·외부 전송을 하지 않는다. 다음 구현의 계약을 고정한다.

1. 카카오워크 사용자 ID ↔ 공유 업무 캘린더 사용자 매핑
2. 업무 등록 메시지 템플릿 파싱·검증
3. 수신 메시지를 통한 업무 생성
4. 처리자별 카카오워크 알림 발송 대기함

## 업무 등록 메시지 템플릿

```text
[업무등록]
처리자: demo_hana, demo_jisoo
요청담당자: 홍길동
연락처: 010-1234-5678
기관: 예시 기관
업무내용: 시설 점검 결과 확인 및 조치 요청
접수일: 2026-07-30
마감일: 2026-08-02
```

### 규칙
- 첫 줄은 정확히 `[업무등록]`.
- `처리자`, `요청담당자`, `연락처`, `기관`, `업무내용`은 필수.
- 처리자는 캘린더 `login_id`를 쉼표로 구분한다.
- `접수일`, `마감일`은 선택이며 YYYY-MM-DD 형식이다.
- 처리자는 활성 계정이어야 하며 1명 이상이어야 한다.
- `마감일`은 접수일보다 빠를 수 없다.

## 저장 모델

### kakao_work_user_links
- `user_id` (캘린더 사용자, unique)
- `kakao_work_user_id` (카카오워크 사용자 ID, unique)
- `linked_at`, `updated_at`

### kakao_work_inbound_events
- `provider_event_id` (중복 수신 방지)
- `sender_kakao_work_user_id`
- `raw_payload` (민감값 마스킹 후 보관)
- `parsed_text`, `status`, `task_id`, `error_message`, `received_at`

### kakao_work_outbox
- `user_id`, `task_id`, `event_type`
- `payload` (비밀값 제외)
- `status` (`PENDING`, `SENT`, `FAILED`)
- `attempt_count`, `provider_message_id`, `last_error`, `created_at`, `sent_at`

## 수신 흐름

1. 카카오워크 공개 HTTPS 웹훅이 메시지를 수신한다.
2. 카카오워크가 제공하는 서명 규격으로 요청을 검증한다.
3. 이벤트 ID로 중복 수신을 차단한다.
4. 메시지 본문을 위 템플릿으로 파싱하고 필수값·처리자·날짜를 검증한다.
5. 전용 봇 서비스 계정이 업무를 생성하고 감사 로그에 `KAKAO_WORK_TASK_CREATED`을 남긴다.
6. 처리자별 연결된 카카오워크 사용자에게 `TASK_ASSIGNED` 알림을 `kakao_work_outbox`에 적재한다.
7. 발송 워커가 카카오워크 공식 Bot API로 전송한다. 성공·실패·재시도는 대기함에 기록한다.

## 발송 메시지 예시

```text
[새 업무 배정]
업무: 시설 점검 결과 확인 및 조치 요청
상태: 접수
요청: 홍길동 / 예시 기관
마감일: 2026-08-02
업무 캘린더에서 상세 내용을 확인하세요.
```

## 실제 API 연결 전 필수값

- 카카오워크 관리자/개발자 콘솔 권한
- 봇 유형과 앱 ID
- Bot API 인증 방식 및 토큰
- 이벤트 웹훅 URL·검증용 서명 키
- 사용자 ID 조회·메시지 발송에 필요한 권한(scope)
- 외부에서 접근 가능한 HTTPS 콜백 URL

> 토큰과 서명 키는 평문 `.env`나 DB에 저장하지 않는다. 운영 도입 시 OS 비밀 저장소 또는 별도 암호화 키 관리 체계를 사용한다.
