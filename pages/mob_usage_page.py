"""
Mobile Usage journey — Voice / Long Distance / Text usage screens.

Method names mirror the "Transaction N: <name>" comments in the original
mbm_ios_mobUsage.py.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from core.base_page import BasePage


class MobUsagePage(BasePage):
    # Transaction 2: Usage Overview
    VIEW_USAGE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "ViewUsageButton")
    DATA_USAGE_TILE = (
        AppiumBy.IOS_PREDICATE,
        'name == "UsageOverviewCategoryCell_Data" AND '
        'label == "Data 2.83 GB used  View usage details BUTTON"',
    )

    # Transaction 3: Unbilled Usage
    USAGE_HEADER = (AppiumBy.ACCESSIBILITY_ID, "UsageHeader")

    # Transaction 4: Billing Cycle (dropdown)
    BILLING_CYCLE_DROPDOWN_ARROW = (AppiumBy.ACCESSIBILITY_ID, "down_arrow_fill")
    BILLING_PERIOD_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "UsageBillingPeriodButton")

    # Transaction 5: Voice Usage
    VOICE_TAB = (AppiumBy.ACCESSIBILITY_ID, " VOICE ")
    NO_USAGE_MARKER = (AppiumBy.ACCESSIBILITY_ID, "No usage")

    # Transaction 6: Long Distance Usage
    LONG_DISTANCE_TAB = (AppiumBy.ACCESSIBILITY_ID, " LONG DIST. ")
    LONG_DISTANCE_DETAIL = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeWindow[1]/XCUIElementTypeOther[2]/XCUIElementTypeOther/'
        'XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/XCUIElementTypeOther/'
        'XCUIElementTypeOther[2]/XCUIElementTypeOther/XCUIElementTypeOther[2]/XCUIElementTypeOther',
    )

    # Transaction 7: Text Usage
    TEXT_TAB = (AppiumBy.ACCESSIBILITY_ID, " TEXT ")

    # ------------------------------------------------------------------
    def open_usage_overview(self):
        self.click(self.VIEW_USAGE_BUTTON)
        self.wait_visible(self.DATA_USAGE_TILE)

    def open_unbilled_usage(self):
        self.click(self.DATA_USAGE_TILE)
        self.wait_visible(self.USAGE_HEADER)

    def change_billing_cycle(self):
        """Opens the billing-cycle dropdown and picks a different cycle via
        coordinate taps — the dropdown list items have no accessible locator
        in the original app build."""
        self.click(self.BILLING_CYCLE_DROPDOWN_ARROW)
        time.sleep(2)
        self.tap(183, 783)
        time.sleep(2)
        self.tap(360, 615)
        self.wait_visible(self.BILLING_PERIOD_BUTTON)

    def view_voice_usage(self):
        self.wait_present(self.VOICE_TAB).click()
        self.wait_present(self.NO_USAGE_MARKER)

    def view_long_distance_usage(self):
        self.click(self.LONG_DISTANCE_TAB)
        self.wait_present(self.LONG_DISTANCE_DETAIL)

    def view_text_usage(self):
        """Timed portion only — call close_usage_screen() afterwards
        (outside the timer) to back out, matching the original script."""
        self.click(self.TEXT_TAB)
        self.wait_present(self.USAGE_HEADER)

    def close_usage_screen(self):
        """Backs out of the usage detail modal. Untimed in the original
        script — call this after view_text_usage(), outside the timer."""
        time.sleep(5)
        self.tap(24, 72)   # back
        time.sleep(5)
        self.tap(360, 70)  # close
