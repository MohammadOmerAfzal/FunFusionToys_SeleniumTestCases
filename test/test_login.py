from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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


def test_valid_login():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")

    driver = webdriver.Remote(
        # UPDATED: Use the dynamic SELENIUM_URL
        command_executor=SELENIUM_URL,
        options=options
    )
    # The wait object needs to be defined
    wait = WebDriverWait(driver, 10) 

    try:
        # UPDATED: Use BASE_URL for website access
        driver.get(BASE_URL)

        # Enter email
        driver.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys("testuser@example.com")

        # Enter password
        driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("123Test")

        # Click Login button
        driver.find_element(By.XPATH, "//button").click()

        time.sleep(2)

        # Check if login succeeded
        if "login" not in driver.current_url.lower():
            print("✅ Login Success!")
        else:
            print("❌ Login Failed!")
    
    finally:
        driver.quit()


# Run directly
if __name__ == "__main__":
    test_valid_login()
