"""Reader stubs for ERA5 datasets."""

from __future__ import annotations

import pandas as pd

from src.config.constants import SOURCE_PATHS
from src.data.s3_client import S3Client


class Era5Reader:
    """Loads temperature and other weather variables from ERA5 sources."""

    def __init__(self, s3_client: S3Client | None = None) -> None:
        self.s3_client = s3_client or S3Client()

    def get_source_prefix(self) -> str:
        return SOURCE_PATHS["era5_root"]

    def load_metadata(self) -> pd.DataFrame:
        return pd.DataFrame(
            [{"source": "era5", "s3_prefix": self.get_source_prefix(), "status": "pending_parser"}]
        )

