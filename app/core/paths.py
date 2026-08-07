from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT_DIR / "data"

EXTERNAL_DATA_DIR = DATA_DIR / "external"
INTERMEDIATE_DATA_DIR = DATA_DIR / "intermediate"
WAREHOUSE_DIR = DATA_DIR / "warehouse"

PIPELINES_DIR = ROOT_DIR / "pipelines"

DOCS_DIR = ROOT_DIR / "docs"
