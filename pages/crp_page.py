"""
Change Rate Plan (CRP) journey — every screen after login/logout, which are
handled by the shared LoginPage / ProfilePage.

Maps 1:1 onto the original mbm_ios_crp.py "Transaction 2..8" comments so it's
easy to cross-reference against the original script.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from core.base_page import BasePage


class CRPPage(BasePage):
    # Transaction 2: Service Landing
    SERVICES_BUTTON = (AppiumBy.IOS_PREDICATE, 'label CONTAINS "Services" AND type == "XCUIElementTypeButton"')
    ADD_SERVICE_MARKER = (AppiumBy.ACCESSIBILITY_ID, "Add a service or subscription")

    # Transaction 3: Mobility Overview
    MOBILITY_CHEVRON = (
        AppiumBy.IOS_CLASS_CHAIN,
        '**/XCUIElementTypeImage[`name == "ic_bell_chevronRight-16"`][2]',
    )

    # Transaction 4: Change Rate Plan
    MY_PLAN_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "CommonReusableOverview.actionButtonMyplan")
    CRP_HEADER = (AppiumBy.ACCESSIBILITY_ID, "CRPFlowHeaderView.titleLabel")

    # Transaction 5: Select NBA (Next-Best-Action) Offer
    NBA_OFFER = (
        AppiumBy.IOS_PREDICATE,
        'label == "Upgrade to a new phone and get 20 GB for $60/mo."',
    )
    SELECTED_OFFER_MARKER = (AppiumBy.ACCESSIBILITY_ID, "Your selected offer")

    # Transaction 6 & 7 both use the same "continue" button on the dock summary
    DOCK_CONTINUE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "CRPDockSummaryView.continueButton")
    ADDONS_MARKER = (AppiumBy.ACCESSIBILITY_ID, "Add-ons")
    REVIEW_SUBMIT_MARKER = (AppiumBy.ACCESSIBILITY_ID, "Review & submit order")

    # Transaction 8: Confirmation
    SUBMIT_CHANGES_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Submit changes")
    CONFIRMATION_HEADER = (AppiumBy.ACCESSIBILITY_ID, "CRPNavigationBar.CRPReviewPage.header")
    DONE_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "CRPNavigationBar.doneButton")
    PROFILE_ICON_SERVICE_HEADER = (AppiumBy.ACCESSIBILITY_ID, "ServiceHeaderView.profile")

    # ------------------------------------------------------------------
    def open_service_landing(self):
        self.click(self.SERVICES_BUTTON)
        self.wait_visible(self.ADD_SERVICE_MARKER)

    def open_mobility_overview(self):
        self.click(self.MOBILITY_CHEVRON)
        # Original script left the post-click wait commented out; kept as-is.

    def open_change_rate_plan(self):
        self.swipe_up(1)
        self.click(self.MY_PLAN_BUTTON)
        self.wait_visible(self.CRP_HEADER)

    def select_nba_offer(self):
        self.swipe_up(2)
        self.click(self.NBA_OFFER)
        self.wait_present(self.SELECTED_OFFER_MARKER)
        time.sleep(5)  # original script waits for the offer summary to settle

    def continue_to_addons(self):
        self.click(self.DOCK_CONTINUE_BUTTON)
        self.wait_present(self.ADDONS_MARKER)

    def continue_to_review(self):
        self.click(self.DOCK_CONTINUE_BUTTON)
        self.wait_present(self.REVIEW_SUBMIT_MARKER)

    def submit_changes(self):
        self.swipe_up(2)
        self.click(self.SUBMIT_CHANGES_BUTTON)
        self.wait_present(self.CONFIRMATION_HEADER)

    def return_to_profile(self):
        """After confirmation: tap Done, then open the profile menu so the
        shared ProfilePage.logout() can take over."""
        self.click(self.DONE_BUTTON)
        time.sleep(2)
        self.click(self.PROFILE_ICON_SERVICE_HEADER)
