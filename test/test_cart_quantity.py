from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Try without headless first
driver = webdriver.Chrome()

print("Test: Add items and check cart quantity")

try:
    # Test 1: Add 1 item
    print("\nTest 1: Add 1 item")
    driver.get("http://3.214.127.147:5174/Shop/676d55d151fc50240e3c9070")
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
    time.sleep(2)

    driver.get("http://3.214.127.147:5174/Cart")
    time.sleep(2)

    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
    if cart_items:
        p_tags = cart_items[0].find_elements(By.TAG_NAME, "p")
        if len(p_tags) >= 4:
            print(f"Quantity after adding 1: {p_tags[3].text}")

    # Test 2: Add 2 more (total 3)
    print("\nTest 2: Add 2 more items")
    driver.get("http://3.214.127.147:5174/Shop/676d55d151fc50240e3c9070")
    time.sleep(2)

    for i in range(2):
        driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
        time.sleep(1)

    driver.get("http://3.214.127.147:5174/Cart")
    time.sleep(2)

    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
    if cart_items:
        p_tags = cart_items[0].find_elements(By.TAG_NAME, "p")
        if len(p_tags) >= 4:
            print(f"Quantity after adding 2 more: {p_tags[3].text}")

except Exception as e:
    print(f"Error: {e}")

driver.quit()
