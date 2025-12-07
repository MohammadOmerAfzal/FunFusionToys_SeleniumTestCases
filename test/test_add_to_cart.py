from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def test_cart_actions(driver, wait, base_url):
    """Test cart actions - add product with custom quantity"""
    print("\n▶️ Test: Cart Actions - Add with Quantity 2")
    
    # Step 1: Open Product Page
    product_url = f"{base_url}/Shop/676d55d151fc50240e3c9070"
    print(f"Opening URL: {product_url}")
    driver.get(product_url)
    time.sleep(2)
    
    # Step 2: Update Quantity to 2
    qty_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#quantity")))
    qty_input.clear()
    qty_input.send_keys("2")
    print("✓ Set quantity to 2")
    
    # Step 3: Click Add to Cart
    add_to_cart_btn = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn")
    add_to_cart_btn.click()
    time.sleep(2)
    print("✓ Product added to cart successfully!")
    
    # Optional: Verify cart state
    cart_url = f"{base_url}/Cart"
    driver.get(cart_url)
    time.sleep(2)
    
    # Check if item is in cart
    cart_items = driver.find_elements(By.CSS_SELECTOR, ".cartitems-format")
    assert len(cart_items) > 0, "Cart is empty - product was not added"
    
    print(f"✓ Cart has {len(cart_items)} item(s)")
    print("✅ Cart actions test completed successfully!")
