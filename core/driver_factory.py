"""
Builds the Appium `webdriver.Remote` session and its `WebDriverWait`.

Every run_*.py entry point calls `create_driver()` once at the start and
`driver.quit()` at the end. Keeping this in one place means capability
changes (new device, new Appium server) only need to happen here.
"""
from appium import webdriver
from appium.options.ios import XCUITestOptions
from selenium.webdriver.support.ui import WebDriverWait

from config import settings


def build_ios_options() -> XCUITestOptions:
    """Assemble the XCUITest capabilities from config/settings.py."""
    options = XCUITestOptions()

    options.set_capability("dl:userName", settings.APPIUM_USERNAME)
    options.set_capability("dl:password", settings.APPIUM_PASSWORD)
    options.platform_name = settings.PLATFORM_NAME
    options.platform_version = settings.PLATFORM_VERSION
    options.device_name = settings.DEVICE_NAME
    options.udid = settings.DEVICE_UDID
    options.automation_name = settings.AUTOMATION_NAME
    options.bundle_id = settings.APP_BUNDLE_ID
    options.new_command_timeout = settings.NEW_COMMAND_TIMEOUT
    options.set_capability("appium:noReset", True)

    return options


def create_driver(wait_timeout: int = None):
    """
    Starts a new Appium session against settings.APPIUM_REMOTE_URL and
    returns (driver, wait) ready to use.

    wait_timeout: override the default WebDriverWait timeout (seconds) for
    flows that need a longer wait — e.g. the ViewBill flow's PDF generation
    step used 60s in the original script instead of the usual 30s.
    """
    options = build_ios_options()

    print("Connecting to Appium...")
    driver = webdriver.Remote(settings.APPIUM_REMOTE_URL, options=options)
    wait = WebDriverWait(driver, wait_timeout or settings.IMPLICIT_WAIT_TIMEOUT)

    print("Session started:", driver.session_id)
    return driver, wait


def quit_driver(driver):
    """Safely ends the Appium session."""
    if driver is not None:
        driver.quit()
