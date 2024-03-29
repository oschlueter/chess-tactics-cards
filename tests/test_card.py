from pathlib import Path

import pytest

from chesscards.card import Deck


class TestCard:
    pass


class TestDeck:
    def test_save_deck__sample__stores_deck_correctly(self, tmp_path):
        # given
        csv_fn = str(Path(__file__).resolve().parent / "data/sample.csv")
        decks_path = tmp_path / "decks"
        deck_name = "test-deck"

        # when
        Deck.create_from_csv(deck_name, csv_fn, decks_dir=str(decks_path))

        # then
        assert (decks_path / deck_name / "cards/00008.json").exists()
        assert (decks_path / deck_name / "logs/").exists()
