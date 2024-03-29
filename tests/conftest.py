import pytest
import random


def read_file(fn: str):
    with open(fn, "r") as f:
        return f.read()


@pytest.fixture(autouse=True)
def set_random_seed():
    random.seed(0)
