from src.config.settings import get_settings


def test_settings_load_default_bucket() -> None:
    settings = get_settings()
    assert settings.s3_bucket == "henddu-reference-data"

