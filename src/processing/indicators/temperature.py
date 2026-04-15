"""Helpers for temperature datasets."""

from __future__ import annotations

import pandas as pd


def build_temperature_frame() -> pd.DataFrame:
    return pd.DataFrame(
        columns=[
            "country_code",
            "admin_level",
            "admin_code",
            "admin_name",
            "indicator",
            "datetime",
            "date",
            "value",
            "unit",
            "source",
        ]
    )

