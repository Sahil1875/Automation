"""
ViewBill journey — view bill, download PDF, history, and usage comparison.

Method names mirror the "Transaction N: <name>" comments in the original
mbm_ios_viewbill.py.
"""
import time
from appium.webdriver.common.appiumby import AppiumBy

from core.base_page import BasePage


class ViewBillPage(BasePage):
    # Transaction 2: View Bill
    BILLING_TAB = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeButton[`name == "Billing"`][1]')
    AMOUNT_DUE_MARKER = (AppiumBy.IOS_CLASS_CHAIN, '**/XCUIElementTypeStaticText[`name == "AmountDue"`]')

    # Transaction 3: Download PDF
    DOWNLOAD_PDF_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Download (PDF)")
    CANCEL_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Cancel")

    # Transaction 4: History
    HISTORY_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "History")
    HISTORY_MARKER = (AppiumBy.ACCESSIBILITY_ID, "HISTORY")

    # Transaction 5: Comparison
    COMPARISON_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Comparison")
    COMPARISON_GRAPH_MARKER = (AppiumBy.ACCESSIBILITY_ID, "PreviousrBarGraph")
    CLOSE_BUTTON = (AppiumBy.IOS_PREDICATE, 'type == "XCUIElementTypeButton" AND name == "Close"')

    # ------------------------------------------------------------------
    def open_view_bill(self):
        self.click(self.BILLING_TAB)
        self.wait_visible(self.AMOUNT_DUE_MARKER)

    def download_pdf(self):
        self.click(self.DOWNLOAD_PDF_BUTTON)
        self.wait_visible(self.CANCEL_BUTTON)

    def dismiss_pdf(self):
        """Untimed in the original script — call after download_pdf()."""
        self.click(self.CANCEL_BUTTON)
        time.sleep(5)

    def open_history(self):
        self.click(self.HISTORY_BUTTON)
        self.wait_visible(self.HISTORY_MARKER)

    def open_comparison(self):
        self.click(self.COMPARISON_BUTTON)
        self.wait_visible(self.COMPARISON_GRAPH_MARKER)

    def close_comparison(self):
        """Untimed in the original script — call after open_comparison()."""
        self.wait_present(self.CLOSE_BUTTON).click()
