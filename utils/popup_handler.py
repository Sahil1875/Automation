"""
Handles the assorted popups the Bell app can show right after login.
None of these are guaranteed to appear, so each one is a best-effort,
timeout-bounded dismiss — never raises if the popup doesn't show up.
"""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


def handle_marketing_popup(driver, timeout: int = 15):
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, "No thanks, maybe later")
            )
        ).click()
        print("Marketing popup dismissed.")
    except TimeoutException:
        print("Marketing popup not shown.")


def handle_face_id_popup(driver, timeout: int = 10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (AppiumBy.ACCESSIBILITY_ID, "BiometricsView.notNowButton")
            )
        ).click()
        print("Face ID popup dismissed.")
    except TimeoutException:
        print("Face ID popup not shown.")


def handle_push_notification_popup(driver, timeout: int = 10):
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "NotNowThanksButton"))
        ).click()
        print("Push notification popup dismissed.")
    except TimeoutException:
        print("Push notification popup not shown.")


def dismiss_post_login_popups(driver):
    """Convenience wrapper: call this once, right after tapping 'Log in'."""
    handle_marketing_popup(driver)
    handle_face_id_popup(driver)
    handle_push_notification_popup(driver)
