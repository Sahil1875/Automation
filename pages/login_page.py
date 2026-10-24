"""
Login screen — identical across all six journeys, so this is used by every
flow. Split into small steps so the flow can decide exactly what to time
(the original scripts only timed from the 'Log in' tap to the home screen
appearing, not the typing of the credentials).
"""
from appium.webdriver.common.appiumby import AppiumBy

from core.base_page import BasePage


class LoginPage(BasePage):
    ALREADY_CUSTOMER_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "StartupButtonsCell.loginButton")
    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Continue")
    USERNAME_FIELD = (
        AppiumBy.IOS_PREDICATE,
        'name == "Username or email address" AND label == "Username or email address" '
        'AND type == "XCUIElementTypeTextField"',
    )
    PASSWORD_FIELD = (
        AppiumBy.IOS_PREDICATE,
        'type == "XCUIElementTypeSecureTextField" AND visible == 1',
    )
    LOGIN_SUBMIT_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Log in")
    HOME_PROFILE_ICON = (AppiumBy.ACCESSIBILITY_ID, "profile")

    def wait_for_startup_screen(self):
        """Waits for the app's idle/startup screen to be ready."""
        self.wait_present(self.ALREADY_CUSTOMER_BUTTON)

    def start_login(self):
        """Taps 'I'm already a Bell customer' then 'Continue'."""
        self.click(self.ALREADY_CUSTOMER_BUTTON)
        self.click(self.CONTINUE_BUTTON)

    def enter_username(self, username: str):
        field = self.find(self.USERNAME_FIELD)
        field.clear()
        field.send_keys(username)
        self.click(self.CONTINUE_BUTTON)

    def enter_password(self, password: str):
        field = self.find(self.PASSWORD_FIELD)
        field.click()
        field.clear()
        field.send_keys(password)

    def submit(self):
        """Taps the final 'Log in' button. Callers typically time from here."""
        self.click(self.LOGIN_SUBMIT_BUTTON)

    def wait_for_home(self):
        """Waits for the home screen's profile icon to become visible."""
        self.wait_visible(self.HOME_PROFILE_ICON)

    def login(self, username: str, password: str):
        """Full login sequence, untimed — use the individual steps in a flow
        if you need to time only part of it (e.g. just the final submit)."""
        self.wait_for_startup_screen()
        self.start_login()
        self.enter_username(username)
        self.enter_password(password)
        self.submit()
        self.wait_for_home()
