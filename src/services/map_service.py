"""Map-oriented service layer."""

from __future__ import annotations

import pandas as pd

from src.processing.prepare.maps import build_animation_dataset, build_map_dataset


class MapService:
    """Provides datasets for choropleth and animation views."""

    def get_choropleth_data(self, frame: pd.DataFrame, indicator: str, admin_level: str) -> pd.DataFrame:
        return build_map_dataset(frame, admin_level, indicator)

    def get_animation_data(self, frame: pd.DataFrame, indicator: str, admin_level: str) -> pd.DataFrame:
        return build_animation_dataset(frame, admin_level, indicator)

