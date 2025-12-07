from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def test_cart_decrement(driver, wait, base_url):
    """Test: Add product with qty=3 and decrement once"""
    print("\n▶️ Test: Cart Decrement")
    
    product_url = f"{base_url}/Shop/676d55d151fc50240e3c9070"
    cart_url = f"{base_url}/Cart"
    
    # Go to product page
    driver.get(product_url)
    print("1. Product page opened")
    time.sleep(2)
    
    # Set quantity to 3
    qty_input = wait.until(EC.presence_of_element_located((By.ID, "quantity")))
    qty_input.clear()
    qty_input.send_keys("3")
    print("2. Set quantity to 3")
    
    # Add to cart
    add_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".add-to-cart-btn")))
    add_btn.click()
    print("3. Product added to cart")
    time.sleep(2)
    
    # Go to cart
    driver.get(cart_url)
    print("4. Navigated to cart page")
    time.sleep(2)
    
    # Read initial quantity
    def read_quantity_from_row(row):
        ps = row.find_elements(By.TAG_NAME, "p")
        if len(ps) >= 3:
            digits = "".join(ch for ch in ps[2].text.strip() if ch.isdigit())
            return int(digits) if digits else None
        return None
    
    row = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.cartitems-format.cartformat"))
    )
    initial_qty = read_quantity_from_row(row)
    print(f"5. Cart quantity before decrement: {initial_qty}")
    
    assert initial_qty == 3, f"Expected quantity 3, got {initial_qty}"
    print("✓ Quantity is correct (3)")
    
    # Click decrement button
    dec_btn = row.find_element(By.CSS_SELECTOR, "p.remove-icon")
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dec_btn)
    time.sleep(0.5)
    
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "p.remove-icon")))
    dec_btn.click()
    print("6. Clicked decrement ❌")
    
    time.sleep(2)
    
    # Read updated quantity
    final_row = driver.find_element(By.CSS_SELECTOR, "div.cartitems-format.cartformat")
    updated_qty = read_quantity_from_row(final_row)
    print(f"7. Quantity after decrement: {updated_qty}")
    
    assert updated_qty == 2, f"Expected quantity 2, got {updated_qty}"
    print("✅ Decrement working perfectly!")
