"""Aggregation helpers from CAMS gridded data to CIV administrative boundaries."""

from __future__ import annotations

import geopandas as gpd
import numpy as np
import pandas as pd
from shapely.geometry import Point

from src.config.constants import CAMS_INDICATOR_VARIABLES
from src.processing.spatial.boundaries import prepare_boundaries
from src.utils.errors import ProcessingError


def build_grid_points(latitudes, longitudes) -> gpd.GeoDataFrame:
    """Create a point grid from latitude/longitude coordinates."""
    records: list[dict[str, object]] = []
    for latitude in latitudes:
        for longitude in longitudes:
            records.append(
                {
                    "latitude": float(latitude),
                    "longitude": float(longitude),
                    "geometry": Point(float(longitude), float(latitude)),
                }
            )

    return gpd.GeoDataFrame(records, geometry="geometry", crs="EPSG:4326")


def map_grid_to_boundaries(
    boundaries: gpd.GeoDataFrame,
    latitudes,
    longitudes,
    admin_level: str,
) -> pd.DataFrame:
    """Assign each CAMS grid point to an administrative polygon."""
    prepared_boundaries = prepare_boundaries(boundaries, admin_level)
    if prepared_boundaries.empty:
        raise ProcessingError(f"No boundaries available for {admin_level}")

    grid_points = build_grid_points(latitudes, longitudes)
    joined = gpd.sjoin(
        grid_points,
        prepared_boundaries[["country_code", "admin_level", "admin_code", "admin_name", "geometry"]],
        how="inner",
        predicate="within",
    )

    if joined.empty:
        raise ProcessingError(f"No CAMS grid points intersected {admin_level} boundaries")

    mapping = joined[
        ["latitude", "longitude", "country_code", "admin_level", "admin_code", "admin_name"]
    ].drop_duplicates()
    return _assign_nearest_points_for_uncovered_regions(
        prepared_boundaries,
        mapping,
        latitudes,
        longitudes,
    )


def _assign_nearest_points_for_uncovered_regions(
    prepared_boundaries: gpd.GeoDataFrame,
    current_mapping: pd.DataFrame,
    latitudes,
    longitudes,
) -> pd.DataFrame:
    """Fallback for small polygons with no CAMS grid point inside them."""
    covered_codes = set(current_mapping["admin_code"].unique())
    uncovered = prepared_boundaries[~prepared_boundaries["admin_code"].isin(covered_codes)].copy()
    if uncovered.empty:
        return current_mapping

    grid_pairs = np.array([(float(lat), float(lon)) for lat in latitudes for lon in longitudes])
    fallback_rows: list[dict[str, object]] = []

    for _, row in uncovered.iterrows():
        representative = row.geometry.representative_point()
        rep_lat = float(representative.y)
        rep_lon = float(representative.x)
        distances = np.sqrt((grid_pairs[:, 0] - rep_lat) ** 2 + (grid_pairs[:, 1] - rep_lon) ** 2)
        nearest_index = int(np.argmin(distances))
        nearest_lat, nearest_lon = grid_pairs[nearest_index]
        fallback_rows.append(
            {
                "latitude": nearest_lat,
                "longitude": nearest_lon,
                "country_code": row["country_code"],
                "admin_level": row["admin_level"],
                "admin_code": row["admin_code"],
                "admin_name": row["admin_name"],
            }
        )

    fallback = pd.DataFrame(fallback_rows)
    combined = pd.concat([current_mapping, fallback], ignore_index=True)
    return combined.drop_duplicates(
        subset=["latitude", "longitude", "admin_level", "admin_code", "admin_name"]
    ).reset_index(drop=True)


def dataset_to_long_frame(
    dataset,
    indicator: str,
    start_time: str | None = None,
    end_time: str | None = None,
) -> pd.DataFrame:
    """Convert a single-indicator xarray dataset into a long dataframe."""
    if indicator not in CAMS_INDICATOR_VARIABLES:
        raise ProcessingError(f"Unsupported CAMS indicator: {indicator}")

    variable_name = CAMS_INDICATOR_VARIABLES[indicator]
    if variable_name not in dataset.data_vars:
        raise ProcessingError(f"Variable {variable_name} not found in dataset")

    scoped = dataset
    if start_time or end_time:
        scoped = dataset.sel(time=slice(start_time, end_time))

    frame = scoped[variable_name].to_dataframe(name="value").reset_index()
    frame["indicator"] = indicator
    frame["date"] = pd.to_datetime(frame["time"]).dt.date
    frame = frame.rename(columns={"time": "datetime"})
    return frame[["datetime", "date", "latitude", "longitude", "indicator", "value"]]


def aggregate_cams_to_admin(
    dataset,
    boundaries: gpd.GeoDataFrame,
    indicator: str,
    admin_level: str,
    start_time: str | None = None,
    end_time: str | None = None,
    source: str = "cams_reanalysis",
) -> pd.DataFrame:
    """Aggregate a CAMS indicator over CIV administrative boundaries."""
    metrics = dataset_to_long_frame(dataset, indicator, start_time=start_time, end_time=end_time)
    grid_mapping = map_grid_to_boundaries(
        boundaries=boundaries,
        latitudes=dataset.latitude.values,
        longitudes=dataset.longitude.values,
        admin_level=admin_level,
    )

    merged = metrics.merge(grid_mapping, on=["latitude", "longitude"], how="inner")
    if merged.empty:
        raise ProcessingError(f"No CAMS values could be matched to {admin_level}")

    aggregated = (
        merged.groupby(
            ["country_code", "admin_level", "admin_code", "admin_name", "indicator", "datetime", "date"],
            dropna=False,
        )["value"]
        .mean()
        .reset_index()
    )
    aggregated["source"] = source
    aggregated["unit"] = "kg m-3"
    return aggregated[
        [
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
    ]
