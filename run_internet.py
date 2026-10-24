"""Entry point: `python run_internet.py`

Thin wrapper — all the real logic lives in flows/internet_flow.py.
"""
from flows.internet_flow import run

if __name__ == "__main__":
    run()
