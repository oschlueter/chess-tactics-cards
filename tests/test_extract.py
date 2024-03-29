from pathlib import Path

from chesscards.extract import extract_tactics
from tests.conftest import read_file_lines


def test_extract__sample__extracts_correct_tactics(database, tmp_path):
    # given
    extract_file = str(tmp_path / "extract.csv")

    # when
    extract_tactics(database, 1000, 1300, 80, ["middlegame", "endgame"], 5, extract_file)

    # then
    # convert to set to ignore order in CSV file
    assert set(read_file_lines(extract_file)) == set(
        read_file_lines(str(Path(__file__).resolve().parent / "data/extract.csv"))
    )
