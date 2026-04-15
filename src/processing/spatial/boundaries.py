"""Boundary shaping helpers for ADM1 and ADM2 outputs."""

from __future__ import annotations

import geopandas as gpd

from src.processing.spatial.reprojection import ensure_wgs84


def prepare_boundaries(frame: gpd.GeoDataFrame, admin_level: str) -> gpd.GeoDataFrame:
    prepared = ensure_wgs84(frame)
    if "admin_level" in prepared.columns:
        prepared = prepared[prepared["admin_level"] == admin_level].copy()
    return prepared

