"""Join helpers between analytical tables and boundaries."""

from __future__ import annotations

import geopandas as gpd
import pandas as pd


def join_metrics_to_boundaries(metrics: pd.DataFrame, boundaries: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    return boundaries.merge(
        metrics,
        on=["country_code", "admin_level", "admin_code", "admin_name"],
        how="left",
    )

