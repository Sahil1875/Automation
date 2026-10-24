"""
BasePage — shared helpers every page object inherits.

A page object should never call `driver.find_element(...)` or
`WebDriverWait(...)` directly; it should call these helpers instead. That
way, if we ever need to change *how* we wait (e.g. add retries, add
logging), we change it once, here.
"""
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver, wait: WebDriverWait):
        self.driver = driver
        self.wait = wait

    # ------------------------------------------------------------------
    # Waiting + interacting
    # ------------------------------------------------------------------
    def click(self, locator):
        """Wait for an element to be clickable, then click it."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def find(self, locator):
        """Wait for an element to be clickable and return it (without clicking)."""
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_visible(self, locator):
        """Wait until an element is visible, return it."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_present(self, locator):
        """Wait until an element is present in the DOM (may not be visible yet)."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_invisible(self, locator):
        """Wait until an element is no longer visible (e.g. a loading spinner)."""
        return self.wait.until(EC.invisibility_of_element_located(locator))

    def try_dismiss(self, locator, timeout: int = 10) -> bool:
        """
        Attempt to click a locator (e.g. a popup's dismiss button) within
        `timeout` seconds. Returns True if it was found and dismissed, False
        if it never appeared. Never raises.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            ).click()
            return True
        except TimeoutException:
            return False

    # ------------------------------------------------------------------
    # Gestures
    # ------------------------------------------------------------------
    def swipe_up(self, times: int = 1, pause: float = 1):
        """Swipe the screen up `times` times, pausing between each swipe."""
        for _ in range(times):
            self.driver.execute_script("mobile: swipe", {"direction": "up"})
            time.sleep(pause)

    def tap(self, x: int, y: int):
        """Tap raw screen coordinates. Prefer a locator-based click when possible —
        coordinate taps are brittle across screen sizes, but some legacy screens
        in this app don't expose accessible locators, so a couple of pages still
        use this."""
        self.driver.execute_script("mobile: tap", {"x": x, "y": y})

    def scroll_to_element_by_accessibility_id(self, acc_id: str, max_scrolls: int = 5):
        """Scroll down the screen until an element with the given accessibility id
        appears, then return it. Raises if it's never found."""
        for _ in range(max_scrolls):
            try:
                return self.driver.find_element("accessibility id", acc_id)
            except Exception:
                self.driver.execute_script("mobile: scroll", {"direction": "down"})
                time.sleep(1)
        raise TimeoutException(f"Element '{acc_id}' not found after {max_scrolls} scrolls.")

    # ------------------------------------------------------------------
    # App lifecycle
    # ------------------------------------------------------------------
    def restart_app(self, bundle_id: str):
        """Terminate then relaunch the app — used between users/iterations
        to guarantee a clean state."""
        self.driver.terminate_app(bundle_id)
        self.driver.activate_app(bundle_id)
