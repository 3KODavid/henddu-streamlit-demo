"""Exposure and ranking service layer."""

from __future__ import annotations

import pandas as pd

from src.processing.indicators.pei import build_pei_frame
from src.processing.prepare.rankings import build_top_exposed_regions


class ExposureService:
    """Provides exposure-oriented outputs for the app."""

    def get_top_exposed_regions(self, frame: pd.DataFrame, indicator: str, limit: int = 10) -> pd.DataFrame:
        return build_top_exposed_regions(frame, indicator, limit=limit)

    def get_population_exposure(self, _frame: pd.DataFrame, _indicator: str) -> pd.DataFrame:
        return build_pei_frame()

