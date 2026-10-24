"""
TV flow.

Reads Data_TV.csv, runs the full TV journey for every user row, times each
step, writes reports/output_tv.xlsx.
"""
import os
import time

from config import settings
from core.driver_factory import create_driver, quit_driver
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from pages.tv_page import TVPage
from utils.csv_reader import read_credentials
from utils.timer import step_timer
from utils.report_writer import write_results_to_excel
from utils.popup_handler import dismiss_post_login_popups

DATA_FILE = os.path.join(settings.DATA_DIR, "Data_TV.csv")
REPORT_FILE = "output_tv.xlsx"

RESULT_KEYS = ["Login", "Services", "TV Overview", "Logout"]


def run():
    driver, wait = create_driver()

    login_page = LoginPage(driver, wait)
    profile_page = ProfilePage(driver, wait)
    tv_page = TVPage(driver, wait)

    results = {key: [] for key in RESULT_KEYS}
    credentials = read_credentials(DATA_FILE)

    try:
        for row in credentials:
            username, password = row["username"], row["password"]
            print(f"\n--- Running TV flow for {username} ---")

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

            with step_timer(results, "Services"):
                tv_page.open_services()
            time.sleep(5)

            with step_timer(results, "TV Overview"):
                tv_page.open_tv_overview()
            time.sleep(5)
            tv_page.return_to_profile()

            with step_timer(results, "Logout"):
                profile_page.logout()
            time.sleep(5)

            driver.terminate_app(settings.APP_BUNDLE_ID)
            driver.activate_app(settings.APP_BUNDLE_ID)

        write_results_to_excel(results, REPORT_FILE)
        print("\nAll users processed.")
    finally:
        quit_driver(driver)


if __name__ == "__main__":
    run()
