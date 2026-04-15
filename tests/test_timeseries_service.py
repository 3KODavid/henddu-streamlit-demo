import pandas as pd

from src.services.timeseries_service import TimeSeriesService


def test_get_timeseries_filters_region() -> None:
    frame = pd.DataFrame(
        [
            {"admin_level": "ADM1", "indicator": "PM2.5", "admin_name": "A", "date": "2025-01-01"},
            {"admin_level": "ADM1", "indicator": "PM2.5", "admin_name": "B", "date": "2025-01-02"},
        ]
    )
    service = TimeSeriesService()
    result = service.get_timeseries(frame, "PM2.5", "ADM1", admin_name="A")
    assert len(result) == 1

