"""Normalization helpers for analytical datasets."""

from __future__ import annotations

import pandas as pd


def normalize_indicator_name(indicator: str) -> str:
    indicator_map = {
        "pm2p5": "PM2.5",
        "pm10": "PM10",
        "no2": "NO2",
        "o3": "O3",
        "temperature": "Temperature",
    }
    return indicator_map.get(indicator.lower(), indicator)


def ensure_datetime_column(frame: pd.DataFrame, column: str = "datetime") -> pd.DataFrame:
    normalized = frame.copy()
    if column in normalized.columns:
        normalized[column] = pd.to_datetime(normalized[column], errors="coerce")
    return normalized
