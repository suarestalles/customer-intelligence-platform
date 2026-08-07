from pipelines.injestion.models import Dataset, DatasetFile

OLIST = Dataset(
    name="olist",
    description="Brazilian E-Commerce Public Dataset",
    url="",
    filename="",
    expected_files=(
        DatasetFile(name="olist_customer_dataset.csv", url="URL_HERE"),
        DatasetFile(name="olist_orders_dataset.csv", url="URL_HERE"),
    ),
)

DATASETS = {
    OLIST.name: OLIST,
}
