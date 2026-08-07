from pipelines.ingestion.registry import DATASETS


def test_olist_dataset_should_exist():
    dataset = DATASETS["olist"]

    assert dataset.name == "olist"
    assert len(dataset.files) > 0


def test_olist_should_have_customer_file():
    dataset = DATASETS["olist"]

    filenames = [file.name for file in dataset.files]

    assert "olist_customer_dataset.csv" in filenames
