from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_real_product_count():
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
        driver.get("http://3.214.127.147:5174/Shop")
        time.sleep(2)

        # Count ONLY real product cards — class="Item"
        products = driver.find_elements(By.CLASS_NAME, "Item")

        print(f"🛒 Real product cards found = {len(products)}")

        # Print titles & prices
        for p in products:
            title = p.find_element(By.CLASS_NAME, "item-name").text
            price = p.find_element(By.CLASS_NAME, "item-price").text
            print(f"➡ {title} | {price}")

        if len(products) == 7:
            print("✅ Product count is correct (7 products).")
        else:
            print("⚠ Product count mismatch!")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_real_product_count()


