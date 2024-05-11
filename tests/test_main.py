from pathlib import Path
from unittest.mock import patch

import pytest
from fsrs import Rating

from chesscards.card import Deck
from chesscards.main import train, rating_by_seconds


@pytest.mark.parametrize(
    "time_spent,expected",
    [(5, Rating.Easy), (35, Rating.Good), (65, Rating.Hard)],
)
def test_rating_by_seconds__various_inputs__returns_correct_rating(time_spent, expected):
    # given
    # fixture

    # when
    actual = rating_by_seconds(time_spent)

    # then
    assert actual == expected


# Custom input function for testing
def mock_input(prompt):
    # Define the sequence of inputs you want to simulate
    inputs = iter(["e4", "n"])
    result = next(inputs)

    print(f"{prompt} {result}")
    return result


@pytest.mark.parametrize(
    "user_input",
    [
        ["e4", "n", "n"],
        ["Te5+ Kf1 Txe6", "y"],
    ],
)
def test_train__sample__does_not_raise_error(tmp_path, user_input):
    # given
    deck = Deck.create_from_csv(
        deck_name="foo",
        csv_fn=str(Path(__file__).resolve().parent / "data/extract_single.csv"),
        decks_dir=str(tmp_path),
    )
    deck.save_deck()

    with patch("builtins.input", side_effect=user_input):
        # when
        train(deck)

    # then
    assert True  # no exception was raised
