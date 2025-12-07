import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait

# Dynamic configuration
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'localhost')
SELENIUM_URL = f'http://{SELENIUM_HOST}:4444/wd/hub'
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5174')

@pytest.fixture(scope="function")
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
    
    print(f"\n🔧 Connecting to Selenium at: {SELENIUM_URL}")
    
    driver = webdriver.Remote(
        command_executor=SELENIUM_URL,
        options=chrome_options
    )
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    """Provides BASE_URL to all tests"""
    return BASE_URL

@pytest.fixture(scope="function")
def wait(driver):
    """Provides WebDriverWait instance"""
    return WebDriverWait(driver, 10)
