from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-allow-origins=*")
chrome_options.add_argument("--disable-features=VizDisplayCompositor")

driver = webdriver.Remote(
    # UPDATED: Use the dynamic SELENIUM_URL
    command_executor=SELENIUM_URL,
    options=chrome_options
)
wait = WebDriverWait(driver, 10)

# Open URL
# UPDATED: Use BASE_URL for website access
driver.get(BASE_URL)

# Wait and click "Click here"
click_here = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//span[text()="Click here"]'))
)
click_here.click()

# Wait for form to appear
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="First Name"]'))
)

# Fill registration form
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="First Name"]').send_keys("Omer")
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Last Name"]').send_keys("TEST")
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]').send_keys("testuser@example.com")
driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]').send_keys("123Test")

# Click Continue
continue_btn = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]'))
)
continue_btn.click()

time.sleep(2)

print("Registration page title:", driver.title)

driver.quit()
