"""Entry point: `python run_crp.py`

Thin wrapper — all the real logic lives in flows/crp_flow.py.
"""
from flows.crp_flow import run

if __name__ == "__main__":
    run()
