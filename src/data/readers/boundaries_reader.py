"""Boundary reader for CIV ADM1 and ADM2 administrative layers."""

from __future__ import annotations

from pathlib import Path
import tempfile
import zipfile

import geopandas as gpd
import pandas as pd

from src.config.constants import SOURCE_PATHS
from src.data.s3_client import S3Client
from src.processing.spatial.reprojection import ensure_wgs84
from src.utils.errors import DataAccessError


ADMIN_LEVELS = ("ADM1", "ADM2")


def _find_candidate_column(columns: list[str], candidates: list[str]) -> str | None:
    normalized = {column.lower(): column for column in columns}

    for candidate in candidates:
        if candidate.lower() in normalized:
            return normalized[candidate.lower()]

    for candidate in candidates:
        for lowercase, original in normalized.items():
            if candidate.lower() in lowercase:
                return original

    return None


def infer_admin_level(frame: gpd.GeoDataFrame, source_name: str) -> str | None:
    source_lower = source_name.lower()
    if "adm1" in source_lower:
        return "ADM1"
    if "adm2" in source_lower:
        return "ADM2"

    columns = list(frame.columns)
    if _find_candidate_column(columns, ["ADM2_PCODE", "ADM2_EN", "ADM2_FR", "ADM2_NAME"]):
        return "ADM2"
    if _find_candidate_column(columns, ["ADM1_PCODE", "ADM1_EN", "ADM1_FR", "ADM1_NAME"]):
        return "ADM1"
    return None


def should_use_shapefile(source_name: str) -> bool:
    source_lower = source_name.lower()
    if source_lower.endswith("_em"):
        return False
    return source_lower in {"civ_admin1", "civ_admin2"}


def normalize_boundary_frame(
    frame: gpd.GeoDataFrame,
    admin_level: str,
    source_name: str,
    country_code: str = "CIV",
) -> gpd.GeoDataFrame:
    columns = list(frame.columns)
    code_candidates = {
        "ADM1": ["ADM1_PCODE", "ADM1_CODE", "ADM1_ID", "admin1Pcod", "shapeID"],
        "ADM2": ["ADM2_PCODE", "ADM2_CODE", "ADM2_ID", "admin2Pcod", "shapeID"],
    }
    name_candidates = {
        "ADM1": ["ADM1_EN", "ADM1_FR", "ADM1_NAME", "admin1Name", "shapeName"],
        "ADM2": ["ADM2_EN", "ADM2_FR", "ADM2_NAME", "admin2Name", "shapeName"],
    }

    code_column = _find_candidate_column(columns, code_candidates[admin_level])
    name_column = _find_candidate_column(columns, name_candidates[admin_level])

    if name_column is None:
        raise DataAccessError(
            f"Unable to infer a name column for {admin_level} from {source_name}. "
            f"Columns seen: {', '.join(columns)}"
        )

    normalized = frame.copy()
    normalized = ensure_wgs84(normalized)
    normalized["country_code"] = country_code
    normalized["admin_level"] = admin_level
    normalized["admin_name"] = normalized[name_column].astype(str).str.strip()
    normalized["admin_code"] = (
        normalized[code_column].astype(str).str.strip()
        if code_column is not None
        else normalized["admin_name"].str.replace(r"\s+", "_", regex=True).str.upper()
    )
    normalized["source_name"] = source_name

    keep_columns = [
        "country_code",
        "admin_level",
        "admin_code",
        "admin_name",
        "source_name",
        "geometry",
    ]
    return normalized[keep_columns].dropna(subset=["geometry"]).reset_index(drop=True)


class BoundariesReader:
    """Loads boundary metadata and full geometries for CIV."""

    def __init__(self, s3_client: S3Client | None = None) -> None:
        self.s3_client = s3_client or S3Client()

    def get_source_key(self) -> str:
        return SOURCE_PATHS["civ_boundaries"]

    def load_metadata(self) -> pd.DataFrame:
        return pd.DataFrame(
            [{"country_code": "CIV", "levels": "ADM1,ADM2", "s3_key": self.get_source_key()}]
        )

    def empty_geodataframe(self) -> gpd.GeoDataFrame:
        return gpd.GeoDataFrame(
            {
                "country_code": [],
                "admin_level": [],
                "admin_code": [],
                "admin_name": [],
                "source_name": [],
            },
            geometry=[],
            crs="EPSG:4326",
        )

    def inspect_archive(self) -> pd.DataFrame:
        archive_bytes = self.s3_client.get_bytes(self.get_source_key())
        with zipfile.ZipFile(archive_bytes) as archive:
            rows = []
            for info in archive.infolist():
                rows.append(
                    {
                        "filename": info.filename,
                        "size_bytes": info.file_size,
                    }
                )
        return pd.DataFrame(rows)

    def load_boundaries(self, admin_level: str | None = None) -> gpd.GeoDataFrame:
        target_levels = [admin_level] if admin_level else list(ADMIN_LEVELS)
        archive_bytes = self.s3_client.get_bytes(self.get_source_key())

        with tempfile.TemporaryDirectory(prefix="henddu_boundaries_") as temp_dir:
            with zipfile.ZipFile(archive_bytes) as archive:
                archive.extractall(temp_dir)

            frames: list[gpd.GeoDataFrame] = []
            for shp_path in Path(temp_dir).rglob("*.shp"):
                source_name = shp_path.stem
                if not should_use_shapefile(source_name):
                    continue
                raw = gpd.read_file(shp_path)
                inferred_level = infer_admin_level(raw, source_name)
                if inferred_level is None or inferred_level not in target_levels:
                    continue
                frames.append(normalize_boundary_frame(raw, inferred_level, source_name))

        if not frames:
            return self.empty_geodataframe()

        combined = pd.concat(frames, ignore_index=True)
        combined = combined.drop_duplicates(subset=["admin_level", "admin_code", "admin_name"]).reset_index(drop=True)
        return gpd.GeoDataFrame(combined, geometry="geometry", crs="EPSG:4326")
