from pathlib import Path

from pipelines.ingestion.workspace import DatasetWorkspace


def test_workspace_creates_raw_directory(tmp_path: Path):
    workspace = DatasetWorkspace("olist", tmp_path)

    workspace.create()

    assert workspace.raw.exists()
