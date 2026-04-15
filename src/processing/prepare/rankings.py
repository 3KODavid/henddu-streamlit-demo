"""Ranking preparation helpers."""

from __future__ import annotations

import pandas as pd

from src.processing.indicators.exposure import build_exposure_ranking


def build_top_exposed_regions(frame: pd.DataFrame, indicator: str, limit: int = 10) -> pd.DataFrame:
    ranking = build_exposure_ranking(frame, indicator)
    return ranking.head(limit).reset_index(drop=True)
