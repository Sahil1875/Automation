"""
Internet journey — view/change internet package.

Method names mirror the "Transaction N: <name>" comments in the original
mbm_ios_internet.py.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from core.base_page import BasePage


class InternetPage(BasePage):
    # Transaction 2: Service Landing
    SERVICES_BUTTON = (AppiumBy.IOS_PREDICATE, 'label CONTAINS "Services" AND type == "XCUIElementTypeButton"')
    INTERNET_TILE = (
        AppiumBy.IOS_PREDICATE,
        'name == "Internet" AND label == "Internet" AND type == "XCUIElementTypeButton"',
    )

    # Transaction 3: Internet Overview
    CHANGE_PACKAGE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "ChangePackageButton")

    # Transaction 4: Internet Usage
    VIEW_USAGE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "View usage")
    PAGE_LOADING_SPINNER = (AppiumBy.IOS_PREDICATE, 'label == "The requested page is loading."')
    USAGE_TABLE_FIRST_CELL = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeTable/**/XCUIElementTypeCell[1]')
    USAGE_CANCEL_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Cancel_button")

    # Transaction 5: Change
    CURRENT_SOLUTION_SHOW_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "CurrentSolutionShowButton")

    # Transaction 6: Add-On Page
    ICP_SELECT_BUTTON = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "ICPButtonSelect"`][1]')
    CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "ContinueButton")

    # Transaction 7: ReviewAndSubmit Page
    SCROLL_TO_SUBMIT_MARKER = (AppiumBy.ACCESSIBILITY_ID, "Scroll to the bottom to submit your changes")

    # Transaction 8: Confirmation Page
    TERMS_CONDITIONS_TEXT = "ReviewTermsConditionsText"  # accessibility id, needs scrolling to reach
    BACK_TO_INTERNET_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Back to Internet")
    PROFILE_ICON_SERVICE_HEADER = (AppiumBy.ACCESSIBILITY_ID, "ServiceHeaderView.profile")

    # ------------------------------------------------------------------
    def open_service_landing(self):
        self.click(self.SERVICES_BUTTON)
        self.wait_visible(self.INTERNET_TILE)

    def open_internet_overview(self):
        self.click(self.INTERNET_TILE)
        self.wait_visible(self.CHANGE_PACKAGE_BUTTON)

    def view_internet_usage(self):
        self.click(self.VIEW_USAGE_BUTTON)
        self.wait_invisible(self.PAGE_LOADING_SPINNER)
        self.wait_visible(self.USAGE_TABLE_FIRST_CELL)
        time.sleep(2)
        self.click(self.USAGE_CANCEL_BUTTON)

    def start_change_package(self):
        change_btn = self.wait_present(self.CHANGE_PACKAGE_BUTTON)
        change_btn.click()
        self.wait_present(self.CURRENT_SOLUTION_SHOW_BUTTON)

    def continue_to_addons(self):
        self.click(self.ICP_SELECT_BUTTON)
        self.wait_present(self.CONTINUE_BUTTON)

    def continue_to_review(self):
        self.click(self.CONTINUE_BUTTON)
        self.wait_present(self.SCROLL_TO_SUBMIT_MARKER)

    def submit_changes(self):
        self.scroll_to_element_by_accessibility_id(self.TERMS_CONDITIONS_TEXT, max_scrolls=10)
        self.swipe_up(1)
        self.click(self.CONTINUE_BUTTON)
        self.wait_present(self.BACK_TO_INTERNET_BUTTON)

    def return_to_profile(self):
        """After confirmation: go back to the Internet overview, then open
        the profile menu so the shared ProfilePage.logout() can take over."""
        self.click(self.BACK_TO_INTERNET_BUTTON)
        time.sleep(2)
        self.tap(30, 80)
        self.click(self.PROFILE_ICON_SERVICE_HEADER)
