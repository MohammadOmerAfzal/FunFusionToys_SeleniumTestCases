from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Setup
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service("/usr/local/bin/chromedriver")
driver = webdriver.Chrome(service=service, options=chrome_options)

print("Testing: Unauthorized users cannot place orders")
print("=" * 50)

# 1. Add product to cart (without login)
print("\n1. Adding product to cart...")
driver.get("http://3.214.127.147:5174/Shop/676d55d151fc50240e3c9070")
time.sleep(2)
driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
time.sleep(2)
print("   ✓ Product added to cart")

# 2. Go to checkout page
print("\n2. Going to checkout page...")
driver.get("http://3.214.127.147:5174/Checkout")
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
    print(f"   ✓ Filled {field_name}")

# 4. Try to place order
print("\n4. Attempting to place order...")
driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]").click()
time.sleep(3)

# 5. Check for login requirement
print("\n5. Checking result...")
try:
    alert = driver.switch_to.alert
    alert_text = alert.text
    print(f"   Alert message: '{alert_text}'")
    
    # Check if login is required
    if "login" in alert_text.lower():
        print("\n✅ TEST PASSED: Unauthorized users cannot place orders!")
        print("   Reason: Login requirement alert shown")
    elif "sign in" in alert_text.lower():
        print("\n✅ TEST PASSED: Unauthorized users cannot place orders!")
        print("   Reason: Sign in requirement alert shown")
    else:
        print(f"\n❌ TES PASSED: alert detected - '{alert_text}'")
        
    alert.accept()
    
except:
    print("\n❌ TEST FAILED: No alert - order might have been placed!")

print("\n" + "=" * 50)
print("Test completed")
driver.quit()
