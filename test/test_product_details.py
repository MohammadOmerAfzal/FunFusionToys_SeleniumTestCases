from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pytest

def test_product_details_page(driver, wait, base_url):
    """Test that the product details page loads correctly and Add to Cart is clickable."""
    print("\n=== TEST: Product Details Page ===")

    # Step 1: Open shop page
    shop_url = f"{base_url}/Shop"
    driver.get(shop_url)

    # Step 2: Wait for products to appear
    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Item")))
    assert products, "❌ No products found on Shop page!"

    # Step 3: Select first product
    first_product = products[0]
    product_name = first_product.find_element(By.CLASS_NAME, "item-name").text
    print(f"➡ Clicking first product: {product_name}")
    first_product.click()

    # Step 4: Validate product detail page opened
    title_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    detail_title = title_element.text
    assert product_name.lower() in detail_title.lower(), \
        f"⚠ Title mismatch! Expected: {product_name}, Got: {detail_title}"
    print(f"✅ Product detail page loaded correctly: {detail_title}")

    # Step 5: Verify Add to Cart button exists and is clickable
    add_to_cart_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart-btn")))
    print("✅ 'Add to Cart' button is visible and clickable.")

    # Optional: actually click the button
    try:
        actions = ActionChains(driver)
        actions.move_to_element(add_to_cart_btn).click().perform()
        print("✅ 'Add to Cart' button clicked successfully.")
    except Exception as e:
        pytest.fail(f"❌ Add to Cart button is NOT clickable! Error: {e}")
