import pandas as pd
import xarray as xr
import geopandas as gpd
from shapely.geometry import Polygon

from src.processing.spatial.cams_aggregation import aggregate_cams_to_admin


def test_aggregate_cams_to_admin_returns_expected_columns() -> None:
    dataset = xr.Dataset(
        {
            "pm2p5": (("time", "latitude", "longitude"), [[[1.0]]]),
        },
        coords={
            "time": pd.to_datetime(["2025-01-01T00:00:00"]),
            "latitude": [5.0],
            "longitude": [-4.0],
        },
    )

    boundaries = gpd.GeoDataFrame(
        {
            "country_code": ["CIV"],
            "admin_level": ["ADM1"],
            "admin_code": ["CI01"],
            "admin_name": ["Abidjan"],
        },
        geometry=[Polygon([(-5.0, 4.0), (-3.0, 4.0), (-3.0, 6.0), (-5.0, 6.0)])],
        crs="EPSG:4326",
    )

    result = aggregate_cams_to_admin(dataset, boundaries, "PM2.5", "ADM1")
    assert list(result.columns) == [
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
    assert result.iloc[0]["value"] == 1.0
