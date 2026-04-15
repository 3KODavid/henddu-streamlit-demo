"""Time-series service layer."""

from __future__ import annotations

import pandas as pd

from src.processing.prepare.timeseries import build_timeseries_dataset


class TimeSeriesService:
    """Provides filtered time-series datasets."""

    def get_timeseries(
        self,
        frame: pd.DataFrame,
        indicator: str,
        admin_level: str,
        admin_name: str | None = None,
    ) -> pd.DataFrame:
        return build_timeseries_dataset(frame, admin_level, indicator, admin_name)

