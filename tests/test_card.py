from datetime import datetime
from pathlib import Path

import freezegun
import pytest
from fsrs import FSRS, Rating

from chesscards.card import Deck


# @freezegun.freeze_time()
@pytest.fixture
def sample_deck(tmp_path):
    csv_fn = str(Path(__file__).resolve().parent / "data/sample.csv")
    decks_path = tmp_path / "decks"
    deck_name = "test-deck"

    with freezegun.freeze_time("2024-01-01 12:00:00"):
        deck = Deck.create_from_csv(deck_name, csv_fn, str(decks_path))

    yield deck


@freezegun.freeze_time("2024-01-01 12:00:00")
class TestCard:
    def read_file(self, fn: str):
        with open(fn, "r") as f:
            return f.read()

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

    def test_load__deck_does_not_exist__raises_value_error(self):
        # given
        deck = Deck('foo')

        # then
        with pytest.raises(ValueError, match='does not exist'):
            # when
            deck.load()

    @pytest.mark.skip(reason="will implement this later")
    def test_due__scenario__result(self):
        pass

    @pytest.mark.skip(reason="will implement this later")
    def test_not_due__scenario__result(self):
        pass


class TestDeck:
    def test_save_deck__sample__stores_deck_correctly(self, sample_deck):
        # given
        # when
        # fixture

        # then
        assert (sample_deck.cards_path / '00008.json').exists()
        assert sample_deck.logs_path.exists()

    def test_load__sample__loads_deck_correctly(self, sample_deck, tmp_path):
        # given
        # fixture

        # when
        deck = Deck(sample_deck.name, parent_dir=str(tmp_path / "decks"))
        deck.load()

        # then
        # a proper check for equality would improve this test but this is GEFN
        assert len(deck.cards) == len(sample_deck.cards)
        assert deck.cards[0].id == sample_deck.cards[0].id
        assert deck.cards[0].due == sample_deck.cards[0].due
        assert deck.cards[0].fen == sample_deck.cards[0].fen
