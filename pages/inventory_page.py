# pages/inventory_page.py

from playwright.sync_api import Page

class InventoryPage():
  def __init__(self, page: Page):
    self.page = page

  def add_to_cart(self, product_name: str):
    # 1. 여러 상품 카드 (.inventory_item) 중, 특정 상품명을 가진 카드를 필터링 
    product_card = self.page.locator(".inventory_item").filter(has_text=product_name)

    # 2. 그 안에 있는 버튼을 찾아 클릭
    product_card.locator("button").click()

  def go_to_cart(self):
    self.page.locator('.shopping_cart_link').click()
    