from pathlib import Path

from chesscards.extract import extract_tactics
from tests.conftest import read_file


def test_extract__sample__extracts_correct_tactics(database, tmp_path):
    # given
    extract_file = str(tmp_path / 'extract.csv')

    # when
    extract_tactics(database, 1000, 1300, 80, ['middlegame', 'endgame'], 5, extract_file)

    # then
    assert read_file(extract_file) == read_file(str(Path(__file__).resolve().parent / "data/extract.csv"))
