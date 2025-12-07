# test/test_register.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import pytest

# --- Dynamic Host Setup ---
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'localhost')
SELENIUM_URL = f'http://{SELENIUM_HOST}:4444/wd/hub'
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5174')

@pytest.fixture
def driver():
    """Setup and teardown for Chrome driver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--remote-allow-origins=*")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    
    driver = webdriver.Remote(
        command_executor=SELENIUM_URL,
        options=chrome_options
    )
    yield driver
    driver.quit()

def test_user_registration(driver):
    """Test user registration flow"""
    wait = WebDriverWait(driver, 10)
    
    print("\nStarting registration test...")
    
    # Open URL
    driver.get(BASE_URL)
    
    # Wait and click "Click here"
    click_here = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="Click here"]'))
    )
    click_here.click()
    
    # Wait for form to appear
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="First Name"]'))
    )
    
    # Fill registration form
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="First Name"]').send_keys("Omer")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Last Name"]').send_keys("TEST")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]').send_keys("testuser@example.com")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]').send_keys("123Test")
    
    # Click Continue
    continue_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]'))
    )
    continue_btn.click()
    
    time.sleep(2)
    
    print("Registration page title:", driver.title)
    print("Registration test completed successfully")
