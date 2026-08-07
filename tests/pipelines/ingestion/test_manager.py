from pipelines.ingestion.manager import DatasetManager


def test_should_return_registered_dataset():
    manager = DatasetManager()

    dataset = manager.get("olist")

    assert dataset.name == "olist"
    assert len(dataset.files) > 0


def test_should_list_registered_datasets():
    manager = DatasetManager()

    datasets = manager.list()

    assert len(datasets) == 1
