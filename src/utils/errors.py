"""Custom exceptions used across the Henddu MVP codebase."""


class HendduError(Exception):
    """Base application error."""


class ConfigurationError(HendduError):
    """Raised when required configuration is missing or invalid."""


class DataAccessError(HendduError):
    """Raised when a dataset cannot be read or validated."""


class ProcessingError(HendduError):
    """Raised when transformations or aggregations fail."""

