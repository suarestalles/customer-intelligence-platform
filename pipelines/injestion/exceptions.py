class DatasetError(Exception):
    """Base exception."""


class DatasetDownloadError(Exception):
    """Download failed."""


class DatasetValidationError(Exception):
    """Validation failed."""


class DatasetNotFoundError(Exception):
    """Dataset is not registered."""
