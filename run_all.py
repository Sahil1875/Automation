"""
Master runner — runs a chosen set of journeys back-to-back, each in its own
subprocess (so its own fresh Appium session), just like the original
mbm_ios_01masterscript.py.

Edit the JOURNEYS list below to choose which run_*.py scripts to run, and in
what order. Comment a line out (prefix with #) to skip it.
"""
import subprocess
import sys
import time

# ================================================================
#                     SCRIPTS TO RUN IN ORDER
# ================================================================
JOURNEYS = [
    # "run_viewbill.py",
    # "run_mob_usage.py",
    # "run_internet.py",
    "run_hug.py",
    "run_crp.py",
    "run_tv.py",
]

# Small pause between journeys, to let the previous Appium session fully close.
GAP_BETWEEN_RUNS_SECONDS = 5


def main():
    print("=" * 60)
    print("         MASTER RUNNER - Bell MyBell iOS Journeys")
    print("=" * 60)

    failed = []

    for script in JOURNEYS:
        print(f"\n>>> Starting : {script}")
        print("-" * 60)

        start_time = time.time()
        result = subprocess.run([sys.executable, script], text=True)
        elapsed = round(time.time() - start_time, 2)

        if result.returncode == 0:
            print(f"\n>>> Finished : {script} in {elapsed} seconds [SUCCESS]")
        else:
            print(f"\n>>> Finished : {script} in {elapsed} seconds [FAILED]")
            failed.append(script)

        print("-" * 60)
        time.sleep(GAP_BETWEEN_RUNS_SECONDS)

    print("\n" + "=" * 60)
    print("                   FINAL SUMMARY")
    print("=" * 60)
    print(f"Total journeys run : {len(JOURNEYS)}")
    print(f"Passed             : {len(JOURNEYS) - len(failed)}")
    print(f"Failed             : {len(failed)}")

    if failed:
        print("\nFailed journeys:")
        for s in failed:
            print(f"  - {s}")
    else:
        print("\nAll journeys completed successfully.")

    print("=" * 60)


if __name__ == "__main__":
    main()
