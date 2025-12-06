from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time

PRODUCT_URL = "http://3.214.127.147:5174/Shop/676d55d151fc50240e3c9070"
CART_URL = "http://3.214.127.147:5174/Cart"

# ---- Chrome / Selenium setup ----
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',  # this is the Selenium container
    options=chrome_options
)

wait = WebDriverWait(driver, 15)

def get_cart_row():
    return wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.cartitems-format.cartformat"))
    )

def read_quantity_from_row(row):
    ps = row.find_elements(By.TAG_NAME, "p")
    if len(ps) >= 3:
        digits = "".join(ch for ch in ps[2].text.strip() if ch.isdigit())
        return int(digits) if digits else None
    return None

try:
    print("=" * 60)
    print("TEST: Add product with qty=3 and decrement once")
    print("=" * 60)

    # Go to product page
    driver.get(PRODUCT_URL)
    print("1. Product page opened")

    qty_input = wait.until(EC.presence_of_element_located((By.ID, "quantity")))
    qty_input.clear()
    qty_input.send_keys("3")
    print("2. Set quantity to 3")

    add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-btn")))
    add_btn.click()
    print("3. Product added to cart")
    time.sleep(1.5)

    driver.get(CART_URL)
    print("4. Navigated to cart page")
    time.sleep(1.5)

    row = get_cart_row()
    initial_qty = read_quantity_from_row(row)
    print(f"5. Cart quantity before decrement: {initial_qty}")

    if initial_qty != 3:
        print(f"✗ Expected 3 but got {initial_qty}")
    else:
        print("✓ Quantity is correct (3)")

    print("\nAttempting decrement (click ❌)...")

    # Find ❌ decrement icon
    dec_btn = row.find_element(By.CSS_SELECTOR, "p.remove-icon")

    # Scroll to it
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dec_btn)
    time.sleep(0.3)

    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "p.remove-icon")))
    dec_btn.click()
    print("6. Clicked decrement ❌")

    # Wait for quantity update
    target_qty = initial_qty - 1

    def qty_updated(driver):
        try:
            new_row = driver.find_element(By.CSS_SELECTOR, "div.cartitems-format.cartformat")
            return read_quantity_from_row(new_row) == target_qty
        except:
            return False

    WebDriverWait(driver, 10).until(qty_updated)

    final_row = driver.find_element(By.CSS_SELECTOR, "div.cartitems-format.cartformat")
    updated_qty = read_quantity_from_row(final_row)

    print(f"7. Quantity after decrement: {updated_qty}")

    if updated_qty == target_qty:
        print("✓ Decrement working perfectly!")
    else:
        print(f"✗ Decrement failed. Expected {target_qty}, got {updated_qty}")

except Exception as e:
    print("\n✗ TEST FAILED:", e)
finally:
    print("\nClosing browser...")
    driver.quit()

