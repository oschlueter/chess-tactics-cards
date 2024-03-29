import sqlite3
from pathlib import Path

from chesscards.prepare_sqlite import prepare_sqlite


def test_prepare_sqlite__sample__creates_expected_sqlite(tmp_path):
    # given
    sqlite_fn = str(tmp_path / "tmp.db")
    csv_fn = str(Path(__file__).resolve().parent / "data/sample.csv")

    # when
    prepare_sqlite(csv_fn, sqlite_fn)

    # then
    with sqlite3.connect(sqlite_fn) as conn:
        cursor = conn.cursor()

        # Example: Execute a simple SQL query
        cursor.execute("SELECT * FROM tactics")

        # Fetch all rows from the query result
        rows = cursor.fetchall()
        assert len(rows) == 4
