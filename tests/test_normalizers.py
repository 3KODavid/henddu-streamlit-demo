from src.data.schemas.normalizers import normalize_indicator_name


def test_normalize_indicator_name() -> None:
    assert normalize_indicator_name("pm2p5") == "PM2.5"

