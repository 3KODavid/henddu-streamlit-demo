"""Environment-backed settings for the Henddu MVP demo."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from src.config.constants import (
    ADMIN_LEVEL_OPTIONS,
    COUNTRY_OPTIONS,
    INDICATOR_OPTIONS,
    TIME_AGGREGATION_OPTIONS,
)


load_dotenv()


@dataclass(frozen=True)
class Settings:
    aws_region: str
    aws_profile: str | None
    s3_bucket: str
    default_country: str
    default_admin_level: str
    default_indicator: str
    default_time_aggregation: str
    enable_population_exposure: bool
    log_level: str
    base_dir: Path
    cache_dir: Path
    processed_dir: Path


def _get_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_settings() -> Settings:
    base_dir = Path(__file__).resolve().parents[2]
    cache_dir = base_dir / "data" / "cache"
    processed_dir = base_dir / "data" / "processed"

    default_country = os.getenv("HENDDU_COUNTRY_CODE", COUNTRY_OPTIONS[0])
    default_admin_level = os.getenv("HENDDU_DEFAULT_ADMIN_LEVEL", ADMIN_LEVEL_OPTIONS[0])
    default_indicator = os.getenv("HENDDU_DEFAULT_INDICATOR", INDICATOR_OPTIONS[0])
    default_time_aggregation = os.getenv(
        "HENDDU_DEFAULT_TIME_AGGREGATION",
        TIME_AGGREGATION_OPTIONS[0],
    )

    if default_country not in COUNTRY_OPTIONS:
        raise ValueError(f"Unsupported default country: {default_country}")
    if default_admin_level not in ADMIN_LEVEL_OPTIONS:
        raise ValueError(f"Unsupported admin level: {default_admin_level}")
    if default_indicator not in INDICATOR_OPTIONS:
        raise ValueError(f"Unsupported indicator: {default_indicator}")
    if default_time_aggregation not in TIME_AGGREGATION_OPTIONS:
        raise ValueError(f"Unsupported time aggregation: {default_time_aggregation}")

    return Settings(
        aws_region=os.getenv("AWS_REGION", "eu-west-1"),
        aws_profile=os.getenv("AWS_PROFILE"),
        s3_bucket=os.getenv("HENDDU_S3_BUCKET", "henddu-reference-data"),
        default_country=default_country,
        default_admin_level=default_admin_level,
        default_indicator=default_indicator,
        default_time_aggregation=default_time_aggregation,
        enable_population_exposure=_get_bool("HENDDU_ENABLE_POPULATION_EXPOSURE", False),
        log_level=os.getenv("HENDDU_LOG_LEVEL", "INFO"),
        base_dir=base_dir,
        cache_dir=cache_dir,
        processed_dir=processed_dir,
    )
