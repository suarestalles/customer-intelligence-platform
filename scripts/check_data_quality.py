from pathlib import Path

from pipelines.quality.runner import DataQualityRunner
from pipelines.warehouse.database_config import Database

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATABASE_PATH = PROJECT_ROOT / "data" / "warehouse" / "customer_intelligence.duckdb"


def main() -> int:
    if not DATABASE_PATH.exists():
        print(f"Database not found: {DATABASE_PATH}")
        print("Run the ingestion and analytics build steps before running data quality checks.")
        return 1

    database = Database(DATABASE_PATH)
    runner = DataQualityRunner(database)

    report = runner.run_all()

    print()
    print("=" * 72)
    print("CUSTOMER INTELLIGENCE PLATFORM - DATA QUALITY")
    print("=" * 72)
    print()

    for result in report.results:
        status = "PASS" if result.passed else "FAIL"

        print(f"[{status}] {result.name}")
        print(f"       {result.message}")

    print()
    print("-" * 72)
    print(
        f"Checks: {report.total_checks} | "
        f"Passed: {report.passed_checks} | "
        f"Failed: {report.failed_checks}"
    )
    print("-" * 72)

    if report.passed:
        print("DATA QUALITY STATUS: PASSED")
        return 0

    print("DATA QUALITY STATUS: FAILED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
