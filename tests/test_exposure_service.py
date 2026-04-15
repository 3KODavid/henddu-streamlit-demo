import pandas as pd

from src.services.exposure_service import ExposureService


def test_get_top_exposed_regions_returns_rows() -> None:
    frame = pd.DataFrame(
        [
            {"admin_level": "ADM1", "admin_code": "A", "admin_name": "A", "indicator": "PM2.5", "value": 50},
            {"admin_level": "ADM1", "admin_code": "B", "admin_name": "B", "indicator": "PM2.5", "value": 10},
        ]
    )
    service = ExposureService()
    result = service.get_top_exposed_regions(frame, "PM2.5")
    assert not result.empty
