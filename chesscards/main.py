import re
from datetime import datetime, timedelta, UTC
from io import BytesIO

import cairosvg
import chess.svg
import matplotlib.pyplot as plt
from fsrs import FSRS, Rating
from PIL import Image

from chesscards.card import Deck, MyReviewLog


def display_svg(svg: str):
    img_png = cairosvg.svg2png(svg)
    img = Image.open(BytesIO(img_png))

    plt.ion()
    plt.axis("off")
    plt.imshow(img)
    plt.show(block=False)


def expected_input(solution: str):
    return re.sub(r"\d+\.\.* ?", "", solution)


def rating_by_seconds(time_spent: int):
    if time_spent < 30:
        return Rating.Easy
    elif time_spent < 60:
        return Rating.Good
    else:
        return Rating.Hard


def train(deck: Deck):
    # data = extract()
    f = FSRS()
    # due = Deck.shuffle(deck.not_due())
    due = Deck.shuffle(deck.due_until_end_of_day())
    print(f"{len(due)} tactics are due for repetition\n")
    for card in due:
        before = datetime.now(UTC)
        scheduling_cards = f.repeat(card, before)

        board = card.board()
        player = "White" if board.turn else "Black"

        display_svg(card.exercise_svg())
        response = input(f"{player} to move: ")
        print(f"motifs are: {card.themes}")
        solution = card.solution_san()
        expected = expected_input(solution)
        print(solution)

        time_spent = int((datetime.now(UTC) - before).total_seconds())

        # it's fine to answer more moves than expected
        if response.startswith(expected):
            print(f"You solved puzzle {card.id}!")
            rating = rating_by_seconds(time_spent)
        else:
            print(f"Your response was    {response}")
            print(f"Expected response is {expected}")
            passed = input(f"mark puzzle {card.id} as completed [yN]? ")

            rating = rating_by_seconds(time_spent) if passed == "y" else Rating.Again

        display_svg(card.solution_svg())

        updated_card = scheduling_cards[rating].card
        review_log = MyReviewLog.from_log(scheduling_cards[rating].review_log, time_spent)
        deck.save_card(updated_card, review_log)
        print(f"it took you {time_spent} seconds to solve this puzzle. it is due again at {updated_card.due}")

        keep_going = input("Next [Yn]?")
        if keep_going == "n":
            break
        print()


if __name__ == "__main__":
    # d = Deck("top_5_1400_1600")
    d = Deck("selection_1600_1800")
    d.load()

    train(d)
