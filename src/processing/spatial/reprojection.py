"""Spatial reprojection helpers."""

from __future__ import annotations

import geopandas as gpd


def ensure_wgs84(frame: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    if frame.crs is None:
        return frame.set_crs("EPSG:4326")
    if frame.crs.to_string() == "EPSG:4326":
        return frame
    return frame.to_crs("EPSG:4326")

