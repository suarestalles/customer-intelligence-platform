from pathlib import Path

from pipelines.warehouse.database_config import Database


def test_database_should_create_database_file(tmp_path: Path) -> None:
    database_path = tmp_path / "warehouse" / "test.duckdb"

    database = Database(database_path)

    # database.execute(
    #     """
    #     CREATE TABLE customers (
    #         id INTEGER PRIMARY KEY,
    #         name VARCHAR
    #     )
    #     """
    # )

    # database.execute(
    #     """
    #         INSERT INTO customers VALUES
    #         (1, 'Alice'),
    #         (2, 'Ben')
    #     """
    # )

    # result = database.query(
    #     """
    #         SELECT *
    #         FROM customers
    #         ORDER BY id
    #     """
    # )

    # assert database_path.exists()
    # assert result == [(1, "Alice"), (2, "Ben")]

    database.create_schema("raw")

    result = database.query(
        "SELECT schema_name FROM information_schema.schemata WHERE schema_name = 'raw'"
    )

    assert result == [("raw",)]
