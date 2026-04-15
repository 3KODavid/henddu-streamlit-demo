"""Helpers for pollution indicator datasets."""

from __future__ import annotations

import pandas as pd


def build_pollution_frame() -> pd.DataFrame:
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

