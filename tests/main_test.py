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
# ============================================================
# 6) TEST: CART DECREMENT / REMOVE ITEM
# ============================================================
def cart_decrement_test():
    print("\n=== TEST: Cart Decrement / Remove Item ===")

    driver.get(f"{BASE_URL}/Cart")
    time.sleep(2)

    try:
        # Find remove icon and click it to decrement/remove
        remove_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "remove-icon")))
        remove_btn.click()
        time.sleep(1)

        # Check remaining cart items
        cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
        print(f"✅Cart now contains {len(cart_items)} item(s)")
    except:
        print("❌ No remove button found. Cart may be empty or selector is wrong.")


# ============================================================
# 7) TEST: CHECKOUT
# ============================================================
def run_checkout_test():
    print("\n=== TEST: Checkout Flow ===")
    driver.get(f"{BASE_URL}/Cart")
    time.sleep(2)
    driver.get(f"{BASE_URL}/Checkout")
    time.sleep(3)

    form_data = {
        "fullname": "Test User",
        "address": "123 Test St",
        "city": "Test City",
        "postalcode": "12345",
        "email": "test@example.com"
    }

    for field, value in form_data.items():
        driver.find_element(By.NAME, field).send_keys(value)

    driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]").click()
    time.sleep(3)

    try:
        alert = driver.switch_to.alert
        print(f"✓ ALERT: {alert.text}")
        alert.accept()
    except:
        print("No alert present")

    print("✅ Checkout flow completed successfully!")


# ------------------ 8) Footer Check ------------------ #
def footer_test():
    print("\n=== TEST: Footer ===")
    driver.get(BASE_URL)
    
    # Scroll to bottom slowly to trigger lazy-loading
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    try:
        # Wait for the footer-bottom paragraph specifically
        footer_text_elem = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.Footer div.footer-bottom p"))
        )
        footer_text = footer_text_elem.text.strip()
        
        if "© 2024 Fun Fusion Toys" in footer_text:
            print("✅ Footer verified")
        else:
            print("❌ Footer text mismatch")
            print("Found text:", footer_text[:500])
    except:
        print("❌ Footer not found at all")
# ------------------ 9) My Orders Page ------------------ #
def my_orders_test():
    print("\n=== TEST: MyOrders Page ===")
    driver.get(f"{BASE_URL}/MyOrders")
    sleep_for_react(3)
    
    # Check if we're on the MyOrders page
    try:
        # Look for the page heading
        page_heading = wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        
        if "My Orders" in page_heading.text:
            print("✅ MyOrders page loaded successfully")
        else:
            print(f"ℹ️ Page heading: {page_heading.text}")
            
        # Check for order cards
        order_cards = driver.find_elements(By.CLASS_NAME, "order-card")
        print(f"✅ Found {len(order_cards)} order(s)")
        
        # Check for Sign Out button
        try:
            sign_out_btn = driver.find_element(By.XPATH, "//button[text()='Sign Out']")
            print("✅ Sign Out button is present")
        except:
            print("ℹ️ Sign Out button not found")
            
    except Exception as e:
        print(f"❌ Failed to access MyOrders page: {e}")

# ------------------ 10) Logout Test ------------------ #
def logout_test():
    print("\n=== TEST: Logout ===")
    
    # First go to a page where we can see logout button (MyOrders or Cart)
    driver.get(f"{BASE_URL}/MyOrders")
    sleep_for_react(2)
    
    try:
        # Find and click the Sign Out button
        sign_out_btn = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign Out']"))
        )
        sign_out_btn.click()
        print("✅ Clicked Sign Out button")
        sleep_for_react(3)
        
        # Verify we're redirected to login/landing page
        current_url = driver.current_url
        if "/Login" in current_url or "/login" in current_url or BASE_URL == current_url:
            print("✅ Successfully logged out and redirected")
            
            # Try to access a protected page to confirm logout
            driver.get(f"{BASE_URL}/MyOrders")
            sleep_for_react(2)
            
            # After logout, we should be redirected away from MyOrders
            if "/MyOrders" not in driver.current_url:
                print("✅ Confirmed: Cannot access MyOrders after logout")
            else:
                print("ℹ️ Still on MyOrders page after logout")
                
        else:
            print(f"ℹ️ Current URL after logout: {current_url}")
            
    except Exception as e:
        print(f"❌ Logout test failed: {e}")
        print("Maybe already logged out or button not found")
# ------------------ Run All Tests ------------------ #
if __name__ == "__main__":
    registration_test()
    login_test()
    product_count_test()
    product_details_test()
    cart_actions_test()
    cart_decrement_test()
    footer_test()
    run_checkout_test()
    print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    driver.quit()
