import pandas as pd

from src.processing.spatial.aggregation import aggregate_to_admin_level


def test_aggregate_to_admin_level() -> None:
    frame = pd.DataFrame(
        [
            {
                "country_code": "CIV",
                "admin_level": "ADM1",
                "admin_code": "A",
                "admin_name": "Abidjan",
                "indicator": "PM2.5",
                "date": "2025-01-01",
                "value": 10.0,
            },
            {
                "country_code": "CIV",
                "admin_level": "ADM1",
                "admin_code": "A",
                "admin_name": "Abidjan",
                "indicator": "PM2.5",
                "date": "2025-01-01",
                "value": 20.0,
            },
        ]
    )

    result = aggregate_to_admin_level(frame, "ADM1")
    assert result.iloc[0]["value"] == 15.0

