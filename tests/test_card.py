from datetime import datetime
from pathlib import Path

import freezegun
import pytest
from fsrs import FSRS, Rating

from chesscards.card import Deck


@freezegun.freeze_time("2024-01-01 12:00:00")
class TestCard:
    def read_file(self, fn: str):
        with open(fn, "r") as f:
            return f.read()

    @pytest.fixture
    def sample_deck(self, tmp_path):
        csv_fn = str(Path(__file__).resolve().parent / "data/sample.csv")
        decks_path = tmp_path / "decks"
        deck_name = "test-deck"

        deck = Deck.create_from_csv(deck_name, csv_fn, str(decks_path))

        yield deck

    def test_save_card__with_review_log__stores_card_and_review_log_correctly(self, sample_deck: Deck):
        # given
        f = FSRS()
        scheduling_cards = f.repeat(sample_deck.cards[0], datetime.utcnow())

        updated_card = scheduling_cards[Rating.Good].card
        review_log = scheduling_cards[Rating.Good].review_log

        # when
        sample_deck.save_card(updated_card, review_log)
        sample_deck.save_card(updated_card, review_log)

        # then
        review_log_path = Path(sample_deck.logs_path) / f"{updated_card.id}.jsonl"

        assert review_log_path.exists(), "review log does not exist"
        assert self.read_file(f"{sample_deck.cards_path}/{updated_card.id}.json") == self.read_file(
            str(Path(__file__).resolve().parent / "data/updated_card.json")
        )
        assert self.read_file(f"{sample_deck.logs_path}/{updated_card.id}.jsonl") == self.read_file(
            str(Path(__file__).resolve().parent / "data/review_log.jsonl")
        )


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

    # def test_load__sample__loads_deck_correctly(self, tmp_path):
