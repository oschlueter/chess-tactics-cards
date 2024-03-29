import sqlite3

import pytest


def test_prepare_sqlite__sample__creates_expected_sqlite(database):
    # given
    # when
    # fixture

    # then
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        # Example: Execute a simple SQL query
        cursor.execute("SELECT * FROM tactics")

        # Fetch all rows from the query result
        rows = cursor.fetchall()
        assert len(rows) == 18


@pytest.mark.parametrize("indexed_column", [
    "popularity",
    "rating",
    "themes"
])
def test_prepare_sqlite__sample__creates_expected_indices(database, indexed_column):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        # Define the table name and index name you want to check
        table_name = 'tactics'
        index_name = f'idx_{indexed_column}'

        # Query the sqlite_master table to check if the index exists
        cursor.execute(f"""
            SELECT
               *
            FROM
               sqlite_master
            WHERE type='index' AND tbl_name='{table_name}' AND name='{index_name}'
        """)

        # Check if the query returned any rows
        index_exists = cursor.fetchone() is not None

        # Assert that the index exists
        assert index_exists, f"Index {index_name} does not exist on table {table_name}"

