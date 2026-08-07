from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class DatasetFile:
    name: str
    url: str
    description: str
    size_bytes: int | None = None


@dataclass(frozen=True, slots=True)
class Dataset:
    name: str
    description: str
    files: tuple[DatasetFile, ...]
    checksum: str | None = None
    format: Literal["csv", "parquet"] = "csv"
