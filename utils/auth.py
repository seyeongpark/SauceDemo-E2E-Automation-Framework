# utils/auth.py
from pathlib import Path
from playwright.sync_api import Browser

STORAGE_DIR = Path(__file__).parent.parent / ".auth"
STORAGE_DIR.mkdir(exist_ok=True)

STANDARD_USER_STATE = STORAGE_DIR / "standard_user.json"

def create_logged_in_state(
    browser: Browser,
    base_url: str,
    username: str,
    password: str,
    storage_path: Path,
) -> Path:
  # UI 로그인 1번 수행 후, Cookie/localStorage를 파일로 저장.
  # 이후 테스트들은 이 파일을 context 생성 시 로그인 상태로 시작.

  context = browser.new_context()
  page = context.new_page()

  page.goto(base_url)
  page.locator("#user-name").fill(username)
  page.locator("#password").fill(password)
  page.locator("#login-button").click()

  # 로그인 성공 검증 (햄버거 메뉴 확인)
  page.locator(".bm-burger-button").wait_for(state="visible")

  context.storage_state(path=storage_path)
  context.close()
  return storage_path
