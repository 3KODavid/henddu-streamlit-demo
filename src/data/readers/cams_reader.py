"""Reader helpers for CAMS reanalysis datasets."""

from __future__ import annotations

from pathlib import Path

import cfgrib
import pandas as pd

from src.config.constants import CAMS_INDICATOR_VARIABLES, SOURCE_PATHS
from src.config.settings import get_settings
from src.data.s3_client import S3Client


class CamsReader:
    """Loads and inspects CAMS pollution datasets from GRIB sources."""

    def __init__(self, s3_client: S3Client | None = None) -> None:
        self.s3_client = s3_client or S3Client()
        self.settings = get_settings()

    def get_source_key(self) -> str:
        return SOURCE_PATHS["cams_pollution"]

    def load_metadata(self) -> pd.DataFrame:
        return pd.DataFrame(
            [{"source": "cams_reanalysis", "s3_key": self.get_source_key(), "status": "ready_for_inspection"}]
        )

    def inspect_datasets(self) -> pd.DataFrame:
        """Inspect a multi-message CAMS GRIB file and summarize its dataset groups."""
        datasets = self._open_datasets()
        rows: list[dict[str, object]] = []
        for index, dataset in enumerate(datasets):
            rows.append(
                {
                    "dataset_index": index,
                    "variables": ",".join(sorted(dataset.data_vars)),
                    "dimensions": ",".join(f"{key}={value}" for key, value in dataset.sizes.items()),
                    "edition": dataset.attrs.get("GRIB_edition"),
                    "centre": dataset.attrs.get("GRIB_centre"),
                }
            )

        return pd.DataFrame(rows)

    def get_variable_name(self, indicator: str) -> str:
        if indicator not in CAMS_INDICATOR_VARIABLES:
            raise ValueError(f"Unsupported CAMS indicator: {indicator}")
        return CAMS_INDICATOR_VARIABLES[indicator]

    def get_dataset_index_for_indicator(self, indicator: str) -> int:
        variable_name = self.get_variable_name(indicator)
        for index, dataset in enumerate(self._open_datasets()):
            if variable_name in dataset.data_vars:
                return index
        raise ValueError(f"Unable to find a CAMS dataset group containing variable {variable_name}")

    def load_indicator_dataset(self, indicator: str):
        dataset_index = self.get_dataset_index_for_indicator(indicator)
        return self._open_datasets()[dataset_index]

    def _open_datasets(self):
        local_path = self._ensure_local_copy()
        return cfgrib.open_datasets(str(local_path))

    def _ensure_local_copy(self) -> Path:
        cache_dir = self.settings.cache_dir
        cache_dir.mkdir(parents=True, exist_ok=True)
        local_path = cache_dir / "cams_surface_pollutants_hourly_2020-01-01_2025-08-31.grib"
        if local_path.exists() and local_path.stat().st_size > 0:
            return local_path

        payload = self.s3_client.get_bytes(self.get_source_key())
        local_path.write_bytes(payload.read())
        return local_path
