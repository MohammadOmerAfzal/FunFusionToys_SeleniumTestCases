from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def test_valid_login():
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)

    try:
        driver.get("http://3.214.127.147:5174/")

        # Enter email
        driver.find_element(By.XPATH, "//input[@placeholder='Email']").send_keys("testuser@example.com")

        # Enter password
        driver.find_element(By.XPATH, "//input[@placeholder='Password']").send_keys("123Test")

        # Click Login button
        driver.find_element(By.XPATH, "//button").click()

        time.sleep(2)

        # Check if login succeeded
        if "login" not in driver.current_url:
            print("✅ Login Success!")
        else:
            print("❌ Login Failed!")
    
    finally:
        driver.quit()


# Run directly
if __name__ == "__main__":
    test_valid_login()

