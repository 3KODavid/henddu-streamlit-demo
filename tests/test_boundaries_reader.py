import geopandas as gpd
from shapely.geometry import Polygon

from src.data.readers.boundaries_reader import infer_admin_level, normalize_boundary_frame


def test_infer_admin_level_from_filename() -> None:
    frame = gpd.GeoDataFrame({"shapeName": ["A"]}, geometry=[Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])], crs="EPSG:4326")
    assert infer_admin_level(frame, "civ_adm1_boundaries") == "ADM1"


def test_normalize_boundary_frame_uses_detected_columns() -> None:
    frame = gpd.GeoDataFrame(
        {
            "ADM2_PCODE": ["CI001001"],
            "ADM2_FR": ["Abobo"],
        },
        geometry=[Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])],
        crs="EPSG:4326",
    )

    normalized = normalize_boundary_frame(frame, "ADM2", "civ_adm2")
    assert normalized.iloc[0]["admin_level"] == "ADM2"
    assert normalized.iloc[0]["admin_code"] == "CI001001"
    assert normalized.iloc[0]["admin_name"] == "Abobo"
