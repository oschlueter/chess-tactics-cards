from pathlib import Path

import pytest
import random

from chesscards.prepare_sqlite import prepare_sqlite


def read_file(fn: str):
    with open(fn, "r") as f:
        return f.read()


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(0)


@pytest.fixture
def database(tmp_path):
    sqlite_fn = str(tmp_path / "tmp.db")
    csv_fn = str(Path(__file__).resolve().parent / "data/sample.csv")

    prepare_sqlite(csv_fn, sqlite_fn)

    return sqlite_fn
