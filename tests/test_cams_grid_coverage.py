import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

from src.processing.spatial.cams_aggregation import _assign_nearest_points_for_uncovered_regions


def test_assign_nearest_points_for_uncovered_regions_fills_missing_admin_units() -> None:
    boundaries = gpd.GeoDataFrame(
        {
            "country_code": ["CIV", "CIV"],
            "admin_level": ["ADM2", "ADM2"],
            "admin_code": ["CI001", "CI002"],
            "admin_name": ["A", "B"],
        },
        geometry=[
            Polygon([(0, 0), (1, 0), (1, 1), (0, 1)]),
            Polygon([(2, 2), (3, 2), (3, 3), (2, 3)]),
        ],
        crs="EPSG:4326",
    )
    mapping = pd.DataFrame(
        [
            {
                "latitude": 0.5,
                "longitude": 0.5,
                "country_code": "CIV",
                "admin_level": "ADM2",
                "admin_code": "CI001",
                "admin_name": "A",
            }
        ]
    )

    completed = _assign_nearest_points_for_uncovered_regions(
        boundaries,
        mapping,
        latitudes=[0.5, 2.5],
        longitudes=[0.5, 2.5],
    )
    assert set(completed["admin_code"]) == {"CI001", "CI002"}
