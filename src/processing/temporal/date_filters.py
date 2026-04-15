"""Date range filtering helpers."""

from __future__ import annotations

import pandas as pd


def filter_by_date_range(
    frame: pd.DataFrame,
    start_date: str | None,
    end_date: str | None,
    column: str = "date",
) -> pd.DataFrame:
    if frame.empty or column not in frame.columns:
        return frame.copy()

    filtered = frame.copy()
    filtered[column] = pd.to_datetime(filtered[column]).dt.date
    if start_date:
        filtered = filtered[filtered[column] >= pd.to_datetime(start_date).date()]
    if end_date:
        filtered = filtered[filtered[column] <= pd.to_datetime(end_date).date()]
    return filtered
