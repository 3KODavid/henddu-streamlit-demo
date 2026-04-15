"""Available UI filters."""

from __future__ import annotations

from src.config.constants import (
    ADMIN_LEVEL_OPTIONS,
    COUNTRY_OPTIONS,
    DATE_PRESET_OPTIONS,
    INDICATOR_OPTIONS,
    TIME_AGGREGATION_OPTIONS,
)


def get_filter_options() -> dict[str, list[str]]:
    return {
        "countries": COUNTRY_OPTIONS,
        "admin_levels": ADMIN_LEVEL_OPTIONS,
        "indicators": INDICATOR_OPTIONS,
        "date_presets": DATE_PRESET_OPTIONS,
        "time_aggregations": TIME_AGGREGATION_OPTIONS,
    }

