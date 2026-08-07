from pipelines.injestion.downloader import DatasetDownloader
from pipelines.injestion.manager import DatasetManager


def main() -> None:
    manager = DatasetManager()

    dataset = manager.get("olist")

    workspace = manager.workspace(dataset.name)

    downloader = DatasetDownloader()

    downloader.download(dataset, workspace)


if __name__ == "__main__":
    main()
