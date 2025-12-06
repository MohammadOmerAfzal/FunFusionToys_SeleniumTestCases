from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ---------- Setup Chrome ----------
chrome_options = Options()
chrome_options.add_argument("--headless")  # remove if you want to see the browser
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',  # this is the Selenium container
    options=chrome_options
)

wait = WebDriverWait(driver, 10)

try:
    # ---------- Open Product Page ----------
    driver.get("http://3.214.127.147:5174/Shop/676d55d151fc50240e3c9070")

    # ---------- Update Quantity ----------
    qty_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input#quantity")))
    qty_input.clear()
    qty_input.send_keys("2")  # Set quantity to 2

    # ---------- Click Add to Cart ----------
    add_to_cart_btn = driver.find_element(By.CSS_SELECTOR, "button.add-to-cart-btn")
    add_to_cart_btn.click()
    time.sleep(2)  # wait for cart update

    print("Product added to cart successfully!")

finally:
    driver.quit()

