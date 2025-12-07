# test_unauthorized_checkout.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

PRODUCT_ID = "676d55d151fc50240e3c9070"

def test_unauthorized_checkout(driver, wait, base_url):
    """
    Test that unauthorized users cannot place an order without logging in.
    """
    print("\n▶️ Testing: Unauthorized users cannot place orders")
    print("=" * 50)

    # Step 1: Open product page and add to cart
    product_url = f"{base_url}/Shop/{PRODUCT_ID}"
    driver.get(product_url)
    add_to_cart_btn = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart-btn"))
    )
    add_to_cart_btn.click()
    print("✅ Product added to cart")

    # Step 2: Go to checkout page
    checkout_url = f"{base_url}/Checkout"
    driver.get(checkout_url)
    print("✅ Checkout page opened")

    # Step 3: Fill checkout form
    form_data = {
        "fullname": "Test User",
        "address": "123 Test St",
        "city": "Test City",
        "postalcode": "12345",
        "email": "test@test.com"
    }

    for field_name, value in form_data.items():
        input_field = wait.until(
            EC.presence_of_element_located((By.NAME, field_name))
        )
        input_field.clear()
        input_field.send_keys(value)
        print(f"✅ Filled {field_name}")

    # Step 4: Attempt to place order
    place_order_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Place Order')]"))
    )
    place_order_btn.click()
    print("✅ Attempted to place order")

    # Step 5: Check for login requirement alert
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"⚠ Alert message: '{alert_text}'")
        alert.accept()

        assert "login" in alert_text.lower() or "sign in" in alert_text.lower(), \
            f"Alert shown but did not indicate login/sign in: '{alert_text}'"
        print("✅ TEST PASSED: Unauthorized users cannot place orders")
    except:
        pytest.fail("❌ TEST FAILED: No alert shown. Order might have been placed without authorization!")

    print("=" * 50)
