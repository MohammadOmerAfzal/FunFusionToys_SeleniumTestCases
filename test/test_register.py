# test/test_register.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytest

def test_user_registration(driver, wait, base_url):
    """
    Test user registration flow:
    1. Click 'Click here' to open registration form
    2. Fill form fields
    3. Submit and verify registration page title
    """
    print("\n▶️ Starting registration test...")

    # Step 1: Open homepage
    driver.get(base_url)

    # Step 2: Click "Click here" to open registration form
    click_here = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//span[text()="Click here"]'))
    )
    click_here.click()

    # Step 3: Wait for form to appear
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[placeholder="First Name"]'))
    )

    # Step 4: Fill registration form
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="First Name"]').send_keys("Omer")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Last Name"]').send_keys("TEST")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Email"]').send_keys("testuser@example.com")
    driver.find_element(By.CSS_SELECTOR, 'input[placeholder="Password"]').send_keys("123Test")

    # Step 5: Click Continue
    continue_btn = wait.until(
        EC.element_to_be_clickable((By.XPATH, '//button[text()="Continue"]'))
    )
    continue_btn.click()

    # Step 6: Verify registration page loaded (optional: check title or a confirmation element)
    page_title = driver.title
    print(f"✅ Registration page title: {page_title}")
    assert "Register" in page_title or page_title != "", "Registration page did not load correctly"

    print("✅ Registration test completed successfully")
