from unittest.mock import MagicMock

from pipelines.quality.runner import DataQualityRunner


def test_runner_initializes_with_database() -> None:
    database = MagicMock()

    runner = DataQualityRunner(database)

    assert runner.database is database


def test_run_raw_checks_returns_quality_report() -> None:
    database = MagicMock()

    runner = DataQualityRunner(database)

    report = runner.run_raw_checks()

    assert report is not None
    assert hasattr(report, "results")
    assert isinstance(report.results, list)


def test_run_analytics_checks_returns_quality_report() -> None:
    database = MagicMock()

    runner = DataQualityRunner(database)

    report = runner.run_analytics_checks()

    assert report is not None
    assert hasattr(report, "results")
    assert isinstance(report.results, list)


def test_run_all_returns_quality_report() -> None:
    database = MagicMock()

    runner = DataQualityRunner(database)

    report = runner.run_all()

    assert report is not None
    assert hasattr(report, "results")
    assert isinstance(report.results, list)


def test_run_all_combines_raw_and_analytics_checks() -> None:
    database = MagicMock()

    runner = DataQualityRunner(database)

    raw_report = runner.run_raw_checks()
    analytics_report = runner.run_analytics_checks()
    all_report = runner.run_all()

    expected_count = len(raw_report.results) + len(analytics_report.results)

    assert len(all_report.results) == expected_count
