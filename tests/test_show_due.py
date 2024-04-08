from pathlib import Path

from chesscards.card import Deck
from chesscards.show_due import show


def test_show_due__sample__does_not_raise_error(tmp_path):
    # given
    deck = Deck.create_from_csv(
        deck_name="foo",
        csv_fn=str(Path(__file__).resolve().parent / "data/extract.csv"),
        decks_dir=str(tmp_path),
    )

    # when
    show(deck.due_until_end_of_day(), "due")

    # then
    assert True  # no exception was raised
