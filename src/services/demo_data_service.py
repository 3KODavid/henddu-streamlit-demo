"""High-level data pipeline for the CIV Streamlit MVP."""

from __future__ import annotations

import pandas as pd

from src.config.constants import CAMS_POLLUTANT_UNITS
from src.data.readers.boundaries_reader import BoundariesReader
from src.data.readers.cams_reader import CamsReader
from src.processing.spatial.cams_aggregation import aggregate_cams_to_admin
from src.processing.temporal.date_filters import filter_by_date_range
from src.processing.temporal.resampling import resample_timeseries


class DemoDataService:
    """Loads and prepares real datasets used by the Streamlit demo."""

    def __init__(
        self,
        boundaries_reader: BoundariesReader | None = None,
        cams_reader: CamsReader | None = None,
    ) -> None:
        self.boundaries_reader = boundaries_reader or BoundariesReader()
        self.cams_reader = cams_reader or CamsReader()

    def load_boundaries(self):
        return self.boundaries_reader.load_boundaries()

    def load_indicator_timeseries(
        self,
        indicator: str,
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        boundaries = self.load_boundaries()
        dataset = self.cams_reader.load_indicator_dataset(indicator)

        adm1 = aggregate_cams_to_admin(
            dataset,
            boundaries,
            indicator,
            "ADM1",
            start_time=start_date,
            end_time=end_date,
        )
        adm2 = aggregate_cams_to_admin(
            dataset,
            boundaries,
            indicator,
            "ADM2",
            start_time=start_date,
            end_time=end_date,
        )

        combined = pd.concat([adm1, adm2], ignore_index=True)
        combined = self._convert_units(combined, indicator)
        return filter_by_date_range(combined, start_date, end_date)

    def build_daily_series(
        self,
        indicator: str,
        start_date: str,
        end_date: str,
    ) -> pd.DataFrame:
        hourly = self.load_indicator_timeseries(indicator, start_date, end_date)
        return resample_timeseries(hourly, "daily")

    def _convert_units(self, frame: pd.DataFrame, indicator: str) -> pd.DataFrame:
        converted = frame.copy()
        converted["value"] = converted["value"] * 1_000_000_000
        converted["unit"] = CAMS_POLLUTANT_UNITS.get(indicator, converted["unit"])
        return converted
