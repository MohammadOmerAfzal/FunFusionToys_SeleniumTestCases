# test_cart_quantity.py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import pytest

# --- Dynamic Host Setup ---
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'localhost')
SELENIUM_URL = f'http://{SELENIUM_HOST}:4444'
BASE_URL = os.environ.get('BASE_URL', 'http://localhost:5174')

PRODUCT_DETAIL_URL = f"{BASE_URL}/Shop/676d55d151fc50240e3c9070"
CART_URL = f"{BASE_URL}/Cart"

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

def test_cart_quantity(driver):
    """Test: Add items and check cart quantity"""
    wait = WebDriverWait(driver, 10)
    
    print("\nTest 1: Add 1 item")
    driver.get(PRODUCT_DETAIL_URL)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
    time.sleep(2)
    
    driver.get(CART_URL)
    time.sleep(2)
    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
    
    assert len(cart_items) > 0, "No cart items found"
    
    p_tags = cart_items[0].find_elements(By.TAG_NAME, "p")
    if len(p_tags) >= 4:
        print(f"Quantity after adding 1: {p_tags[3].text}")
        assert p_tags[3].text == "1", f"Expected quantity 1, got {p_tags[3].text}"
    
    print("\nTest 2: Add 2 more items")
    driver.get(PRODUCT_DETAIL_URL)
    time.sleep(2)
    for i in range(2):
        driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
        time.sleep(1)
    
    driver.get(CART_URL)
    time.sleep(2)
    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
    
    if cart_items:
        p_tags = cart_items[0].find_elements(By.TAG_NAME, "p")
        if len(p_tags) >= 4:
            print(f"Quantity after adding 2 more: {p_tags[3].text}")
            assert p_tags[3].text == "3", f"Expected quantity 3, got {p_tags[3].text}"
    
    print("Test case Passed")
