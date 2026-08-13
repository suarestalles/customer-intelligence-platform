from dataclasses import dataclass

from pipelines.quality.checks import (
    QualityCheckResult,
    analytics_quality_checks,
    raw_quality_checks,
)
from pipelines.warehouse.database_config import Database


@dataclass(frozen=True, slots=True)
class QualityReport:
    results: list[QualityCheckResult]

    @property
    def total_checks(self) -> int:
        return len(self.results)

    @property
    def passed_checks(self) -> int:
        return sum(result.passed for result in self.results)

    @property
    def failed_checks(self) -> int:
        return self.total_checks - self.passed_checks

    @property
    def passed(self) -> bool:
        return self.failed_checks == 0


class DataQualityRunner:
    def __init__(self, database: Database) -> None:
        self.database = database

    def run_raw_checks(self) -> QualityReport:
        results = raw_quality_checks(self.database)
        return QualityReport(results)

    def run_analytics_checks(self) -> QualityReport:
        results = analytics_quality_checks(self.database)
        return QualityReport(results)

    def run_all(self) -> QualityReport:
        results = [
            *raw_quality_checks(self.database),
            *analytics_quality_checks(self.database),
        ]

        return QualityReport(results)
