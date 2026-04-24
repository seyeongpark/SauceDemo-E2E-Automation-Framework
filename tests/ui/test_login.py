# tests/test_login.py

import pytest, json, allure
from pages.login_page import LoginPage
from playwright.sync_api import expect
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent.parent / "data" / "login.json"

with open(DATA_FILE, encoding="utf-8") as f:
  login_cases = json.load(f)

LOGIN_CASES = [
    (
        case["user_id"],
        case["username"],
        case["password"],
        case["expected_error"],
        case["expected_url"]
    )
    for case in login_cases
]

@allure.epic("쇼핑몰")
@allure.feature("로그인")
@allure.story("로그인 기능 검증")
@pytest.mark.parametrize("user_id, username, password, expected_msg, expected_url", LOGIN_CASES)
def test_login(page, base_url, user_id, username, password, expected_msg, expected_url):
  login_page = LoginPage(page)
  login_page.open(base_url)
  print(f"[TEST CASE] {user_id}")
  login_page.login(username, password)

  if expected_msg:
    expect(login_page.text_error).to_contain_text(expected_msg)
    expect(login_page.page).to_have_url(expected_url)
  else:
    expect(login_page.text_error).to_be_hidden()
    expect(login_page.btn_hamburger).to_be_visible()