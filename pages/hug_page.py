"""
Hardware Upgrade (HUG) journey — buying a new device on a plan.

This is the longest journey (12 transactions). Method names mirror the
"Transaction N: <name>" comments in the original mbm_ios_hug.py so it's easy
to cross-reference. A few locators were marked `# TODO: add locator` in the
original script — kept as-is below since we don't have access to the live
app to verify better ones; search this file for `TODO`.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from core.base_page import BasePage


class HUGPage(BasePage):
    # Transaction 2: Service Landing
    SERVICES_BUTTON = (AppiumBy.IOS_PREDICATE, 'label CONTAINS "Services" AND type == "XCUIElementTypeButton"')
    ADD_SERVICE_MARKER = (AppiumBy.ACCESSIBILITY_ID, "Add a service or subscription")

    # Transaction 3: Mobility Overview
    MOBILITY_CHEVRON = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeImage[`name == "ic_bell_chevronRight-16"`][1]',
    )
    SHOP_DEVICES_MARKER = (AppiumBy.ACCESSIBILITY_ID, "Shop new devices")

    # Transaction 4: Shop Devices
    SHOP_DEVICES_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Shop new devices")

    # Transaction 5: Device Details
    FEATURES_HIGHLIGHTS_MARKER = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeStaticText[`name == "View features and highlights"`]',
    )

    # Transaction 6: Select Plan Page
    HUG_CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "HugPaymentOptionsSectionView.hugDeviceContinueBtn")  # TODO: add locator
    SELECT_RATE_PLAN_MARKER = (AppiumBy.ACCESSIBILITY_ID, "Select a rate plan")  # TODO: add locator

    # Transaction 6a: Select Plan
    RATE_PLAN_PRICE = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeOther[`name == "HugRatePlanSectionView.hugRatePlanPrice"`][1]',
    )  # TODO: add locator

    # Transaction 6b: Keep It Option
    FIXED_OPTION = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeStaticText[`name == "Fixed Option"`][1]',
    )  # TODO: add locator

    # Transaction 7: Add-On Page
    ADD_ON_STEP_MARKER = (AppiumBy.ACCESSIBILITY_ID, "HUG.DeviceOptionsPricing.stepThreeOfThree")

    # Transaction 08: Continue to Care
    CONTINUE_TO_CARE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "HUG.HUGRatePlan.continueToDeviceCareButton")  # TODO: add locator
    ADDON_CHECKMARK = (AppiumBy.ACCESSIBILITY_ID, "HUG.DeviceAddons.HUGCompatibleAddonCell.checkMark0")  # TODO: add locator

    # Transaction 09: Select SPC plan
    ADDON_CHECKMARK_CHECKED = (
        AppiumBy.IOS_PREDICATE,
        'name == "HUG.DeviceAddons.HUGCompatibleAddonCell.checkMark0" AND label CONTAINS "CHECKED"',
    )

    # Transaction 10: ReviewAndSubmit Page
    DEVICE_CARE_CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "HUG.HUGDeviceCare.continueButton")
    REVIEW_TITLE = (AppiumBy.ACCESSIBILITY_ID, "HUG.Review.largeTitleView")

    # Transaction 11: Confirmation Page
    REVIEW_CANCEL_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "HUG.Review.navigationItem.cancelButton")
    PROFILE_ICON = (AppiumBy.ACCESSIBILITY_ID, "profile")

    # ------------------------------------------------------------------
    def open_service_landing(self):
        self.click(self.SERVICES_BUTTON)
        self.wait_visible(self.ADD_SERVICE_MARKER)

    def open_mobility_overview(self):
        self.click(self.MOBILITY_CHEVRON)
        self.wait_visible(self.SHOP_DEVICES_MARKER)

    def open_shop_devices(self):
        self.click(self.SHOP_DEVICES_BUTTON)
        # Original script's post-click wait was left commented out; kept as-is.

    def open_device_details(self):
        """Selects a device from the shop grid via coordinate taps — the
        original script found no reliable accessible locator for these
        device tiles, so it fell back to tapping fixed coordinates."""
        self.swipe_up(2)
        self.tap(100, 239)
        time.sleep(2)
        self.tap(100, 258)
        self.wait_present(self.FEATURES_HIGHLIGHTS_MARKER)

    def open_select_plan_page(self):
        self.swipe_up(1, pause=2)
        continue_btn = self.find(self.HUG_CONTINUE_BUTTON)
        self.tap(292, 239)
        time.sleep(1)
        continue_btn.click()
        self.wait_present(self.SELECT_RATE_PLAN_MARKER)

    def select_plan(self):
        self.swipe_up(1)
        self.tap(292, 239)
        self.click(self.RATE_PLAN_PRICE)
        self.wait_visible(self.RATE_PLAN_PRICE)

    def choose_keep_it_option(self):
        self.swipe_up(7)
        self.click(self.FIXED_OPTION)
        self.wait_visible(self.FIXED_OPTION)

    def continue_to_addons(self):
        self.click(self.HUG_CONTINUE_BUTTON)
        self.wait_present(self.ADD_ON_STEP_MARKER)

    def continue_to_care(self):
        self.click(self.CONTINUE_TO_CARE_BUTTON)
        self.wait_present(self.ADDON_CHECKMARK)

    def select_spc_plan(self):
        self.click(self.ADDON_CHECKMARK)
        self.wait_visible(self.ADDON_CHECKMARK_CHECKED)

    def continue_to_review(self):
        self.click(self.DEVICE_CARE_CONTINUE_BUTTON)
        self.wait_visible(self.REVIEW_TITLE)

    def confirm_order(self):
        self.swipe_up(5)
        self.tap(200, 750)
        self.wait_present(self.REVIEW_CANCEL_BUTTON)

    def return_to_profile(self):
        """After confirmation: dismiss the review screen and open the
        profile menu so the shared ProfilePage.logout() can take over."""
        self.click(self.REVIEW_CANCEL_BUTTON)
        time.sleep(2)
        self.click(self.PROFILE_ICON)
