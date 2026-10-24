"""Reads username/password rows out of a data CSV."""
import csv
from typing import List, Dict


def read_credentials(csv_path: str) -> List[Dict[str, str]]:
    """
    Reads a CSV with `username,password` columns and returns a list of dicts,
    e.g. [{"username": "524206502", "password": "Bell1234"}, ...]
    """
    with open(csv_path, newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        return list(reader)
