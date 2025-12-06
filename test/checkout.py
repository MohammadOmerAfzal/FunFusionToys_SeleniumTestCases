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

driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',  # this is the Selenium container
    options=chrome_options
)

print("Starting complete checkout flow...")

# 1. Login
driver.get("http://3.214.127.147:5174/")
time.sleep(2)
driver.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys("m.omarafzal12@gmail.com")
driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("123")
driver.find_element(By.XPATH, "//button").click()
time.sleep(3)
print("Logged in")

# 2. Add to cart
driver.get("http://3.214.127.147:5174/Shop/676d55d151fc50240e3c9070")
time.sleep(3)
driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
time.sleep(2)
print("Added to cart")

# 3. Go to cart
driver.get("http://3.214.127.147:5174/Cart")
time.sleep(3)
print("On cart page")

# 4. Go to checkout
driver.get("http://3.214.127.147:5174/Checkout")
time.sleep(3)
print("On checkout page")

# 5. Fill form
form_data = {
    "fullname": "Test User",
    "address": "123 Test St",
    "city": "Test City",
    "postalcode": "12345",
    "email": "test@example.com"
}

for field, value in form_data.items():
    driver.find_element(By.NAME, field).send_keys(value)
print("Form filled")

# 6. Submit order
driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]").click()
time.sleep(5)
print("Order submitted")

# Handle the success alert
try:
    alert = driver.switch_to.alert
    alert_text = alert.text
    print(f"✅ ALERT: {alert_text}")
    alert.accept()  # Click OK on the alert
    print("✅ Alert accepted")
except:
    print("No alert present")

# Now you can take screenshot
driver.save_screenshot("result.png")
print("✅ Screenshot saved: result.png")

# 7. Save result
driver.save_screenshot("result.png")
print(f"Final URL: {driver.current_url}")
print("Check result.png for final state")

driver.quit()
