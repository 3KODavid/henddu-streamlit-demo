"""WorldPop reader stub for population exposure workflows."""

from __future__ import annotations

import pandas as pd

from src.config.constants import SOURCE_PATHS
from src.data.s3_client import S3Client


class WorldPopReader:
    """Loads population raster metadata for CIV."""

    def __init__(self, s3_client: S3Client | None = None) -> None:
        self.s3_client = s3_client or S3Client()

    def get_source_key(self) -> str:
        return SOURCE_PATHS["civ_worldpop_2020"]

    def load_metadata(self) -> pd.DataFrame:
        return pd.DataFrame(
            [
                {
                    "country_code": "CIV",
                    "year": 2020,
                    "s3_key": self.get_source_key(),
                    "status": "pending_raster_pipeline",
                }
            ]
        )

