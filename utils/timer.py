"""
Replaces the repeated

    start_time = time.time()
    ...
    end_time = time.time()
    results["Some Step"].append(round(end_time - start_time, 3))

boilerplate from the original scripts with a single context manager:

    with step_timer(results, "Login"):
        login_page.login(username, password)

The elapsed time (seconds, rounded to 3 decimals) is appended to
`results["Login"]` automatically when the `with` block exits — even if the
step prints extra logs in between, exactly like the original scripts did.
"""
import time
from contextlib import contextmanager


@contextmanager
def step_timer(results: dict, step_name: str):
    print(f"----------- {step_name} : Starts -----------")
    start_time = time.time()
    try:
        yield
    finally:
        elapsed = round(time.time() - start_time, 3)
        results.setdefault(step_name, []).append(elapsed)
        print(f"----------- {step_name} : Finished {elapsed} Seconds -----------")
