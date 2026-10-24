# Bell MyBell iOS — Appium Performance Automation Framework

This framework drives the **Bell MyBell Mobile (iOS)** app through Appium to measure
how long each screen/transaction takes to load, for six user journeys:

| Journey       | What it measures                                   | Data file              | Report              |
|---------------|------------------------------------------------------|-------------------------|----------------------|
| CRP           | Change Rate Plan flow                                | `data/Data_CRP.csv`      | `reports/output_crp.xlsx` |
| HUG           | Hardware Upgrade (buy a new phone) flow              | `data/Data_HUG.csv`      | `reports/output_hug.xlsx` |
| Internet      | View/Change internet package flow                    | `data/Data_Internet.csv` | `reports/output_internet.xlsx` |
| Mobile Usage  | Voice / Text / Data usage screens                     | `data/Data_MobUsage.csv` | `reports/output_mobusage.xlsx` |
| TV            | TV services overview                                  | `data/Data_TV.csv`       | `reports/output_tv.xlsx` |
| ViewBill      | View bill, download PDF, history, comparison          | `data/Data_Viewbill.csv` | `reports/output_viewbill.xlsx` |

For every user row in the CSV, the script logs in, walks through every screen of the
journey, times how long each step took to load, logs out, and finally writes an
Excel report with one column per user (iteration) and an **Average** row at the bottom
— exactly like the original scripts, just organized properly.

---

## 1. Why this structure? (read this if you're new to the project)

The original scripts each had ~300 lines of Appium code copy-pasted into one file per
journey, mixing together: driver setup, login steps, screen navigation, timers, and
Excel export. That's hard to maintain — if a locator on the Login screen changes, you'd
have to fix it in *six different files*.

This framework follows the **Page Object Model (POM)**, the industry-standard pattern
for UI automation:

- **One class per app screen (or per closely-related group of screens)**, called a
  "Page Object". It only knows two things: *where the elements are* (locators) and
  *what a user can do on that screen* (methods like `login()`, `logout()`).
- **Flow scripts** (in `flows/`) don't know about locators at all — they just call
  page-object methods in order, e.g. `login_page.login(user, pwd)` then
  `crp_page.open_service_landing()`. This is what you read to understand *what a test
  does*.
- **Utilities** (`utils/`) hold small generic helpers used everywhere: timing a step,
  reading a CSV, writing the Excel report, dismissing popups.
- **Config** (`config/`) holds environment values (device, Appium server, credentials)
  so nothing is hardcoded inside test logic.

If a locator changes tomorrow, you fix it in exactly **one place** — the relevant page
object — and every flow that uses it is instantly fixed too.

---

## 2. Folder structure

```
bell_mbm_ios_framework/
├── README.md                 <- you are here
├── requirements.txt          <- Python dependencies
├── .env.example               <- copy to .env and fill in your own values
├── pytest.ini
│
├── config/
│   └── settings.py            <- Appium server URL, device caps, app bundle id (env-driven)
│
├── core/
│   ├── driver_factory.py      <- creates / quits the Appium driver session
│   └── base_page.py           <- BasePage: click(), wait_visible(), swipe_up(), tap(), etc.
│                                  Every page object inherits from this.
│
├── pages/                      <- ONE FILE PER SCREEN-GROUP ("Page Objects")
│   ├── login_page.py           <- Login screen (shared by all 6 journeys)
│   ├── profile_page.py         <- Profile menu + Logout (shared)
│   ├── crp_page.py             <- Every screen in the Change Rate Plan journey
│   ├── hug_page.py             <- Every screen in the Hardware Upgrade journey
│   ├── internet_page.py        <- Every screen in the Internet journey
│   ├── mob_usage_page.py       <- Every screen in the Mobile Usage journey
│   ├── tv_page.py              <- Every screen in the TV journey
│   └── viewbill_page.py        <- Every screen in the ViewBill journey
│
├── utils/
│   ├── popup_handler.py        <- dismiss marketing / Face ID / push-notification popups
│   ├── timer.py                <- `with step_timer(results, "Login"): ...` — records elapsed time
│   ├── csv_reader.py           <- reads username/password rows from a CSV
│   └── report_writer.py        <- writes the `results` dict to a formatted Excel file
│
├── flows/                      <- ONE FILE PER JOURNEY — reads like a test case, no locators
│   ├── crp_flow.py
│   ├── hug_flow.py
│   ├── internet_flow.py
│   ├── mob_usage_flow.py
│   ├── tv_flow.py
│   └── viewbill_flow.py
│
├── data/                       <- input CSVs (username, password per row)
│   ├── Data_CRP.csv
│   ├── Data_HUG.csv
│   ├── Data_Internet.csv
│   ├── Data_MobUsage.csv
│   ├── Data_TV.csv
│   └── Data_Viewbill.csv
│
├── reports/                     <- Excel reports land here after every run (gitignored)
│
├── run_crp.py                   <- entry point: `python run_crp.py`
├── run_hug.py
├── run_internet.py
├── run_mob_usage.py
├── run_tv.py
├── run_viewbill.py
└── run_all.py                   <- runs a chosen set of journeys back-to-back, like the
                                     original "master script", each in its own process
```

