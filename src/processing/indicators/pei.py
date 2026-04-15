"""Population Exposure Index scaffolding."""

from __future__ import annotations

import pandas as pd


def build_pei_frame() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "country_code",
            "admin_level",
            "admin_code",
            "admin_name",
            "indicator",
            "population_exposure_index",
            "population_exposed",
        ]
    )

