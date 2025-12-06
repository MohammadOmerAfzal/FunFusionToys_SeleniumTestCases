from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time


def test_product_details_page():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )
    wait = WebDriverWait(driver, 10)

    try:
        print("\n=== TEST: Product Details Page ===")

        # Step 1: Open shop page
        driver.get("http://3.214.127.147:5174/Shop")
        time.sleep(2)

        # Step 2: Select first product card
        products = driver.find_elements(By.CLASS_NAME, "Item")
        if not products:
            print("❌ No products found on Shop page!")
            return

        first_product = products[0]
        product_name = first_product.find_element(By.CLASS_NAME, "item-name").text

        print(f"➡ Clicking first product: {product_name}")

        # Step 3: Click product (opens details page)
        first_product.click()
        time.sleep(2)

        # Step 4: Validate product detail page opened
        title_element = driver.find_element(By.TAG_NAME, "h1")
        detail_title = title_element.text

        if product_name.lower() in detail_title.lower():
            print(f"✅ Product detail page loaded correctly: {detail_title}")
        else:
            print(f"⚠ Title mismatch! Expected: {product_name}, Got: {detail_title}")

        # Step 5: Verify Add to Cart button exists
        try:
            add_to_cart_btn = driver.find_element(By.CLASS_NAME, "add-to-cart-btn")
            print("✅ 'Add to Cart' button is visible.")
        except:
            print("❌ 'Add to Cart' button NOT FOUND!")
            return

        # Step 6: Test button is clickable
        try:
            actions = ActionChains(driver)
            actions.move_to_element(add_to_cart_btn).click().perform()
            print("✅ 'Add to Cart' button is clickable.")
        except:
            print("❌ Add to Cart button is NOT clickable!")

    finally:
        driver.quit()



if __name__ == "__main__":
    test_product_details_page()

