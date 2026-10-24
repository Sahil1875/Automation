"""
TV journey — shortest journey, just an overview screen.

Method names mirror the "Transaction N: <name>" comments in the original
mbm_ios_tv.py.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from core.base_page import BasePage


class TVPage(BasePage):
    # Transaction 2: Services
    SERVICES_BUTTON = (AppiumBy.IOS_PREDICATE, 'label CONTAINS "Services" AND type == "XCUIElementTypeButton"')
    TV_CHEVRON = (AppiumBy.IOS_PREDICATE, 'name == "ic_bell_chevronRight-16"')

    # Transaction 3: TV Overview
    PAY_PER_VIEW_MARKER = (AppiumBy.IOS_PREDICATE, 'name == "Pay-per-view"')
    BACK_BUTTON = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "MOSBackButton"`][1]')
    PROFILE_ICON_SERVICE_HEADER = (AppiumBy.ACCESSIBILITY_ID, "ServiceHeaderView.profile")

    # ------------------------------------------------------------------
    def open_services(self):
        self.click(self.SERVICES_BUTTON)
        self.wait_visible(self.TV_CHEVRON)

    def open_tv_overview(self):
        self.click(self.TV_CHEVRON)
        self.wait_visible(self.PAY_PER_VIEW_MARKER)

    def return_to_profile(self):
        """Untimed navigation back to the profile menu, so the shared
        ProfilePage.logout() can take over."""
        self.click(self.BACK_BUTTON)
        time.sleep(2)
        self.click(self.PROFILE_ICON_SERVICE_HEADER)
        time.sleep(2)
