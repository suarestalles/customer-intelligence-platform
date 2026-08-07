from pathlib import Path

import httpx2

from pipelines.injestion.models import Dataset
from pipelines.injestion.workspace import DatasetWorkspace


class DatasetDownloader:
    def __init__(self) -> None:
        self.client = httpx2.Client(timeout=60, follow_redirects=True)

    def download(self, dataset: Dataset, workspace: DatasetWorkspace) -> None:
        for file in dataset.expected_files:
            self._download_file(file.url, workspace.root / file.name)

    def _download_file(self, url: str, destination: Path) -> None:
        response = self.client.get(url)
        response.raise_for_status()
        destination.write_bytes(response.content)
