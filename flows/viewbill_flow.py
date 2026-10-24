"""
ViewBill flow.

Reads Data_Viewbill.csv, runs the full ViewBill journey for every user row,
times each step, writes reports/output_viewbill.xlsx.
"""
import os
import time

from config import settings
from core.driver_factory import create_driver, quit_driver
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from pages.viewbill_page import ViewBillPage
from utils.csv_reader import read_credentials
from utils.timer import step_timer
from utils.report_writer import write_results_to_excel
from utils.popup_handler import dismiss_post_login_popups

DATA_FILE = os.path.join(settings.DATA_DIR, "Data_Viewbill.csv")
REPORT_FILE = "output_viewbill.xlsx"

# The original script used a longer (60s) WebDriverWait for this flow,
# since bill/PDF generation can be slower than other screens.
WAIT_TIMEOUT = 60

RESULT_KEYS = [
    "Login",
    "View Bill",
    "Download PDF",
    "History",
    "Comparison",
    "Logout",
]


def run():
    driver, wait = create_driver(wait_timeout=WAIT_TIMEOUT)

    login_page = LoginPage(driver, wait)
    profile_page = ProfilePage(driver, wait)
    viewbill_page = ViewBillPage(driver, wait)

    results = {key: [] for key in RESULT_KEYS}
    credentials = read_credentials(DATA_FILE)

    try:
        for row in credentials:
            username, password = row["username"], row["password"]
            print(f"\n--- Running ViewBill flow for {username} ---")

            profile_page.ensure_logged_out()
            time.sleep(5)
            login_page.wait_for_startup_screen()
            time.sleep(2)

            login_page.start_login()
            login_page.enter_username(username)
            login_page.enter_password(password)
            with step_timer(results, "Login"):
                login_page.submit()
                dismiss_post_login_popups(driver)
                login_page.wait_for_home()
            time.sleep(5)

            with step_timer(results, "View Bill"):
                viewbill_page.open_view_bill()
            time.sleep(5)

            with step_timer(results, "Download PDF"):
                viewbill_page.download_pdf()
            viewbill_page.dismiss_pdf()

            with step_timer(results, "History"):
                viewbill_page.open_history()
            time.sleep(5)

            with step_timer(results, "Comparison"):
                viewbill_page.open_comparison()
            time.sleep(5)
            viewbill_page.close_comparison()
            time.sleep(5)

            with step_timer(results, "Logout"):
                profile_page.ensure_logged_out()
            time.sleep(5)

            driver.terminate_app(settings.APP_BUNDLE_ID)
            driver.activate_app(settings.APP_BUNDLE_ID)

        write_results_to_excel(results, REPORT_FILE)
        print("\nAll users processed.")
    finally:
        quit_driver(driver)


if __name__ == "__main__":
    run()
