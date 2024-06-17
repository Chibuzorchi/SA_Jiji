from appium import webdriver
from typing import Any, Dict
from appium.webdriver.common.appiumby import AppiumBy
from appium.options.common import AppiumOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Define capabilities
cap: Dict[str, Any] = {
    "platformName": "Android",
    "platformVersion": "11",
    "deviceName": "Pixel 8 Pro",
    "automationName": "UIAutomator2",
    "app": "C://jiji-ng-4-9-0-2.apk",
    "fullReset": True,
    "noReset": False
}

url = "http://localhost:4723"
options = AppiumOptions()
options.load_capabilities(cap)
driver = webdriver.Remote(url, options=options)
wait = WebDriverWait(driver, 30)


# Negative Test Case: Invalid phone number
def test_invalid_phone():
    try:
        english = wait.until(EC.presence_of_element_located(
            (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ng.jiji.app:id/tvTitle" and @text="English"]')))
        if not english.is_selected():
            print("English radio button is not selected. Selecting it now.")
            english.click()

        # Navigate through registration steps
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'ng.jiji.app:id/bBuy'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'ng.jiji.app:id/tab_user_text'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'ng.jiji.app:id/tvSignUpOrLogIn'))).click()
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'ng.jiji.app:id/bByEmailOrPhone'))).click()

        # Fill registration form with invalid phone number
        wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/etEmail'))).send_keys(
            'sunkevi@gmail.com')
        wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/etPassword'))).send_keys('Frug@l123')
        wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/etFirstName'))).send_keys('Frugal')
        wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/etLastName'))).send_keys('Mann')
        wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/etPhone'))).send_keys('55445')

        # Submit registration
        wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'ng.jiji.app:id/bRegister'))).click()

        # Add assertion to check for error message related to phone number
        error_message = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/textinput_error')))
        assert "Invalid phone number" in error_message.text, \
            f"Expected 'Invalid phone number' in error message, but got '{error_message.text}'"
        print("Error message for invalid phone number is displayed as expected.")

    except TimeoutException as e:
        print(f"TimeoutException occurred: {str(e)}")
    except AssertionError as e:
        print(f"AssertionError occurred: {str(e)}")
    finally:
        driver.quit()


# Execute test
test_invalid_phone()
