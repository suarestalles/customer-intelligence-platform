from pathlib import Path

from app.core.paths import EXTERNAL_DATA_DIR


class DatasetWorkspace:
    def __init__(self, dataset_name: str, base_path: Path = EXTERNAL_DATA_DIR) -> None:
        self.dataset_name = dataset_name
        self.root = base_path / dataset_name

        self.downloads = self.root / "downloads"
        self.extracted = self.root / "extracted"
        self.metadata = self.root / "metadata.json"
        self.raw = self.root / "raw"

    def create(self) -> None:
        self.downloads.mkdir(parents=True, exist_ok=True)
        self.extracted.mkdir(parents=True, exist_ok=True)
        self.raw.mkdir(parents=True, exist_ok=True)
