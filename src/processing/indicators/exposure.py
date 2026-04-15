"""Exposure scoring helpers for the MVP."""

from __future__ import annotations

import pandas as pd

from src.config.constants import DEFAULT_THRESHOLDS


def build_exposure_ranking(frame: pd.DataFrame, indicator: str) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(
            columns=["admin_level", "admin_code", "admin_name", "mean_value", "days_above_threshold"]
        )

    threshold = DEFAULT_THRESHOLDS[indicator]
    scoped = frame[frame["indicator"] == indicator].copy()
    grouped = scoped.groupby(["admin_level", "admin_code", "admin_name"], dropna=False)
    ranking = grouped["value"].agg(["mean", "max"]).reset_index()
    ranking["days_above_threshold"] = grouped.apply(lambda group: (group["value"] > threshold).sum()).values
    ranking = ranking.rename(columns={"mean": "mean_value", "max": "max_value"})
    return ranking.sort_values(["mean_value", "days_above_threshold"], ascending=False)

