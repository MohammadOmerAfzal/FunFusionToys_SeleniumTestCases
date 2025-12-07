from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# NOTE: WebDriverWait is not imported in the original script but is often useful. 
# Added here for completeness if you decide to use it.
from selenium.webdriver.support.ui import WebDriverWait 
import time
import os # <-- NEW: Import os module

# --- Dynamic Host Setup (Required for CI) ---
# SELENIUM_HOST will be 'selenium-node-ci' (container name)
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'localhost')
SELENIUM_URL = f'http://{SELENIUM_HOST}:4444/wd/hub'

# BASE_URL will be 'http://frontend-ci:5173' (internal service name and port)
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5174') 
# --------------------------------------------

def test_real_product_count():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--remote-allow-origins=*") 
    options.add_argument("--disable-gpu") 
    options.add_argument("--disable-features=VizDisplayCompositor")

    driver = webdriver.Remote(
        # UPDATED: Use the dynamic SELENIUM_URL
        command_executor=SELENIUM_URL,
        options=options
    )
    # Ensure WebDriverWait is imported if used (was not in original, but defining it)
    try:
        wait = WebDriverWait(driver, 10) 
    except NameError:
        pass # Only runs if WebDriverWait isn't imported

    try:
        # UPDATED: Use BASE_URL for website access
        shop_url = f"{BASE_URL}/Shop"
        print(f"Opening Shop URL: {shop_url}")
        driver.get(shop_url)
        time.sleep(2)

        # Count ONLY real product cards — class="Item"
        products = driver.find_elements(By.CLASS_NAME, "Item")

        print(f"🛒 Real product cards found = {len(products)}")

        # Print titles & prices
        for p in products:
            # Added a nested try/except for robustness in finding sub-elements
            try:
                title = p.find_element(By.CLASS_NAME, "item-name").text
                price = p.find_element(By.CLASS_NAME, "item-price").text
                print(f"➡ {title} | {price}")
            except Exception as e:
                print(f"Error reading product details: {e}")

        if len(products) == 7:
            print("✅ Product count is correct (7 products).")
        else:
            print("⚠ Product count mismatch!")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_real_product_count()
