"""Writes a `results` dict (step name -> list of per-user timings) to Excel,
one column per user iteration plus an Average row — same layout the
original scripts produced."""
import os
import pandas as pd

from config import settings


def write_results_to_excel(results: dict, output_filename: str) -> str:
    """
    results: {"Login": [1.2, 1.4, ...], "Service Landing": [...], ...}
    output_filename: e.g. "output_crp.xlsx"

    Returns the full path the report was written to.
    """
    os.makedirs(settings.REPORTS_DIR, exist_ok=True)
    output_path = os.path.join(settings.REPORTS_DIR, output_filename)

    df = pd.DataFrame(results)
    df = df.T
    df.columns = [f"Iteration {i + 1}" for i in range(len(df.columns))]
    # Per-step average across all iterations (users), as a new column.
    # NOTE: the original scripts wrote this as `df.loc["Average"] = df.mean(axis=1)`,
    # which adds a *row* but assigns values computed *per row* — pandas can't align
    # those labels, so the "Average" row came out as all NaN in every original
    # report. This is the corrected version: `df.mean(axis=1)` already gives one
    # average per step (row), so it belongs in a new *column*.
    df["Average"] = df.mean(axis=1)

    df.to_excel(output_path, index=True)
    print(f"\nReport written to: {output_path}")
    return output_path
