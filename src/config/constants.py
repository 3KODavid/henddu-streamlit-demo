"""Shared constants for the Henddu MVP demo."""

COUNTRY_OPTIONS = ["CIV"]
ADMIN_LEVEL_OPTIONS = ["ADM1", "ADM2"]
INDICATOR_OPTIONS = ["PM2.5", "PM10", "NO2", "O3", "Temperature"]
DEMO_INDICATOR_OPTIONS = ["PM2.5", "PM10", "NO2", "O3"]
TIME_AGGREGATION_OPTIONS = ["daily", "weekly", "monthly"]
DATE_PRESET_OPTIONS = [
    "Last 7 days",
    "Last 30 days",
    "Last 3 months",
    "Last 6 months",
    "Last 12 months",
    "Custom",
]

DEFAULT_THRESHOLDS = {
    "PM2.5": 35.0,
    "PM10": 50.0,
    "NO2": 100.0,
    "O3": 100.0,
    "Temperature": 35.0,
}

SOURCE_PATHS = {
    "cams_pollution": "climate-data/raw/cams_reanalysis/cams_surface_pollutants_hourly_2020-01-01_2025-08-31.grib",
    "cams_aod": "climate-data/raw/cams_reanalysis/cams_aod_hourly_2020-01-01_2025-08-31.grib",
    "era5_root": "climate-data/raw/era5/",
    "civ_boundaries": "vulnerability-data/CIV/hdx-cod-ab/2018/civ_admin_boundaries.shp.zip",
    "civ_worldpop_2020": "vulnerability-data/CIV/worldpop-population-counts/2020/civ_pop_2020_CN_1km_R2025A_UA_v1.tif",
}

CAMS_INDICATOR_VARIABLES = {
    "PM2.5": "pm2p5",
    "PM10": "pm10",
    "NO2": "no2",
    "O3": "go3",
    "SO2": "so2",
    "CO": "co",
}

CAMS_POLLUTANT_UNITS = {
    "PM2.5": "ug/m3",
    "PM10": "ug/m3",
    "NO2": "ug/m3",
    "O3": "ug/m3",
    "SO2": "ug/m3",
    "CO": "ug/m3",
}

CAMS_DATA_START_DATE = "2020-01-01"
CAMS_DATA_END_DATE = "2025-08-31"
