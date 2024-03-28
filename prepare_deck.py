import csv
import random

from card import ChessCard, Deck


def read(fn: str):
    with open(fn) as f:
        reader = csv.DictReader(f)
        tactics = [row for row in reader]
        random.shuffle(tactics)

        return tactics


def sample():
    return read('sample.csv')


def extract():
    return read('extract.csv')


if __name__ == '__main__':
    data = extract()

    deck = Deck('selection_1600_1800', [
        ChessCard(tactic['PuzzleId'], tactic['FEN'], tactic['Moves'], tactic['Themes']) for tactic in data
    ])
    deck.save_deck()
