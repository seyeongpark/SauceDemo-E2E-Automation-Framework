# tests/test_complete_order.py

import pytest, allure
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from playwright.sync_api import expect

E2E_CASES = [
  (
    ["Sauce Labs Backpack", "Sauce Labs Fleece Jacket"],  # 장바구니 상품
    "James", "Lee", "Q1W2E3"                              # 배송 정보
  )
]

# --- 메인 테스트 시나리오 ---
@allure.epic("쇼핑몰")
@allure.feature("주문/결제")
@allure.story("정상 주문 완료")
@pytest.mark.e2e
@pytest.mark.smoke
@pytest.mark.parametrize("products, firstname, lastname, zipcode", E2E_CASES)
def test_complete_order(logged_in_page,page, products, firstname, lastname, zipcode):
    
    # 1. 로그인 (비즈니스 시나리오에만 집중 -> fixture에서 로그인 로직 가져오기)
    page = logged_in_page
    
    # 2. 상품 추가 및 장바구니 이동
    inventory = InventoryPage(page)
    for product in products:
        inventory.add_to_cart(product)
    inventory.go_to_cart()
    
    # 3. 체크아웃 진행
    CartPage(page).click_checkout()
    
    # 4. 배송 정보 입력
    checkout = CheckoutPage(page)
    checkout.enter_info(firstname, lastname, zipcode)
    
    # 5. 최종 확인 및 완료
    checkout.click_finish_checkout()
    
    # 6. 완료 메세지 검증
    expect(checkout.text_complete_order).to_be_visible()
    expect(checkout.text_complete_order).to_contain_text('Thank you for your order!')