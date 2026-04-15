"""KPI service layer."""

from __future__ import annotations

import pandas as pd

from src.processing.prepare.kpis import build_kpis


class KpiService:
    """Provides KPI summaries for overview screens."""

    def get_kpis(self, frame: pd.DataFrame, indicator: str) -> dict[str, object]:
        return build_kpis(frame, indicator)

