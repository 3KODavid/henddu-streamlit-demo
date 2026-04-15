"""Prepare datasets for time-series charts."""

from __future__ import annotations

import pandas as pd


def build_timeseries_dataset(
    frame: pd.DataFrame,
    admin_level: str,
    indicator: str,
    admin_name: str | None = None,
) -> pd.DataFrame:
    filtered = frame[(frame["admin_level"] == admin_level) & (frame["indicator"] == indicator)].copy()
    if admin_name:
        filtered = filtered[filtered["admin_name"] == admin_name]
    return filtered.sort_values("date")

