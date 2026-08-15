from pathlib import Path

from pipelines.analytics.customer_cohorts import CustomerCohorts
from pipelines.analytics.customer_features import CustomerFeatures
from pipelines.analytics.customer_metrics import CustomerMetrics
from pipelines.analytics.customer_rfm import CustomerRFM
from pipelines.analytics.order_metrics import OrderMetrics
from pipelines.warehouse.database_config import Database

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = PROJECT_ROOT / "data" / "warehouse" / "customer_intelligence.duckdb"


def main() -> None:
    database = Database(DATABASE_PATH)

    OrderMetrics(database).build()
    CustomerMetrics(database).build()
    CustomerRFM(database).build()
    CustomerCohorts(database).build()
    CustomerFeatures(database).build()

    print("Analytics models built successfully.")


if __name__ == "__main__":
    main()
