from pathlib import Path

from pipelines.warehouse.database import Database


class RawLoader:
    def __init__(self, database: Database, raw_directory: Path) -> None:
        self.database = database
        self.raw_directory = raw_directory

    def load_file(self, file_path: Path) -> None:
        table_name = self._table_name(file_path)

        query = f"""
            CREATE OR REPLACE TABLE raw.{table_name} AS
            SELECT *
            FROM read_csv_auto('{file_path.as_posix()}')
        """

        self.database.execute(query)

    def load_all(self) -> None:
        self.database.create_schema("raw")

        for file_path in sorted(self.raw_directory.glob("*.csv")):
            self.load_file(file_path)

    @staticmethod
    def _table_name(file_path: Path) -> str:
        name = file_path.stem

        if name.startswith("olist_"):
            name = name.removeprefix("olist_")

        if name.endswith("_dataset"):
            name = name.removesuffix("_dataset")

        return name
