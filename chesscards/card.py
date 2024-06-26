import csv
import itertools
import json
import random
from datetime import datetime, UTC
from pathlib import Path

import cairosvg
import chess
import chess.svg
from fsrs import Card, State
from fsrs.models import ReviewLog


class ChessCard(Card):
    id: str
    fen: str
    moves: str
    themes: str
    source: str

    def __init__(self, id: str, fen: str, moves: str, themes: str, source: str = "lichess"):
        super().__init__()

        self.id = id
        self.fen = fen
        self.moves = moves
        self.themes = themes
        self.source = source

    @staticmethod
    def from_dict(
        id: str,
        fen: str,
        moves: str,
        themes: str,
        due: str,
        stability: float,
        difficulty: float,
        elapsed_days: int,
        scheduled_days: int,
        reps: int,
        lapses: int,
        state: State,
        last_review: datetime = None,
        source: str = "lichess",
    ):

        if not source or source == "lichess":
            card = LiChessCard(id, fen, moves, themes)
        elif source == "book":
            card = BookChessCard(id, fen, moves, themes, source)
        else:
            raise ValueError(f"Cannot create ChessCard with source type '{source}'!")

        card.due = datetime.strptime(due, "%Y-%m-%d %H:%M:%S.%f%z")
        card.stability = stability
        card.difficulty = difficulty
        card.elapsed_days = elapsed_days
        card.scheduled_days = scheduled_days
        card.reps = reps
        card.lapses = lapses
        card.state = State(state)

        if last_review:
            card.last_review = datetime.strptime(last_review, "%Y-%m-%d %H:%M:%S.%f%z")

        return card

    def solution_san(self):
        board = self.board()
        moves_uci = self._moves()
        moves = [chess.Move.from_uci(uci) for uci in moves_uci]
        translation_table = str.maketrans("QNBR", "DSLT")

        try:
            return board.variation_san(moves).translate(translation_table)
        except chess.IllegalMoveError as e:
            # include card ID in error message so I can quickly find and fix the erroneous move
            raise ValueError(f"invalid move in card {self.id}: {e}") from e

    def _moves(self):
        return self.moves.split(" ")

    def exercise_svg(self):
        board = self.board()

        return chess.svg.board(flipped=not board.turn, board=board)

    def solution_svg(self):
        board = self.board()
        for move in self._moves():
            board.push(chess.Move.from_uci(move))

        return chess.svg.board(flipped=board.turn, board=board)

    def board(self):
        return chess.Board(self.fen)


class LiChessCard(ChessCard):
    def _moves(self):
        return super()._moves()[1:]

    def board(self):
        board = super().board()
        move = chess.Move.from_uci(self.moves.split(" ")[0])
        board.push(move)

        return board

    def exercise_svg(self):
        board = self.board()
        lastmove = chess.Move.from_uci(self.moves.split(" ")[0])

        return chess.svg.board(flipped=not board.turn, board=board, lastmove=lastmove)


class BookChessCard(ChessCard):
    pass


class Deck:
    name: str
    cards: list[ChessCard]

    def __init__(self, name: str, cards=None, parent_dir: str = "decks"):
        if cards is None:
            cards = []

        self.name = name
        self.cards = cards

        self.cards_path = Path(f"{parent_dir}/{self.name}/cards/")
        self.logs_path = Path(f"{parent_dir}/{self.name}/logs/")

    def save_deck(self):
        self.cards_path.mkdir(parents=True, exist_ok=True)
        self.logs_path.mkdir(parents=True, exist_ok=True)

        for card in self.cards:
            self.save_card(card)

    def save_card(self, card: ChessCard, log: ReviewLog = None):
        with open(str(self.cards_path / f"{card.id}.json"), "w") as f:
            f.write(json.dumps(card.__dict__, default=str, indent=4))

        if log:
            with open(str(self.logs_path / f"{card.id}.jsonl"), "a") as f:
                f.write(json.dumps(log.__dict__, default=str))
                f.write("\n")

    def load(self):
        if not self.cards_path.exists():
            raise ValueError(f"deck {self.name} does not exist!")

        for x in self.cards_path.iterdir():
            if x.is_file() and x.suffix == ".json":
                with x.open() as f:
                    data = json.load(f)
                    self.cards.append(ChessCard.from_dict(**data))

        self.cards.sort(key=lambda card: card.due)

    def due_until_end_of_day(self):
        return [card for card in self.cards if card.due.date() <= datetime.now(UTC).date()]

    def due_after_end_of_day(self):
        return [card for card in self.cards if card.due.date() > datetime.now(UTC).date()]

    def due(self):
        return [card for card in self.cards if card.due < datetime.now(UTC)]

    @staticmethod
    def shuffle(cards: [ChessCard]):
        # Sort due_cards by due date
        cards.sort(key=lambda card: card.due.date())

        result = []
        # Group cards by due date and shuffle each group
        for cards in (
            random.sample(cards, len(cards))
            for cards in (list(group) for date, group in itertools.groupby(cards, key=lambda card: card.due.date()))
        ):
            result.extend(cards)

        return result

    def not_due(self):
        return [card for card in self.cards if card.due > datetime.now(UTC)]

    @staticmethod
    def create_from_csv(deck_name: str, csv_fn: str, decks_dir: str = "decks", source="lichess"):
        with open(csv_fn) as f:
            reader = csv.DictReader(f)
            tactics = [row for row in reader]

            if source == "lichess":
                card_type = LiChessCard
            else:
                card_type = ChessCard

            deck = Deck(
                deck_name,
                [
                    card_type(tactic["PuzzleId"], tactic["FEN"], tactic["Moves"], tactic["Themes"], source=source)
                    for tactic in tactics
                ],
                decks_dir,
            )

            return deck

    def anki_export(self, export_path="anki"):
        anki_path = Path(export_path)
        anki_path.mkdir(parents=True, exist_ok=True)

        with open(f"{export_path}/deck.txt", "w") as f:

            f.writelines([
                "#separator:tab\n",
                "#html:true\n",
                "#tags column:3\n"
            ])

            for card in self.shuffle(self.cards):
                exercise_png = f"{card.id}_e.png"
                solution_png = f"{card.id}_s.png"

                self.save_png(card.exercise_svg(), f"{export_path}/{exercise_png}")
                self.save_png(card.solution_svg(), f"{export_path}/{solution_png}")

                am_zug = "Weiß" if card.board().turn else "Schwarz"
                am_zug = f"{am_zug} am Zug"

                f.write(f'"<img src=""{exercise_png}""><br>{am_zug}"\t"<img src=""{solution_png}""><br>{card.solution_san()}"\t{card.themes}\n')

    @staticmethod
    def save_png(svg: str, file_name: str):
        png = cairosvg.svg2png(svg)

        with open(file_name, 'wb') as f:
            f.write(png)


class MyReviewLog(ReviewLog):
    duration: int

    def __init__(
        self, rating: int, scheduled_days: int, elapsed_days: int, review: datetime, state: int, duration: int
    ):
        super().__init__(rating, scheduled_days, elapsed_days, review, state)

        self.duration = duration

    @staticmethod
    def from_log(log: ReviewLog, duration: int):
        return MyReviewLog(log.rating, log.scheduled_days, log.elapsed_days, log.review, log.state, duration)
