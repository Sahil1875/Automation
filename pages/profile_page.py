"""
Profile menu + Logout — shared across all six journeys.

Two different accessibility ids are used for the profile icon in the
original scripts depending on which screen the user is on ('profile' on the
plain home screen, 'ServiceHeaderView.profile' on some service-detail
screens). Both are exposed here; each flow's page object passes whichever
one matches the screen it's calling from.
"""
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from core.base_page import BasePage


class ProfilePage(BasePage):
    PROFILE_ICON_HOME = (AppiumBy.ACCESSIBILITY_ID, "profile")
    PROFILE_ICON_SERVICE_HEADER = (AppiumBy.ACCESSIBILITY_ID, "ServiceHeaderView.profile")
    LOGOUT_BUTTON = "Log out_identifier"  # accessibility id, needs scrolling to reach
    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Continue")

    def open_profile(self, locator=None):
        """Tap the profile icon. Defaults to the home-screen icon; pass
        PROFILE_ICON_SERVICE_HEADER for screens that use the other id."""
        self.click(locator or self.PROFILE_ICON_HOME)

    def logout(self):
        """Scrolls to and taps 'Log out', then confirms via 'Continue'.
        Call this from inside a `step_timer` block to time it, as the
        original scripts did."""
        logout_btn = self.scroll_to_element_by_accessibility_id(self.LOGOUT_BUTTON)
        logout_btn.click()
        self.click(self.CONTINUE_BUTTON)

    def ensure_logged_out(self, timeout: int = 10):
        """
        Best-effort safety step run at the *start* of every iteration: if a
        previous run left the app logged in, log out now so the flow starts
        from a known state. Does nothing (and doesn't raise) if the app is
        already at the logged-out startup screen.
        """
        try:
            profile_btn = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(self.PROFILE_ICON_HOME)
            )
            profile_btn.click()
            logout_btn = self.scroll_to_element_by_accessibility_id(self.LOGOUT_BUTTON)
            logout_btn.click()
            self.click(self.CONTINUE_BUTTON)
            print("Logout completed (pre-run safety check).")
        except TimeoutException:
            print("Already logged out — no action needed.")
