from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

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


def test_invalid_email():
    english = wait.until(EC.presence_of_element_located(
        (AppiumBy.XPATH, '//android.widget.TextView[@resource-id="ng.jiji.app:id/tvTitle" and @text="English"]')))

    if english.is_selected():
        print("English radio button is already selected.")
    else:
        print("English radio button is not selected.")
        english.click()

    wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'ng.jiji.app:id/bBuy'))).click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'ng.jiji.app:id/tab_user_text'))).click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'ng.jiji.app:id/tvSignUpOrLogIn'))).click()
    wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'ng.jiji.app:id/bByEmailOrPhone'))).click()

    wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/etEmail'))).send_keys('invalidemail')
    wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/etPassword'))).send_keys('Frug@l123')
    wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/etFirstName'))).send_keys('Frugal')
    wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/etLastName'))).send_keys('Mann')
    wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/etPhone'))).send_keys('09044558877')

    wait.until(EC.element_to_be_clickable((AppiumBy.ID, 'ng.jiji.app:id/bRegister'))).click()

    try:
        error_message = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'ng.jiji.app:id/textinput_error')))
        assert error_message.text == "Incorrect email address, please check the spelling", \
            f"Expected 'Incorrect email address, please check the spelling', but got {error_message.text}"
        print("Error message for invalid email is displayed as expected.")
    except TimeoutException:
        print("Error message element for invalid email was not found.")


test_invalid_email()
driver.quit()
