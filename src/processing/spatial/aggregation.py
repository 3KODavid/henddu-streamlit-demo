"""Spatial aggregation stubs for regional indicators."""

from __future__ import annotations

import pandas as pd


def aggregate_to_admin_level(
    frame: pd.DataFrame,
    admin_level: str,
    value_column: str = "value",
) -> pd.DataFrame:
    if frame.empty:
        return frame.copy()

    group_columns = ["country_code", "admin_level", "admin_code", "admin_name", "indicator", "date"]
    aggregated = (
        frame[frame["admin_level"] == admin_level]
        .groupby(group_columns, dropna=False)[value_column]
        .mean()
        .reset_index()
    )
    return aggregated

