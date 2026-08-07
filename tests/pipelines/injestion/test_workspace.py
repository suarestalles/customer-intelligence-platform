from pipelines.injestion.workspace import DatasetWorkspace


def test_workspace_creates_directories(tmp_path):
    workspace = DatasetWorkspace(dataset_name="olist", base_path=tmp_path)

    workspace.create()

    assert workspace.downloads.exists()
    assert workspace.extracted.exists()
