from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait # <-- ADDED: Needed for 'wait'
import time
import os # <-- NEW: Import os module


# --- Dynamic Host Setup (Required for CI) ---
# SELENIUM_HOST will be 'selenium-node-ci' (container name)
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'localhost')
SELENIUM_URL = f'http://{SELENIUM_HOST}:4444/wd/hub'

# BASE_URL will be 'http://frontend-ci:5173' (internal service name and port)
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5174') 
# --------------------------------------------


def test_product_details_page():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        # UPDATED: Use the dynamic SELENIUM_URL
        command_executor=SELENIUM_URL,
        options=options
    )
    # The wait object needs to be defined
    wait = WebDriverWait(driver, 10) 

    try:
        print("\n=== TEST: Product Details Page ===")

        # Step 1: Open shop page
        # UPDATED: Use BASE_URL for website access
        shop_url = f"{BASE_URL}/Shop"
        driver.get(shop_url)
        time.sleep(2)

        # Step 2: Select first product card
        products = driver.find_elements(By.CLASS_NAME, "Item")
        if not products:
            print("❌ No products found on Shop page!")
            return

        first_product = products[0]
        product_name = first_product.find_element(By.CLASS_NAME, "item-name").text

        print(f"➡ Clicking first product: {product_name}")

        # Step 3: Click product (opens details page)
        first_product.click()
        time.sleep(2)

        # Step 4: Validate product detail page opened
        title_element = driver.find_element(By.TAG_NAME, "h1")
        detail_title = title_element.text

        if product_name.lower() in detail_title.lower():
            print(f"✅ Product detail page loaded correctly: {detail_title}")
        else:
            print(f"⚠ Title mismatch! Expected: {product_name}, Got: {detail_title}")

        # Step 5: Verify Add to Cart button exists
        try:
            add_to_cart_btn = driver.find_element(By.CLASS_NAME, "add-to-cart-btn")
            print("✅ 'Add to Cart' button is visible.")
        except:
            print("❌ 'Add to Cart' button NOT FOUND!")
            return

        # Step 6: Test button is clickable
        try:
            actions = ActionChains(driver)
            actions.move_to_element(add_to_cart_btn).click().perform()
            print("✅ 'Add to Cart' button is clickable.")
        except:
            print("❌ Add to Cart button is NOT clickable!")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_product_details_page()

