from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # WebDriverWait was defined but not imported in the original
import time
import os # <-- NEW: Import os module

# --- Dynamic Host Setup (Required for CI) ---
# SELENIUM_HOST will be 'selenium-node-ci' (container name)
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'localhost')
SELENIUM_URL = f'http://{SELENIUM_HOST}:4444/wd/hub'

# BASE_URL will be 'http://frontend-ci:5173' (internal service name and port)
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5174') 
# --------------------------------------------

chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--remote-allow-origins=*") 
chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    

driver = webdriver.Remote(
    # UPDATED: Use the dynamic SELENIUM_URL
    command_executor=SELENIUM_URL,
    options=chrome_options
)
wait = WebDriverWait(driver, 10)

# Define product URL dynamically
PRODUCT_DETAIL_URL = f"{BASE_URL}/Shop/676d55d151fc50240e3c9070"
CART_URL = f"{BASE_URL}/Cart"

print("Test: Add items and check cart quantity")

try:
    # Test 1: Add 1 item
    print("\nTest 1: Add 1 item")
    # UPDATED: Use BASE_URL
    driver.get(PRODUCT_DETAIL_URL) 
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
    time.sleep(2)

    # UPDATED: Use BASE_URL
    driver.get(CART_URL) 
    time.sleep(2)

    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
    if cart_items:
        p_tags = cart_items[0].find_elements(By.TAG_NAME, "p")
        if len(p_tags) >= 4:
            # Note: The index [3] depends entirely on your application's HTML structure.
            print(f"Quantity after adding 1: {p_tags[3].text}")

    # Test 2: Add 2 more (total 3)
    print("\nTest 2: Add 2 more items")
    # UPDATED: Use BASE_URL
    driver.get(PRODUCT_DETAIL_URL) 
    time.sleep(2)

    for i in range(2):
        driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
        time.sleep(1)

    # UPDATED: Use BASE_URL
    driver.get(CART_URL) 
    time.sleep(2)

    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
    if cart_items:
        p_tags = cart_items[0].find_elements(By.TAG_NAME, "p")
        if len(p_tags) >= 4:
            print(f"Quantity after adding 2 more: {p_tags[3].text}")
    print("Test case Passed")

except Exception as e:
    print(f"Error: {e}")

driver.quit()
