import csv
import random
import re
from datetime import datetime, timedelta
from io import BytesIO

import cairosvg
import chess.svg
import matplotlib.pyplot as plt
from fsrs import FSRS, Rating
from PIL import Image

from chesscards.card import Deck


def display(board: chess.Board, flip=False, lastmove: chess.Move = None):
    # display 'not board.turn' when showing the exercise
    # display 'board.turn' when showing the solution
    turn = board.turn if flip else not board.turn
    svg = chess.svg.board(flipped=turn, board=board, lastmove=lastmove)

    img_png = cairosvg.svg2png(svg)
    img = Image.open(BytesIO(img_png))

    plt.ion()
    plt.axis("off")
    plt.imshow(img)
    plt.show(block=False)


def solution_san(moves: str, board: chess.Board):
    moves_uci = moves.split(" ")[1:]
    moves = [chess.Move.from_uci(uci) for uci in moves_uci]
    translation_table = str.maketrans("QNBR", "DSLT")

    return board.variation_san(moves).translate(translation_table)


def is_variation_okay(expected_input: str, user_input: str):
    list1 = expected_input.split(" ")
    list2 = user_input.split(" ")

    return list1[:-2] == list2[:-2] and list1[-1] == list2[-1]


def expected_input(solution: str):
    return re.sub(r"\d+\.\.* ?", "", solution)


def push_previous_move(moves: str, board: chess.Board):
    move = chess.Move.from_uci(moves.split(" ")[0])
    board.push(move)

    return move


def push_solution(moves: str, board: chess.Board):
    for move in moves.split(" ")[1:]:
        board.push(chess.Move.from_uci(move))


def rating_by_seconds(time_spent: timedelta):
    if time_spent.total_seconds() < 30:
        return Rating.Easy
    elif time_spent.total_seconds() < 60:
        return Rating.Good
    else:
        return Rating.Hard


if __name__ == "__main__":
    # deck = Deck('top_5_1400_1600')
    deck = Deck("selection_1600_1800")
    deck.load()
    # data = extract()
    print()

    f = FSRS()
    due = deck.due()

    print(f"{len(due)} tactics are due for repetition\n")

    for card in due:
        # card = ChessCard(tactic['FEN'], tactic['Moves'], tactic['Themes'])

        before = datetime.utcnow()
        scheduling_cards = f.repeat(card, before)

        board = chess.Board(card.fen)
        previous_move = push_previous_move(card.moves, board)
        player = "White" if board.turn else "Black"

        display(board, lastmove=previous_move)
        response = input(f"{player} to move: ")
        print(f"motifs are: {card.themes}")
        solution = solution_san(card.moves, board)
        expected = expected_input(solution)
        print(solution)

        time_spent = datetime.utcnow() - before

        # it's fine to answer more moves than expected
        if response.startswith(expected):
            print(f"You solved puzzle {card.id}!")
            rating = rating_by_seconds(time_spent)
        elif is_variation_okay(expected, response):
            print(f"Your response was {response}")
            print(f"Expected response is {expected}")
            passed = input("mark as completed [yN]? ")

            rating = rating_by_seconds(time_spent) if passed == "y" else Rating.Again
        else:
            input(f"Try puzzle {card.id} again another time.")
            rating = Rating.Again

        push_solution(card.moves, board)
        display(board, flip=True)

        updated_card = scheduling_cards[rating].card
        review_log = scheduling_cards[rating].review_log
        deck.save_card(updated_card, review_log)
        print(
            f"it took you {time_spent.total_seconds()} seconds to solve this puzzle. it is due again at {updated_card.due}"
        )
        input("Next?")
        print()
