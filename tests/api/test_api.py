# tests/api/test_api.py

import os

import pytest
from playwright.sync_api import Playwright, APIRequestContext

API_BASE = "https://reqres.in/api/"

@pytest.fixture(scope="module")
def api_request(playwright: Playwright) -> APIRequestContext:
  api_key = os.getenv("REQRES_API_KEY")
  assert api_key, "REQRES_API_KEY 환경변수 확인 필요"

  request_context = playwright.request.new_context(
    base_url = API_BASE,
    extra_http_headers = {
      "Content-Type": "application/json",
      "x-api-key": api_key,
    }
  )
  yield request_context
  request_context.dispose()

# 사용자 목록 조회 - 상태코드, 응답구조, 페지네이션 검증
@pytest.mark.api
@pytest.mark.smoke
def test_get_users_list(api_request: APIRequestContext):
  response = api_request.get("users?page=2")

  assert response.status == 200, f"Expected 200, got {response.status}"

  body = response.json()
  assert body["page"] == 2
  assert "data" in body
  assert len(body["data"]) > 0
  assert all("email" in user for user in body["data"])

# POST /users 에 사용자 생성
@pytest.mark.api
def test_create_user(api_request: APIRequestContext):
  payload = { "name": "John Doe", "job": "QA Engineer" }

  response = api_request.post("users", data=payload)

  assert response.status == 201
  body = response.json()
  assert body["name"] == payload["name"]
  assert body["job"] == payload["job"]
  assert "id" in body
  assert "createdAt" in body

# 존재하지 않는 사용자 조회 시 --> 404
@pytest.mark.api
def test_user_not_found(api_request: APIRequestContext):
  response = api_request.get("users/44")

  assert response.status == 404
