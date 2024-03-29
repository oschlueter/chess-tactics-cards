from pathlib import Path

import pytest

from chesscards.extract import extract_tactics
from chesscards.prepare_sqlite import prepare_sqlite
from tests.conftest import read_file


@pytest.fixture
def database(tmp_path):
    sqlite_fn = str(tmp_path / "tmp.db")
    csv_fn = str(Path(__file__).resolve().parent / "data/sample.csv")

    prepare_sqlite(csv_fn, sqlite_fn)

    return sqlite_fn


def test_extract__sample__extracts_correct_tactics(database, tmp_path):
    # given
    extract_file = str(tmp_path / 'extract.csv')

    # when
    extract_tactics(database, 1000, 1300, 80, ['middlegame', 'endgame'], 5, extract_file)

    # then
    assert read_file(extract_file) == read_file(str(Path(__file__).resolve().parent / "data/extract.csv"))