**Rule of thumb for freshers:** if you're changing *what a locator looks like* → edit a
file in `pages/`. If you're changing *the order of steps or which screens are visited*
→ edit a file in `flows/`. You should almost never need to touch `core/` or `utils/`.

---

## 3. Setup

```bash
# 1. Create and activate a virtual environment (recommended)
python3.10 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure your environment
cp .env.example .env
# then edit .env and fill in:
#   APPIUM_REMOTE_URL, APPIUM_USERNAME, APPIUM_PASSWORD,
#   DEVICE_NAME, PLATFORM_VERSION, DEVICE_UDID, APP_BUNDLE_ID
```

`.env` is listed in `.gitignore` — never commit real credentials to source control.
`config/settings.py` reads from `.env` (via `python-dotenv`) and falls back to the
original hardcoded values only if a variable is missing, so the framework still runs
out of the box for anyone with access to the original lab, but production setups
should always use `.env`.

---

## 4. Running a journey

```bash
python run_crp.py         # Change Rate Plan
python run_hug.py         # Hardware Upgrade
python run_internet.py    # Internet
python run_mob_usage.py   # Mobile Usage
python run_tv.py          # TV
python run_viewbill.py    # View Bill
```

Each one:
1. Starts a fresh Appium session against the device configured in `.env`.
2. Reads every row of its `data/Data_*.csv`.
3. Runs the full user journey for each row, timing every step.
4. Writes `reports/output_<journey>.xlsx` with per-user timings + an Average row.
5. Quits the driver session.

### Running several journeys back to back

```bash
python run_all.py
```

Edit the `JOURNEYS` list at the top of `run_all.py` to choose which ones to include
and in what order (mirrors the old `mbm_ios_01masterscript.py`). Each journey still
runs in its **own subprocess** with its own Appium session, so one journey crashing
doesn't take down the others — you get a pass/fail summary at the end.

---

## 5. Adding a new journey (e.g. "Add-a-Line")

1. Add `data/Data_AddALine.csv` with `username,password` columns.
2. Create `pages/add_a_line_page.py`, subclassing `BasePage`, with one method per screen
   transition (look at `pages/crp_page.py` for the pattern).
3. Create `flows/add_a_line_flow.py`, copying the shape of `flows/crp_flow.py`: loop
   over CSV rows, call page-object methods wrapped in `step_timer`, write the report.
4. Create `run_add_a_line.py` (copy `run_crp.py` and change the import).
5. Optionally add it to the `JOURNEYS` list in `run_all.py`.

You never need to touch `core/` or existing page objects to add a new journey.

---

## 6. Bug fixed during the refactor

The original scripts computed the "Average" summary with:

```python
df.loc["Average"] = df.mean(axis=1)
```

`df.mean(axis=1)` correctly computes one average **per step** (row), but assigning it
via `df.loc["Average"] = ...` adds it as a new **row**, and pandas can't align a
Series indexed by step names against columns named "Iteration 1", "Iteration 2", etc.
The result was an "Average" row filled entirely with `NaN` in every original `.xlsx`
report (you can verify this in the `output_*.xlsx` files that shipped with the
original scripts). `utils/report_writer.py` fixes this by adding the result as a new
**column** instead (`df["Average"] = df.mean(axis=1)`), which is what the per-step
average actually needs.

---

## 7. Notes carried over from the original scripts

- Some locators in the original HUG script were marked `# TODO: add locator` — these
  were kept as-is (with the same `# TODO` comments) in `pages/hug_page.py` since we
  don't have access to the live app to verify better locators. Search for `TODO` in
  that file.
- Hardcoded `time.sleep()` calls were kept where the original relied on them (mostly
  for animations/screen settle time) since replacing them all with explicit waits
  would require access to the live app to verify. New explicit waits should be
  preferred going forward — see `BasePage.wait_visible()`.
- Session/device capabilities (username, password, UDID, bundle id) now come from
  `config/settings.py`, sourced from environment variables — nothing is hardcoded in
  test logic anymore.
