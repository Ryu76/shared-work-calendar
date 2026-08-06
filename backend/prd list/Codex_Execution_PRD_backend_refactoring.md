# Codex Execution PRD

# backend/main.py 리팩토링 및 모듈화

## 역할

당신은 Senior Python Backend Engineer이다. 목표는 기존 기능을 절대
깨뜨리지 않고 `backend/main.py`를 계층형 아키텍처로 리팩토링하는 것이다.

## 핵심 원칙

-   기존 API URL 변경 금지
-   Request/Response 형식 변경 금지
-   DB 스키마 변경 금지
-   기존 기능 삭제 금지
-   회귀(regression) 발생 금지
-   작은 단위로 점진적 리팩토링

## 목표 구조

``` text
backend/
  app/main.py
  core/
  routers/
  services/
  repositories/
  schemas/
  models/
  middleware/
  utils/
  background/
  tests/
```

## 계층 규칙

### Router

-   Request 검증
-   Service 호출
-   SQL 작성 금지

### Service

-   비즈니스 로직
-   트랜잭션
-   Repository 호출

### Repository

-   DB 접근만 수행
-   SELECT/INSERT/UPDATE/DELETE/SP

## 작업 Phase

### Phase 1

-   프로젝트 구조 생성
-   config/logger/database 분리
-   main.py 최소화

### Phase 2

-   Router 분리
-   Auth
-   User
-   Task
-   Dashboard
-   Admin

### Phase 3

-   Service 계층 생성
-   기존 로직 이동
-   비즈니스 로직 통합

### Phase 4

-   Repository 생성
-   모든 SQL 이동
-   DB 호출 일원화

### Phase 5

-   Middleware
-   Exception Handler
-   Response Helper
-   Validator
-   Notification Layer
-   Scheduler

## 완료 조건

-   main.py 50줄 이하 권장
-   SQL은 Repository에만 존재
-   Router는 Service만 호출
-   Global Exception 적용
-   Logger 적용
-   .env 기반 Config 적용

## 테스트

반드시 아래를 수행한다.

-   로그인
-   JWT
-   업무 등록
-   업무 수정
-   업무 삭제
-   업무 조회
-   Dashboard
-   예외 처리

기존 결과와 비교하여 동일하게 동작해야 한다.

## 코드 스타일

-   Python 3.11
-   Type Hint 사용
-   Pydantic 사용
-   함수 100줄 이하 권장
-   클래스 단일 책임 원칙
-   중복 제거(DRY)

## 커밋 단위

1.  project structure
2.  router split
3.  service split
4.  repository split
5.  middleware
6.  exception
7.  logger
8.  tests

## 출력 방식

각 Phase 종료 시 아래 형식으로 보고한다.

``` text
Completed:
- ...

Modified Files:
- ...

Risk:
- ...

Next Phase:
- ...
```

## 금지사항

-   API 스펙 변경
-   URL 변경
-   DB 변경
-   임의 기능 추가
-   대규모 일괄 수정
-   테스트 없이 완료 처리

리팩토링은 반드시 기능 보존을 최우선으로 하며, 작은 변경 → 테스트 → 다음
단계 순서로 진행한다.
