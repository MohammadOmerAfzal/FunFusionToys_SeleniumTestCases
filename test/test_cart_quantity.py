# test_cart_quantity.py
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

PRODUCT_DETAIL_PATH = "/Shop/676d55d151fc50240e3c9070"
CART_PATH = "/Cart"

def test_cart_quantity(driver, wait, base_url):
    """Test: Add items and check cart quantity"""

    # Step 1: Add 1 item
    driver.get(f"{base_url}{PRODUCT_DETAIL_PATH}")
    add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart-btn")))
    add_btn.click()

    # Step 2: Go to cart and verify quantity
    driver.get(f"{base_url}{CART_PATH}")
    cart_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cartitems-format")))
    assert len(cart_items) > 0, "No cart items found"

    p_tags = cart_items[0].find_elements(By.TAG_NAME, "p")
    assert len(p_tags) >= 4, "Cart item does not have quantity info"
    assert p_tags[3].text == "1", f"Expected quantity 1, got {p_tags[3].text}"
    print(f"Quantity after adding 1: {p_tags[3].text}")

    # Step 3: Add 2 more items
    driver.get(f"{base_url}{PRODUCT_DETAIL_PATH}")
    for _ in range(2):
        add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart-btn")))
        add_btn.click()

    # Step 4: Go to cart and verify quantity
    driver.get(f"{base_url}{CART_PATH}")
    cart_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cartitems-format")))
    p_tags = cart_items[0].find_elements(By.TAG_NAME, "p")
    assert p_tags[3].text == "3", f"Expected quantity 3, got {p_tags[3].text}"
    print(f"Quantity after adding 2 more: {p_tags[3].text}")
