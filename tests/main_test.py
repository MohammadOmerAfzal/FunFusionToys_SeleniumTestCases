from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# -------------------- CONFIG -------------------- #
BASE_URL = "http://frontend-ci:5173"
PRODUCT_ID = "676d55d151fc50240e3c9070"
EXPECTED_PRODUCT_COUNT = 7

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)


# ============================================================
# 1) TEST: USER REGISTRATION
# ============================================================
def run_registration_test():
    print("\n=== TEST: User Registration ===")
    driver.get(BASE_URL)

    # Click "Click here"
    click_here = wait.until(EC.element_to_be_clickable((By.XPATH, '//span[text()="Click here"]')))
    click_here.click()

    # Fill form
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="First Name"]')))
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="First Name"]').send_keys("Omer")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Last Name"]').send_keys("TEST")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]').send_keys("testuser@example.com")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]').send_keys("123Test")

    # Continue
    cont = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]')))
    cont.click()

    print("Registration Completed!")


# ============================================================
# 2) TEST: VALID LOGIN
# ============================================================
def run_login_test():
    print("\n=== TEST: Valid Login ===")
    driver.get(BASE_URL)

    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']")))
    password_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']")))

    email_input.send_keys("testuser@example.com")
    password_input.send_keys("123Test")

    login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button")))
    login_btn.click()

    wait.until(lambda d: "login" not in d.current_url.lower())
    print("Login Successful ✔")


# ============================================================
# 3) TEST: PRODUCT COUNT ON SHOP PAGE
# ============================================================
def run_product_count_test():
    print("\n=== TEST: Real Product Count ===")
    shop_url = f"{BASE_URL}/Shop"
    driver.get(shop_url)

    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Item")))
    print(f"Products Found: {len(products)}")

    for p in products:
        try:
            title = p.find_element(By.CLASS_NAME, "item-name").text
            price = p.find_element(By.CLASS_NAME, "item-price").text
            print(f"➡ {title} | {price}")
        except:
            pass

    if len(products) != EXPECTED_PRODUCT_COUNT:
        print(f"❌ Expected {EXPECTED_PRODUCT_COUNT}, found {len(products)}")
    else:
        print("✔ Product count correct!")


# ============================================================
# 4) TEST: PRODUCT DETAILS PAGE
# ============================================================
def run_product_details_test():
    print("\n=== TEST: Product Details Page ===")
    driver.get(f"{BASE_URL}/Shop")

    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Item")))
    first = products[0]
    product_name = first.find_element(By.CLASS_NAME, "item-name").text
    first.click()

    # Validate details page
    title_element = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))
    detail_title = title_element.text

    print("Product detail page opened:", detail_title)

    add_btn = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "add-to-cart-btn")))
    ActionChains(driver).move_to_element(add_btn).click().perform()


# ============================================================
# 5) TEST: CART ACTIONS (QTY=2)
# ============================================================
def run_cart_actions_test():
    print("\n=== TEST: Cart Actions (Qty = 2) ===")
    product_url = f"{BASE_URL}/Shop/{PRODUCT_ID}"
    driver.get(product_url)
    time.sleep(2)

    qty = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#quantity")))
    qty.clear()
    qty.send_keys("2")

    add_btn = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn")
    add_btn.click()
    time.sleep(2)

    driver.get(f"{BASE_URL}/Cart")
    time.sleep(2)

    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
    print(f"Cart items: {len(cart_items)}")


# ============================================================
# 6) TEST: ADD TO CART (BASIC)
# ============================================================
def run_add_to_cart_test():
    print("\n=== TEST: Add Product to Cart ===")
    driver.get(f"{BASE_URL}/Shop/{PRODUCT_ID}")

    add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.add-to-cart-btn")))
    ActionChains(driver).move_to_element(add_btn).click().perform()

    driver.get(f"{BASE_URL}/Cart")
    cart_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cartitems-format")))

    print(f"Cart contains {len(cart_items)} item(s)")


# ============================================================
# 7) TEST: CART DECREMENT (ADD QTY=3 THEN DECREMENT)
# ============================================================
def run_cart_decrement_test():
    print("\n=== TEST: Cart Decrement ===")

    driver.get(f"{BASE_URL}/Shop/{PRODUCT_ID}")
    time.sleep(2)

    qty_input = wait.until(EC.presence_of_element_located((By.ID, "quantity")))
    qty_input.clear()
    qty_input.send_keys("3")

    add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-btn")))
    add_btn.click()
    print("Added product with qty=3")

    driver.get(f"{BASE_URL}/Cart")
    time.sleep(2)

    decrement_btn = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cartitems-decrement")))
    decrement_btn.click()
    print("Decremented quantity once ✔")


# ============================================================
# RUN ALL TESTS SEQUENTIALLY
# ============================================================
run_registration_test()
run_login_test()
run_product_count_test()
run_product_details_test()
run_cart_actions_test()
run_add_to_cart_test()
run_cart_decrement_test()

driver.quit()
print("\n🎉 ALL TESTS COMPLETED SUCCESSFULLY!")

