"""KPI preparation helpers."""

from __future__ import annotations

import pandas as pd

from src.config.constants import DEFAULT_THRESHOLDS


def build_kpis(frame: pd.DataFrame, indicator: str) -> dict[str, object]:
    if frame.empty:
        return {
            "mean_value": None,
            "max_value": None,
            "top_region": None,
            "regions_above_threshold": 0,
            "latest_date": None,
        }

    scoped = frame[frame["indicator"] == indicator].copy()
    if scoped.empty:
        return {
            "mean_value": None,
            "max_value": None,
            "top_region": None,
            "regions_above_threshold": 0,
            "latest_date": None,
        }

    grouped = scoped.groupby("admin_name", dropna=False)["value"].mean().sort_values(ascending=False)
    return {
        "mean_value": float(scoped["value"].mean()),
        "max_value": float(scoped["value"].max()),
        "top_region": grouped.index[0] if not grouped.empty else None,
        "regions_above_threshold": int(
            scoped.groupby("admin_name")["value"].mean().gt(DEFAULT_THRESHOLDS[indicator]).sum()
        ),
        "latest_date": scoped["date"].max(),
    }

