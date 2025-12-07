from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json

BASE_URL = "http://frontend-ci:5173"
PRODUCT_ID = "676d55d151fc50240e3c9070"
EXPECTED_PRODUCT_COUNT = 7

# ------------------ Setup Driver ------------------ #
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 20)

# ------------------ Helper ------------------ #
def sleep_for_react(seconds=3):
    time.sleep(seconds)

# ------------------ 1) Registration ------------------ #
def registration_test():
    print("=== TEST: Registration ===")
    driver.get(BASE_URL)
    wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Click here"]'))).click()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="First Name"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="First Name"]').send_keys("Omer")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Last Name"]').send_keys("TEST")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]').send_keys("testuser@example.com")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]').send_keys("123Test")
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]'))).click()
    sleep_for_react()
    print("✅ Registration completed")

# ------------------ 2) Login ------------------ #
def login_test():
    print("=== TEST: Login ===")
    driver.get(BASE_URL)
    wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']"))).send_keys("testuser@example.com")
    driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("123Test")
    driver.find_element(By.TAG_NAME, "button").click()
    sleep_for_react()
    assert "login" not in driver.current_url.lower()
    print("✅ Login successful")

# ------------------ 3) Product Count ------------------ #
def product_count_test():
    print("=== TEST: Product Count ===")
    driver.get(f"{BASE_URL}/Shop")
    sleep_for_react(5)
    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Item")))
    print(f"Products found: {len(products)}")
    for p in products:
        title = p.find_element(By.CLASS_NAME, "item-name").text
        price = p.find_element(By.CLASS_NAME, "item-price").text
        print(f"➡ {title} | {price}")
    assert len(products) == EXPECTED_PRODUCT_COUNT, f"Expected {EXPECTED_PRODUCT_COUNT}, got {len(products)}"
    print("✅ Product count correct")

# ------------------ 4) Product Details ------------------ #
def product_details_test():
    print("=== TEST: Product Details ===")
    driver.get(f"{BASE_URL}/Shop")
    sleep_for_react()
    first_product = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".product-list > div:first-child")))
    product_name = first_product.find_element(By.CLASS_NAME, "item-name").text
    first_product.click()
    sleep_for_react()
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    add_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart-btn")))
    print(f"✅ Product detail opened for: {product_name}")

# ------------------ 5) Cart Actions ------------------ #
def cart_actions_test():
    print("=== TEST: Cart Actions ===")
    driver.get(f"{BASE_URL}/Shop/{PRODUCT_ID}")
    sleep_for_react()
    qty_input = wait.until(EC.presence_of_element_located((By.ID, "quantity")))
    qty_input.clear()
    qty_input.send_keys("2")
    driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
    sleep_for_react()
    driver.get(f"{BASE_URL}/Cart")
    sleep_for_react()
    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
    print(f"Cart items: {len(cart_items)}")
    assert len(cart_items) >= 1
    print("✅ Cart actions completed")

# ------------------ 6) Cart Decrement ------------------ #
def cart_decrement_test():
    print("=== TEST: Cart Decrement ===")
    driver.get(f"{BASE_URL}/Shop/{PRODUCT_ID}")
    sleep_for_react()
    qty_input = wait.until(EC.presence_of_element_located((By.ID, "quantity")))
    qty_input.clear()
    qty_input.send_keys("3")
    driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn").click()
    sleep_for_react()
    driver.get(f"{BASE_URL}/Cart")
    decrement_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cartitems-decrement")))
    decrement_btn.click()
    sleep_for_react()
    print("✅ Cart quantity decremented")

# ------------------ 7) Footer Check ------------------ #
def footer_test():
    print("=== TEST: Footer ===")
    driver.get(BASE_URL)
    footer = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Footer")))
    assert "© 2024" in footer.text
    print("✅ Footer text verified")

# ------------------ Run All Tests ------------------ #
if __name__ == "__main__":
    registration_test()
    login_test()
    product_count_test()
    product_details_test()
    cart_actions_test()
    cart_decrement_test()
    footer_test()
    print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    driver.quit()
