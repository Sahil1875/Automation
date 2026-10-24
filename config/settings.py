"""
Central place for every environment / device value the framework needs.

Nothing here is business logic — it just reads from a `.env` file (via
python-dotenv). There are NO hardcoded fallback credentials: if a required
variable is missing from `.env`, this module raises a clear error at import
time instead of silently connecting with someone else's leftover values.

Freshers: if you need to point the framework at a different device or Appium
server, edit your `.env` file — you should never need to edit this file.
"""
import os
from dotenv import load_dotenv

# Load variables from a .env file in the project root, if present.
load_dotenv()

# Variables that MUST be supplied via .env — no safe default exists for
# these (credentials, server URLs, device identifiers are all
# environment/person-specific and often sensitive).
_REQUIRED_VARS = [
    "APPIUM_REMOTE_URL",
    "APPIUM_USERNAME",
    "APPIUM_PASSWORD",
    "PLATFORM_NAME",
    "PLATFORM_VERSION",
    "DEVICE_NAME",
    "DEVICE_UDID",
    "AUTOMATION_NAME",
    "APP_BUNDLE_ID",
]

_missing = [name for name in _REQUIRED_VARS if not os.environ.get(name)]
if _missing:
    raise RuntimeError(
        "Missing required environment variable(s): "
        + ", ".join(_missing)
        + ".\n\nCopy \".env.example\" (in the project root) to \".env\" and "
        "fill in real values before running the framework. Nothing in "
        "settings.py falls back to hardcoded credentials anymore — this is "
        "intentional, so real secrets can never silently ship inside source "
        "code."
    )

# ---------------------------------------------------------------------------
# Appium / device-lab grid
# ---------------------------------------------------------------------------
APPIUM_REMOTE_URL = os.environ["APPIUM_REMOTE_URL"]
APPIUM_USERNAME = os.environ["APPIUM_USERNAME"]
APPIUM_PASSWORD = os.environ["APPIUM_PASSWORD"]

# ---------------------------------------------------------------------------
# Device under test
# ---------------------------------------------------------------------------
PLATFORM_NAME = os.environ["PLATFORM_NAME"]
PLATFORM_VERSION = os.environ["PLATFORM_VERSION"]
DEVICE_NAME = os.environ["DEVICE_NAME"]
DEVICE_UDID = os.environ["DEVICE_UDID"]
AUTOMATION_NAME = os.environ["AUTOMATION_NAME"]
APP_BUNDLE_ID = os.environ["APP_BUNDLE_ID"]

# ---------------------------------------------------------------------------
# Timeouts — these DO have safe, non-sensitive defaults, so they're allowed
# to fall back rather than force every .env to define them.
# ---------------------------------------------------------------------------
IMPLICIT_WAIT_TIMEOUT = int(os.environ.get("IMPLICIT_WAIT_TIMEOUT", "30"))
NEW_COMMAND_TIMEOUT = int(os.environ.get("NEW_COMMAND_TIMEOUT", "0"))

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
