from pathlib import Path

import duckdb


class Database:
    def __init__(self, database_path: Path) -> None:
        self.database_path = database_path

    def connect(self) -> duckdb.DuckDBPyConnection:
        self.database_path.parent.mkdir(parents=True, exist_ok=True)

        return duckdb.connect(str(self.database_path))

    def execute(self, query: str) -> None:
        with self.connect() as connection:
            connection.execute(query)

    def query(self, query: str) -> list[tuple]:
        with self.connect() as connection:
            result = connection.execute(query)

            return result.fetchall()

    def create_schema(self, schema_name: str) -> None:
        self.execute(f"CREATE SCHEMA IF NOT EXISTS {schema_name}")
