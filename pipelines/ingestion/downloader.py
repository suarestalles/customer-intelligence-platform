import logging
from pathlib import Path

import httpx2

from pipelines.ingestion.exceptions import DatasetDownloadError
from pipelines.ingestion.models import Dataset
from pipelines.ingestion.workspace import DatasetWorkspace

logger = logging.getLogger(__name__)


class DatasetDownloader:
    def __init__(self) -> None:
        self.client = httpx2.Client(timeout=60, follow_redirects=True)

    def download(
        self, dataset: Dataset, workspace: DatasetWorkspace, overwrite: bool = False
    ) -> None:
        logger.info(f"Starting dataset ingestion: {dataset.name}")
        workspace.create()
        step = 1
        for file in dataset.files:
            if not file.url.startswith(("http://", "https://")):
                raise DatasetDownloadError(f"Invalid URL for file: {file.name}")
            destination = workspace.root / file.name

            logger.info(f"-----[{step}/9]Downloading {dataset.name}")
            self._download_file(file.url, destination, overwrite)
            logger.info(f"-----Finished downloading {dataset.name}")
            step += 1
        logger.info(f"Dataset ingestion finished: {dataset.name}")

    def _download_file(self, url: str, destination: Path, overwrite: bool = False) -> None:
        if destination.exists() and not overwrite:
            logger.info(f"{destination.name} already exists. Skipping...")
            return

        logger.info(f"Downloading {destination.name}")

        try:
            with self.client.stream("GET", url) as response:
                response.raise_for_status()

                with destination.open("wb") as f:
                    for chunk in response.iter_bytes():
                        f.write(chunk)
        except httpx2.HTTPError as exc:
            raise DatasetDownloadError(f"Failed downloading {url}") from exc

        logger.info(f"Finished {destination.name}")
