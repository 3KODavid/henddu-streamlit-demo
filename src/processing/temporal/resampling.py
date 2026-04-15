"""Temporal aggregation helpers."""

from __future__ import annotations

import pandas as pd


def resample_timeseries(frame: pd.DataFrame, frequency: str) -> pd.DataFrame:
    if frame.empty or "datetime" not in frame.columns:
        return frame.copy()

    normalized = frame.copy()
    normalized["datetime"] = pd.to_datetime(normalized["datetime"])
    normalized = normalized.set_index("datetime")
    result = (
        normalized.groupby(["country_code", "admin_level", "admin_code", "admin_name", "indicator"])
        .resample({"daily": "D", "weekly": "W", "monthly": "ME"}[frequency])["value"]
        .mean()
        .reset_index()
    )
    result["date"] = result["datetime"].dt.date
    return result

