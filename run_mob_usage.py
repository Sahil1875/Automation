"""Entry point: `python run_mob_usage.py`

Thin wrapper — all the real logic lives in flows/mob_usage_flow.py.
"""
from flows.mob_usage_flow import run

if __name__ == "__main__":
    run()
