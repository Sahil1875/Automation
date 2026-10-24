"""Entry point: `python run_viewbill.py`

Thin wrapper — all the real logic lives in flows/viewbill_flow.py.
"""
from flows.viewbill_flow import run

if __name__ == "__main__":
    run()
