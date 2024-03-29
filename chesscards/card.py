import json
from datetime import datetime
from pathlib import Path

from fsrs import Card, State


class ChessCard(Card):
    id: str
    fen: str
    moves: str
    themes: str

    def __init__(self, id: str, fen: str, moves: str, themes: str):
        super().__init__()

        self.id = id
        self.fen = fen
        self.moves = moves
        self.themes = themes

    @staticmethod
    def from_dict(id: str, fen: str, moves: str, themes: str, due: str, stability: float, difficulty: float,
                  elapsed_days: int, scheduled_days: int, reps: int, lapses: int, state: State, last_review: datetime = None):

        card = ChessCard(id, fen, moves, themes)
        card.due = datetime.strptime(due, '%Y-%m-%d %H:%M:%S.%f')
        card.stability = stability
        card.difficulty = difficulty
        card.elapsed_days = elapsed_days
        card.scheduled_days = scheduled_days
        card.reps = reps
        card.lapses = lapses
        card.state = State(state)

        if last_review:
            card.last_review = datetime.strptime(last_review, '%Y-%m-%d %H:%M:%S.%f')

        return card


class Deck:
    name: str
    cards: list[ChessCard]

    def __init__(self, name: str, cards=None):
        if cards is None:
            cards = []

        self.name = name
        self.cards = cards

        self.deck_path = Path(f'decks/{self.name}')

    def save_deck(self):
        self.deck_path.mkdir(exist_ok=True)

        for card in self.cards:
            self.save_card(card)

    def save_card(self, card: ChessCard):
        with open(str(self.deck_path / f'{card.id}.json'), 'w') as f:
            f.write(json.dumps(card.__dict__, default=str, indent=4))

    def _mkdir(self):
        self.deck_path.mkdir(parents=True, exist_ok=True)

    def exists(self):
        return self.deck_path.exists()

    def load(self):
        if not self.deck_path.exists():
            raise ValueError(f"deck {self.name} does not exist!")

        for x in self.deck_path.iterdir():
            if x.is_file() and x.suffix == '.json':
                with x.open() as f:
                    data = json.load(f)
                    self.cards.append(ChessCard.from_dict(**data))

        self.cards.sort(key=lambda card: card.due)

    def due(self):
        return [card for card in self.cards if card.due < datetime.utcnow()]

    def not_due(self):
        return [card for card in self.cards if card.due > datetime.utcnow()]

