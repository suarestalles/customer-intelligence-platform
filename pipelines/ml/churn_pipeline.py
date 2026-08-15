from pipelines.ml.customer_churn_dataset import CustomerChurnDataset
from pipelines.ml.customer_features import CustomerFeatures
from pipelines.warehouse.database_config import Database


class ChurnPipeline:
    def __init__(self, database: Database) -> None:
        self.database = database

    def build_dataset(self) -> None:
        CustomerFeatures(self.database).build()
        CustomerChurnDataset(self.database).build()
