"""Prepare datasets for choropleth and animated maps."""

from __future__ import annotations

import pandas as pd


def build_map_dataset(frame: pd.DataFrame, admin_level: str, indicator: str) -> pd.DataFrame:
    return frame[(frame["admin_level"] == admin_level) & (frame["indicator"] == indicator)].copy()


def build_animation_dataset(frame: pd.DataFrame, admin_level: str, indicator: str) -> pd.DataFrame:
    return build_map_dataset(frame, admin_level, indicator)

