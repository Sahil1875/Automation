"""
Mobile Usage flow.

Reads Data_MobUsage.csv, runs the full Mobile Usage journey for every user
row, times each step, writes reports/output_mobusage.xlsx.
"""
import os
import time

from config import settings
from core.driver_factory import create_driver, quit_driver
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from pages.mob_usage_page import MobUsagePage
from utils.csv_reader import read_credentials
from utils.timer import step_timer
from utils.report_writer import write_results_to_excel
from utils.popup_handler import dismiss_post_login_popups

DATA_FILE = os.path.join(settings.DATA_DIR, "Data_MobUsage.csv")
REPORT_FILE = "output_mobusage.xlsx"

RESULT_KEYS = [
    "Login",
    "Usage Overview",
    "Unbilled Usage",
    "Billing Cycle",
    "Voice Usage",
    "Long Distance Usage",
    "Text Usage",
    "Logout",
]


def run():
    driver, wait = create_driver()

    login_page = LoginPage(driver, wait)
    profile_page = ProfilePage(driver, wait)
    usage_page = MobUsagePage(driver, wait)

    results = {key: [] for key in RESULT_KEYS}
    credentials = read_credentials(DATA_FILE)

    try:
        for row in credentials:
            username, password = row["username"], row["password"]
            print(f"\n--- Running Mobile Usage flow for {username} ---")

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

            with step_timer(results, "Usage Overview"):
                usage_page.open_usage_overview()
            time.sleep(5)

            with step_timer(results, "Unbilled Usage"):
                usage_page.open_unbilled_usage()
            time.sleep(5)

            with step_timer(results, "Billing Cycle"):
                usage_page.change_billing_cycle()
            time.sleep(5)

            with step_timer(results, "Voice Usage"):
                usage_page.view_voice_usage()
            time.sleep(5)

            with step_timer(results, "Long Distance Usage"):
                usage_page.view_long_distance_usage()
            time.sleep(5)

            with step_timer(results, "Text Usage"):
                usage_page.view_text_usage()
            usage_page.close_usage_screen()

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
