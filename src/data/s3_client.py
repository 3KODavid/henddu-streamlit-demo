"""Thin S3 client wrapper used by data readers."""

from __future__ import annotations

from io import BytesIO

import boto3
from botocore.config import Config

from src.config.settings import get_settings
from src.utils.errors import DataAccessError
from src.utils.logging import get_logger


logger = get_logger(__name__)


class S3Client:
    """Centralized S3 access with light error handling."""

    def __init__(self) -> None:
        settings = get_settings()
        session_kwargs = {}
        if settings.aws_profile:
            session_kwargs["profile_name"] = settings.aws_profile
        if settings.aws_access_key_id and settings.aws_secret_access_key:
            session_kwargs["aws_access_key_id"] = settings.aws_access_key_id
            session_kwargs["aws_secret_access_key"] = settings.aws_secret_access_key
        if settings.aws_session_token:
            session_kwargs["aws_session_token"] = settings.aws_session_token

        session = boto3.Session(**session_kwargs)
        self.bucket = settings.s3_bucket
        self.client = session.client(
            "s3",
            region_name=settings.aws_region,
            config=Config(retries={"max_attempts": 5, "mode": "standard"}),
        )

    def list_objects(self, prefix: str) -> list[str]:
        try:
            response = self.client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
        except Exception as exc:  # pragma: no cover
            raise DataAccessError(f"Unable to list s3://{self.bucket}/{prefix}") from exc

        contents = response.get("Contents", [])
        return [item["Key"] for item in contents]

    def get_bytes(self, key: str) -> BytesIO:
        try:
            response = self.client.get_object(Bucket=self.bucket, Key=key)
        except Exception as exc:  # pragma: no cover
            raise DataAccessError(f"Unable to fetch s3://{self.bucket}/{key}") from exc

        logger.info("Fetched s3://%s/%s", self.bucket, key)
        return BytesIO(response["Body"].read())
