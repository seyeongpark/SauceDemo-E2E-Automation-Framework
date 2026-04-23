# pages/login_page.py

from playwright.sync_api import Page

class LoginPage():

  def __init__(self, page: Page):
    self.page = page
    self.input_username = page.locator('#user-name')
    self.input_password = page.locator('#password')
    self.btn_login = page.locator('#login-button')
    self.btn_hamburger = page.locator('.bm-burger-button')

  @property
  def text_error(self):
      return self.page.locator('[data-test="error"]')

  def open(self, URL):
    self.page.goto(URL)

  def login(self, username: str, password: str):
    self.input_username.fill(username)
    self.input_password.fill(password)
    self.btn_login.click()