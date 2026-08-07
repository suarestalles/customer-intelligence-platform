from dataclasses import dataclass
from typing import Literal


@dataclass(frozen=True, slots=True)
class DatasetFile:
    name: str
    url: str


@dataclass(frozen=True, slots=True)
class Dataset:
    name: str
    description: str
    url: str
    filename: str
    expected_files: tuple[DatasetFile, ...]
    compressed: bool = True
    checksum: str | None = None
    format: Literal["zip", "csv", "parquet"] = "zip"
