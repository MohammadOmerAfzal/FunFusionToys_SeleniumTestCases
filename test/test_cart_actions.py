# test_add_to_cart.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import pytest

PRODUCT_ID = "676d55d151fc50240e3c9070"

def test_add_product_to_cart(driver, wait, base_url):
    """Test adding a product to cart and verifying it in the Cart page."""

    # -----------------------------
    # Step 1: Open Product Page
    # -----------------------------
    product_url = f"{base_url}/Shop/{PRODUCT_ID}"
    driver.get(product_url)
    print(f"Opening product page: {product_url}")

    # Wait for Add to Cart button
    add_to_cart_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart-btn"))
    )
    assert add_to_cart_btn.is_displayed(), "Add to Cart button not visible"
    print("✅ Add to Cart button is visible")

    # Optional: Click the button
    try:
        actions = ActionChains(driver)
        actions.move_to_element(add_to_cart_btn).click().perform()
        print("✅ Clicked Add to Cart button")
    except Exception as e:
        pytest.fail(f"❌ Failed to click Add to Cart button: {e}")

    # -----------------------------
    # Step 2: Go to Cart Page
    # -----------------------------
    cart_url = f"{base_url}/Cart"
    driver.get(cart_url)
    print(f"Opening Cart page: {cart_url}")

    # Verify cart items
    cart_items = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cartitems-format"))
    )
    assert cart_items, "Cart is empty after adding product"
    print(f"✅ Cart items found: {len(cart_items)}")

    # Check first product name
    product_name_element = cart_items[0].find_element(By.TAG_NAME, "p")
    product_name = product_name_element.text
    assert product_name, "Product name not found in cart"
    print(f"✅ Product in cart: {product_name}")

    # Check price (optional)
    totals = driver.find_elements(By.XPATH, "//*[contains(text(), 'Rs.')]")
    if totals:
        print("✅ Prices found in cart:")
        for total in totals:
            print(f"  {total.text}")

    print("✅ Test completed successfully")
