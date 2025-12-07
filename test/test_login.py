# test_valid_login.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

def test_valid_login(driver, wait, base_url):
    """
    Test user login flow using fixtures from conftest.py.
    Verifies that the login succeeds.
    """
    print("\n▶️ Test: Valid User Login")

    # Step 1: Open homepage/login page
    driver.get(base_url)

    # Step 2: Enter email
    email_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email']"))
    )
    email_input.send_keys("testuser@example.com")

    # Step 3: Enter password
    password_input = wait.until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Password']"))
    )
    password_input.send_keys("123Test")

    # Step 4: Click login button
    login_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, "//button"))
    )
    login_btn.click()

    # Step 5: Verify login success
    # Wait until URL changes or dashboard element appears (replace with actual selector)
    # Here we wait until URL does NOT contain 'login'
    try:
        wait.until(lambda d: "login" not in d.current_url.lower())
        print(f"✅ Login Success! Current URL: {driver.current_url}")
    except:
        pytest.fail(f"❌ Login Failed! Still on login page: {driver.current_url}")
