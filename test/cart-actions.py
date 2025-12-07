from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os # <-- NEW: Import os module

# --- Dynamic Host Setup (Required for CI) ---
# SELENIUM_HOST will be 'selenium-node-ci' (container name)
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'localhost')
SELENIUM_URL = f'http://{SELENIUM_HOST}:4444/wd/hub'

# BASE_URL will be 'http://frontend-ci:5173' (internal service name and port)
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5174') 
# --------------------------------------------

# -----------------------------
# Chrome Options for EC2
# -----------------------------
chrome_options = Options()
chrome_options.add_argument("--headless=new")  # New headless mode
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("--remote-allow-origins=*")

# -----------------------------
# Driver Setup
# -----------------------------
driver = webdriver.Remote(
    # UPDATED: Use the dynamic SELENIUM_URL
    command_executor=SELENIUM_URL,  
    options=chrome_options
)

print("WebDriver initialized")

# -----------------------------
# Step 1: Open Product Page directly
# -----------------------------
product_id = "676d55d151fc50240e3c9070"
# UPDATED: Use the dynamic BASE_URL
product_url = f"{BASE_URL}/Shop/{product_id}" 

print(f"Opening: {product_url}")
driver.get(product_url)
time.sleep(5)  # Give ample time to load

# Check if page loaded
print(f"Page title: {driver.title}")
print(f"Current URL: {driver.current_url}")

# Save screenshot to debug
driver.save_screenshot("step1_product_page.png")
print("Screenshot saved: step1_product_page.png")

# -----------------------------
# Step 2: Find and Click Add to Cart button
# -----------------------------
# Try multiple selectors since we can't see the page
selectors_to_try = [
    "button.add-to-cart-btn",
    ".add-to-cart-btn",
    "button[class*='cart']",
    "//button[contains(text(), 'Add')]",
    "//button[contains(text(), 'Cart')]",
    "button"
]

button_found = False
for selector in selectors_to_try:
    try:
        if selector.startswith("//"):
            button = driver.find_element(By.XPATH, selector)
        else:
            button = driver.find_element(By.CSS_SELECTOR, selector)
        
        print(f"Found button with selector: {selector}")
        print(f"Button text: {button.text}")
        print(f"Button class: {button.get_attribute('class')}")
        
        # Click the button
        driver.execute_script("arguments[0].click();", button)
        print("Clicked Add to Cart button!")
        button_found = True
        break
    except Exception as e:
        continue

if not button_found:
    print("ERROR: Could not find Add to Cart button")
    # List all buttons on page
    buttons = driver.find_elements(By.TAG_NAME, "button")
    print(f"Found {len(buttons)} buttons on page:")
    for i, btn in enumerate(buttons):
        print(f"  Button {i+1}: '{btn.text}' class='{btn.get_attribute('class')}'")
    
    # Save HTML for debugging
    with open("page_source.html", "w") as f:
        f.write(driver.page_source)
    print("Page source saved to page_source.html")

time.sleep(2)

# -----------------------------
# Step 3: Go to Cart Page
# -----------------------------
# UPDATED: Use the dynamic BASE_URL
cart_url = f"{BASE_URL}/Cart"
print(f"\nOpening Cart: {cart_url}")
driver.get(cart_url)
time.sleep(3)

# Save screenshot
driver.save_screenshot("step2_cart_page.png")
print("Screenshot saved: step2_cart_page.png")

# Check cart contents
try:
    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
    print(f"Cart items found: {len(cart_items)}")
    
    if cart_items:
        # Get product name
        product_name = driver.find_element(By.CSS_SELECTOR, ".cartitems-format p").text
        print(f"Product in cart: {product_name}")
        
        # Get cart total
        totals = driver.find_elements(By.XPATH, "//*[contains(text(), 'Rs.')]")
        for total in totals:
            print(f"Found price: {total.text}")
    else:
        print("Cart appears to be empty")
        
except Exception as e:
    print(f"Error checking cart: {e}")

# -----------------------------
# Cleanup
# -----------------------------
print("\nTest completed")
driver.quit()
