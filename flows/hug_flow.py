"""
Hardware Upgrade (HUG) flow.

Reads Data_HUG.csv, runs the full HUG journey for every user row, times each
step, writes reports/output_hug.xlsx.
"""
import os
import time

from config import settings
from core.driver_factory import create_driver, quit_driver
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from pages.hug_page import HUGPage
from utils.csv_reader import read_credentials
from utils.timer import step_timer
from utils.report_writer import write_results_to_excel
from utils.popup_handler import dismiss_post_login_popups

DATA_FILE = os.path.join(settings.DATA_DIR, "Data_HUG.csv")
REPORT_FILE = "output_hug.xlsx"

RESULT_KEYS = [
    "Login",
    "Service Landing",
    "Mobility Overview",
    "Shop Devices",
    "Device Details",
    "Select Plan Page",
    "Select Plan",
    "Keep It Option",
    "Add-On Page",
    "Continue to Care",
    "Select SPC plan",
    "ReviewAndSubmit Page",
    "Confirmation Page",
    "Logout",
]


def run():
    driver, wait = create_driver()

    login_page = LoginPage(driver, wait)
    profile_page = ProfilePage(driver, wait)
    hug_page = HUGPage(driver, wait)

    results = {key: [] for key in RESULT_KEYS}
    credentials = read_credentials(DATA_FILE)

    try:
        for row in credentials:
            username, password = row["username"], row["password"]
            print(f"\n--- Running HUG flow for {username} ---")

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

            with step_timer(results, "Service Landing"):
                hug_page.open_service_landing()
            time.sleep(5)

            with step_timer(results, "Mobility Overview"):
                hug_page.open_mobility_overview()
            time.sleep(5)

            with step_timer(results, "Shop Devices"):
                hug_page.open_shop_devices()
            time.sleep(5)

            with step_timer(results, "Device Details"):
                hug_page.open_device_details()
            time.sleep(5)

            with step_timer(results, "Select Plan Page"):
                hug_page.open_select_plan_page()
            time.sleep(5)

            with step_timer(results, "Select Plan"):
                hug_page.select_plan()
            time.sleep(5)

            with step_timer(results, "Keep It Option"):
                hug_page.choose_keep_it_option()
            time.sleep(5)

            with step_timer(results, "Add-On Page"):
                hug_page.continue_to_addons()
            time.sleep(5)

            with step_timer(results, "Continue to Care"):
                hug_page.continue_to_care()
            time.sleep(5)

            with step_timer(results, "Select SPC plan"):
                hug_page.select_spc_plan()
            time.sleep(5)

            with step_timer(results, "ReviewAndSubmit Page"):
                hug_page.continue_to_review()
            time.sleep(5)

            with step_timer(results, "Confirmation Page"):
                hug_page.confirm_order()
            time.sleep(2)
            hug_page.return_to_profile()
            time.sleep(5)

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
