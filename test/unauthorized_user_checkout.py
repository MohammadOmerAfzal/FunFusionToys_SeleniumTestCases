from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait # <-- ADDED: Needed for 'wait'
from selenium.webdriver.support import expected_conditions as EC # <-- ADDED: Needed for 'EC'
import time
import os # <-- NEW: Import os module

# --- Dynamic Host Setup (Required for CI) ---
# SELENIUM_HOST will be 'selenium-node-ci' (container name)
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'localhost')
SELENIUM_URL = f'http://{SELENIUM_HOST}:4444/wd/hub'

# BASE_URL will be 'http://frontend-ci:5173' (internal service name and port)
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5174') 
# --------------------------------------------

PRODUCT_DETAIL_URL = f"{BASE_URL}/Shop/676d55d151fc50240e3c9070"
CHECKOUT_URL = f"{BASE_URL}/Checkout"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Remote(
    # UPDATED: Use the dynamic SELENIUM_URL
    command_executor=SELENIUM_URL,
    options=chrome_options
)
# Ensure WebDriverWait is imported
wait = WebDriverWait(driver, 10)

print("Testing: Unauthorized users cannot place orders")
print("=" * 50)

# 1. Add product to cart (without login)
print("\n1. Adding product to cart...")
# UPDATED: Use dynamic URL
driver.get(PRODUCT_DETAIL_URL) 
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
time.sleep(2)
print("    ✓ Product added to cart")

# 2. Go to checkout page
print("\n2. Going to checkout page...")
# UPDATED: Use dynamic URL
driver.get(CHECKOUT_URL)
time.sleep(2)

# 3. Fill checkout form
print("\n3. Filling checkout form...")
form_data = {
    "fullname": "Test User",
    "address": "123 Test St",
    "city": "Test City",
    "postalcode": "12345",
    "email": "test@test.com"
}

for field_name, value in form_data.items():
    driver.find_element(By.NAME, field_name).send_keys(value)
    print(f"    ✓ Filled {field_name}")

# 4. Try to place order
print("\n4. Attempting to place order...")
driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]").click()
time.sleep(3)

# 5. Check for login requirement
print("\n5. Checking result...")
try:
    alert = driver.switch_to.alert
    alert_text = alert.text
    print(f"    Alert message: '{alert_text}'")
    
    # Check if login is required
    if "login" in alert_text.lower() or "sign in" in alert_text.lower():
        print("\n✅ TEST PASSED: Unauthorized users cannot place orders!")
        print("    Reason: Login/Sign in requirement alert shown")
    else:
        # Note: If no login is required, this test should technically fail unless the alert is a generic success message.
        print(f"\n❌ TEST FAILED: Alert detected, but did not require login/sign in: '{alert_text}'")
        
    alert.accept()
    
except:
    # This means no alert was shown. This is a critical failure for this test case.
    print("\n❌ TEST FAILED: No alert shown. Order might have been placed without authorization!")

print("\n" + "=" * 50)
print("Test completed")
driver.quit()
