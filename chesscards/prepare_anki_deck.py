from pathlib import Path

from card import Deck

if __name__ == '__main__':
    p = Path("anki_export")
    p.mkdir(parents=True, exist_ok=True)

    deck = Deck.create_from_csv(
        deck_name="test",
        csv_fn="extract.csv",
    )

    deck.anki_export(p)
