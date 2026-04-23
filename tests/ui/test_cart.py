# tests/test_cart.py

import pytest, json
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pathlib import Path

DATA_FILE = Path(__file__).parent.parent.parent / "data" / "cart.json"
MIN_ORDER_AMOUNT = 40.00

with open(DATA_FILE, encoding="utf-8") as f:
  CART_CASES = json.load(f)

# 장바구니 총액이 기대값과 정확히 일치하는지 검증
@pytest.mark.regression
@pytest.mark.parametrize(
  "case", 
  CART_CASES,
  ids=[c["case_id"] for c in CART_CASES],
)
def test_cart_total_calculation(logged_in_page, case):
  page = logged_in_page

  inventory = InventoryPage(page)

  for product in case["products"]:
    inventory.add_to_cart(product)  
  inventory.go_to_cart()

  actual_total = CartPage(page).total_price()

  assert actual_total == pytest.approx(case["expected_total"], abs=0.01),(
      f"[{case['case_id']}] {case['description']}"
      f"expected ${case['expected_total']}, got ${actual_total}"
  )

# 최소 주문금액 기준을 충족하는지 검증
@pytest.mark.regression
@pytest.mark.parametrize(
  "case", 
  CART_CASES,
  ids=[c["case_id"] for c in CART_CASES],
)
def test_cart_for_minimum_order(logged_in_page, case):
  page = logged_in_page
  inventory = InventoryPage(page)
  for product in case["products"]:
    inventory.add_to_cart(product)
  inventory.go_to_cart()
  
  actual_total = CartPage(page).total_price()
  expected_minimum = case["expected_total"] >= MIN_ORDER_AMOUNT
  actual_minimum = actual_total >= MIN_ORDER_AMOUNT

  print(f"{case['case_id']}: et- ${case['expected_total']} ac- ${actual_total}")

  assert expected_minimum == actual_minimum, (
    f"[{case['case_id']}] 최소금액 TC 기준 불일치: "
    f"총액 ${actual_total}, 기준 ${MIN_ORDER_AMOUNT}"
  )