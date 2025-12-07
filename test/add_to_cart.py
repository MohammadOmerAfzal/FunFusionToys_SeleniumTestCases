from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os  # <-- NEW: Import os module to read environment variables

# --- 1. Get Environment Variables ---
# SELENIUM_HOST: The hostname of the Selenium Chrome container (set to 'selenium-node-ci' in Jenkins)
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'localhost')
SELENIUM_URL = f'http://{SELENIUM_HOST}:4444/wd/hub'

# BASE_URL: The base URL of the website frontend (set to 'http://frontend-ci:5173' in Jenkins)
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5173')

# --- 2. Setup Chrome Options ---
chrome_options = Options()
chrome_options.add_argument("--headless")   # Headless mode is essential for CI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--remote-allow-origins=*")

# --- 3. Initialize Remote WebDriver ---
driver = webdriver.Remote(
    # Connects to the host name resolved on the ci-network
    command_executor=SELENIUM_URL,  
    options=chrome_options
)

wait = WebDriverWait(driver, 10)

try:
    # --- 4. Open Product Page ---
    # The URL is now constructed using the BASE_URL from the environment
    PRODUCT_URL = BASE_URL + "/Shop/676d55d151fc50240e3c9070"
    print(f"Opening URL: {PRODUCT_URL}")
    driver.get(PRODUCT_URL)

    # --- 5. Update Quantity ---
    qty_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#quantity")))
    qty_input.clear()
    qty_input.send_keys("2")  # Set quantity to 2

    # --- 6. Click Add to Cart ---
    add_to_cart_btn = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn")
    add_to_cart_btn.click()
    time.sleep(2)  # wait for cart update

    print("Product added to cart successfully!")
    
    # Optional: Add an assertion here to verify cart state if possible
    
finally:
    # --- 7. Cleanup ---
    driver.quit()
