import pandas as pd

from src.services.map_service import MapService


def test_get_choropleth_data_filters_indicator_and_level() -> None:
    frame = pd.DataFrame(
        [
            {"admin_level": "ADM1", "indicator": "PM2.5", "value": 1},
            {"admin_level": "ADM2", "indicator": "PM2.5", "value": 2},
            {"admin_level": "ADM1", "indicator": "NO2", "value": 3},
        ]
    )
    service = MapService()
    result = service.get_choropleth_data(frame, "PM2.5", "ADM1")
    assert len(result) == 1

