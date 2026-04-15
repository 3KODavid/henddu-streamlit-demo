"""Dataset validation helpers."""

from __future__ import annotations

import pandas as pd

from src.utils.errors import DataAccessError


def require_columns(frame: pd.DataFrame, required_columns: list[str]) -> None:
    missing = [column for column in required_columns if column not in frame.columns]
    if missing:
        raise DataAccessError(f"Missing required columns: {', '.join(missing)}")

