# test_real_product_count.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

EXPECTED_PRODUCT_COUNT = 7  # Adjust based on your actual expected products

def test_real_product_count(driver, wait, base_url):
    """
    Test to count the number of real products on the Shop page
    and print their titles and prices.
    """
    shop_url = f"{base_url}/Shop"
    print(f"Opening Shop URL: {shop_url}")
    driver.get(shop_url)

    # Wait until product cards appear
    products = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Item")))
    product_count = len(products)
    print(f"🛒 Real product cards found = {product_count}")

    # Print product titles & prices
    for p in products:
        try:
            title = p.find_element(By.CLASS_NAME, "item-name").text
            price = p.find_element(By.CLASS_NAME, "item-price").text
            print(f"➡ {title} | {price}")
        except Exception as e:
            print(f"Error reading product details: {e}")

    # Assert the expected number of products
    assert product_count == EXPECTED_PRODUCT_COUNT, \
        f"Expected {EXPECTED_PRODUCT_COUNT} products, found {product_count}"
    print("✅ Product count is correct")
