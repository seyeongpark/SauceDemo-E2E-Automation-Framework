# pages/checkout_page.py

from playwright.sync_api import Page

class CheckoutPage:
  def __init__ (self, page: Page):
    self.page = page
    self.input_firstname = page.locator('#first-name')
    self.input_lastname = page.locator('#last-name')
    self.input_zipcode = page.locator('#postal-code')
    self.btn_continue = page.locator('#continue')
    self.btn_finish = page.locator('#finish')
    self.text_complete_order = page.locator('[data-test="complete-header"]')

  def enter_info(self, f_name, l_name, zip):
    self.input_firstname.fill(f_name)
    self.input_lastname.fill(l_name)
    self.input_zipcode.fill(zip)
    self.btn_continue.click()

  def click_continue(self):
    self.btn_continue.click()

  def click_finish_checkout(self):
    self.btn_finish.click()
