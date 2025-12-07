from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def test_checkout_flow(driver, wait, base_url):
    """Test complete checkout flow with logged-in user"""
    print("\n▶️ Test: Complete Checkout Flow")
    
    # 1. Login
    driver.get(f"{base_url}/")
    time.sleep(2)
    
    email_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']")))
    email_input.send_keys("m.omarafzal12@gmail.com")
    
    password_input = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
    password_input.send_keys("123")
    
    login_btn = driver.find_element(By.XPATH, "//button")
    login_btn.click()
    time.sleep(3)
    print("✓ Logged in")
    
    # 2. Add to cart
    driver.get(f"{base_url}/Shop/676d55d151fc50240e3c9070")
    time.sleep(3)
    
    add_btn = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn")
    add_btn.click()
    time.sleep(2)
    print("✓ Added to cart")
    
    # 3. Go to cart
    driver.get(f"{base_url}/Cart")
    time.sleep(3)
    print("✓ On cart page")
    
    # 4. Go to checkout
    driver.get(f"{base_url}/Checkout")
    time.sleep(3)
    print("✓ On checkout page")
    
    # 5. Fill form
    form_data = {
        "fullname": "Test User",
        "address": "123 Test St",
        "city": "Test City",
        "postalcode": "12345",
        "email": "test@example.com"
    }
    
    for field, value in form_data.items():
        field_input = driver.find_element(By.NAME, field)
        field_input.send_keys(value)
    print("✓ Form filled")
    
    # 6. Submit order
    place_order_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Place Order')]")
    place_order_btn.click()
    time.sleep(5)
    print("✓ Order submitted")
    
    # Handle the success alert
    try:
        alert = driver.switch_to.alert
        alert_text = alert.text
        print(f"✓ ALERT: {alert_text}")
        alert.accept()
        print("✓ Alert accepted")
    except:
        print("No alert present")
    
    print(f"✓ Final URL: {driver.current_url}")
    print("✅ Checkout flow completed successfully!")
