# conftest.py

import pytest, os
from dotenv import load_dotenv
from pathlib import Path
from utils.auth import create_logged_in_state, STANDARD_USER_STATE

load_dotenv()

@pytest.fixture(scope="session")
def base_url():
  return os.getenv("BASE_URL", "https://www.saucedemo.com/")

@pytest.fixture(scope="session")
def standard_user():
  return {
    "username": os.getenv("STANDARD_USERNAME", "standard_user"),
    "password": os.getenv("STANDARD_PASSWORD", "secret_sauce")
  }

def browser_context_args(browser_context_args):
  return {
    **browser_context_args,
    "viewpoint": {"width": 1280, "height": 720},
    "locale": "ko-KR"
  }

# storage에 저장할 state를 반환
@pytest.fixture(scope="session") 
def standard_user_storage_state(browser, base_url, standard_user) -> Path:
  return create_logged_in_state(
    browser = browser,
    base_url = base_url,
    username = standard_user["username"],
    password = standard_user["password"],
    storage_path = STANDARD_USER_STATE,
  )

# 이미 로그인 된 상테로 시작하는 page -?-> 로그인 ui를 건너뜀
@pytest.fixture
def logged_in_page(browser, standard_user_storage_state, base_url):
  context = browser.new_context(storage_state=standard_user_storage_state)
  page = context.new_page()
  page.goto(f"{base_url}inventory.html")
  yield page
  context.close()