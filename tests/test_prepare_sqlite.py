import sqlite3

import pytest


@pytest.mark.parametrize("query,count", [("SELECT * FROM tactics", 5), ("SELECT * FROM themes", 18)])
def test_prepare_sqlite__sample__creates_expected_sqlite(query, count, database):
    # given
    # when
    # fixture

    # then
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        # Example: Execute a simple SQL query
        cursor.execute(query)

        # Fetch all rows from the query result
        rows = cursor.fetchall()
        assert len(rows) == count


@pytest.mark.parametrize(
    "table,num_index",
    [
        ("tactics", 4),
        ("themes", 2),
    ],
)
def test_prepare_sqlite__sample__creates_expected_indices(database, table, num_index):
    with sqlite3.connect(database) as conn:
        cursor = conn.cursor()

        cursor.execute(
            f"""
            SELECT
               count(*)
            FROM
               sqlite_master
            WHERE type='index' AND tbl_name='{table}'
        """
        )

        index_count = cursor.fetchone()[0]

        # Assert that the index exists
        assert index_count == num_index, f"Table {table}  does not have {num_index} incides!"
