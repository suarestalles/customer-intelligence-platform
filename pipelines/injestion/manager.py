from pipelines.injestion.exceptions import DatasetNotFoundError
from pipelines.injestion.models import Dataset
from pipelines.injestion.registry import DATASETS
from pipelines.injestion.workspace import DatasetWorkspace


class DatasetManager:
    def get(self, dataset_name: str) -> Dataset:
        try:
            return DATASETS[dataset_name]
        except KeyError as exc:
            raise DatasetNotFoundError(f"Dataset '{dataset_name}' is not registered") from exc

    def list(self) -> list[Dataset]:
        return list(DATASETS.values())

    def workspace(self, dataset_name: str) -> DatasetWorkspace:
        self.get(dataset_name)

        workspace = DatasetWorkspace(dataset_name)
        workspace.create()

        return workspace
