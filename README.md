# SauceDemo E2E Automation Framework

Playwright와 pytest 기반의 E2E 자동화 프레임워크입니다.
https://www.saucedemo.com/ 을 대상으로 POM, 데이터 분리, storage_state 재사용, CI/CD, 크로스 브라우저를 적용하였습니다.

## 프로젝트 목표

- POM 기반의 유지보수가 가능한 구조 설계
- 데이터 주도 테스트로 케이스 확장성 확보
- GitHub Actions로 CI 파이프라인 구축 (nightly)
- Chromium/Firefox/Webkit 크로스 브라우저 사용
- 실패시 스크린샷/비디오 자동 수집

## 아키텍처

tests/    --->  pages/   ---> Playwright
(시나리오)        (POM)         (브라우저)

  ^               ^
data/*.json    BasePage

## 디렉토리 구조

- `pages/` — Page Object 클래스 (BasePage 상속)
- `tests/ui/` — UI E2E 테스트
- `tests/api/` — API 레벨 테스트
- `data/` — 테스트 데이터 (JSON)
- `utils/` — 로그인 상태 생성 등 헬퍼
- `.github/workflows/` — CI 파이프라인

## 실행 방법
### 설치
```bash
pip install -r requirements.txt
playwright install
cp .env.example .env
```

### 로컬 실행
```bash
# 전체 테스트
pytest

# 스모크 테스트
pytest -m smoke

# 특정 브라우저
pytest --browser firefox

# 병렬 실행
pytest -n auto

# Headless
pytest --headed=false
```

### 리포트 확인
```bash
# 실패한 테스트의 trace 보기
playwight show-trace test-results//trace.zip
```

```bash
# Allure 리포트 보기 (임시 서버)
allure serve allure-results
```


### 테스트 커버리지
| 영역 | 시나리오 수 | 설명 |
|-----|----------|-----|
| 로그인 | 7 | 정상/오류/잠금/필수값 누락 |
| 장바구니 | 8 | 최소 주문금액 검증, 다양한 조합 |
| E2E 주문 | 1+ | 로그인→장바구니→결제 풀 플로우 |
| API | 3+ | REST API 직접 호출 검증 |

### CI
**실행 트리거**
- Push / PR: 빠른 피드백 (smoke 중심)
- 매일 KST 03:00 (nightly): 전체 회귀 테스트
- 수동 실행 (workflow_dispatch): 필요 시 즉시 실행