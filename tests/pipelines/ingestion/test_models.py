from pipelines.ingestion.models import Dataset, DatasetFile


def test_dataset_should_have_files():
    dataset = Dataset(
        name="olist",
        description="Brazilian E-Commerce Dataset",
        files=(
            DatasetFile(
                name="customers.csv",
                url="http://example.com/customers.csv",
                description="Customer information",
            ),
        ),
    )

    assert dataset.name == "olist"
    assert len(dataset.files) == 1
