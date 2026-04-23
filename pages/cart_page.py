# pages/cart_page.py

from playwright.sync_api import Page

class CartPage():
  def __init__(self, page: Page):
    self.page = page
    self.btn_checkout = page.locator('[data-test="checkout"]')
    self.text_item_price = page.locator('.inventory_item_price')

  def click_checkout(self):
    self.btn_checkout.click()

# 가격 텍스트를 리스트로 가져오기
  def total_price(self) -> float:
      if self.text_item_price.count() == 0:
         return 0.0

      prices = self.text_item_price.all_inner_texts()
      return sum(float(p.replace('$', '')) for p in prices)
  