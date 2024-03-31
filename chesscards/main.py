import re
from datetime import datetime, timedelta
from io import BytesIO

import cairosvg
import chess.svg
import matplotlib.pyplot as plt
from fsrs import FSRS, Rating
from PIL import Image

from chesscards.card import Deck


def display_svg(svg: str):
    img_png = cairosvg.svg2png(svg)
    img = Image.open(BytesIO(img_png))

    plt.ion()
    plt.axis("off")
    plt.imshow(img)
    plt.show(block=False)


def expected_input(solution: str):
    return re.sub(r"\d+\.\.* ?", "", solution)


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
    due = deck.due_shuffle()

    print(f"{len(due)} tactics are due for repetition\n")

    for card in due:
        before = datetime.utcnow()
        scheduling_cards = f.repeat(card, before)

        board = card.board()
        player = "White" if board.turn else "Black"

        display_svg(card.exercise_svg())
        response = input(f"{player} to move: ")
        print(f"motifs are: {card.themes}")
        solution = card.solution_san()
        expected = expected_input(solution)
        print(solution)

        time_spent = datetime.utcnow() - before

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
        review_log = scheduling_cards[rating].review_log
        deck.save_card(updated_card, review_log)
        print(
            f"it took you {time_spent.total_seconds()} seconds to solve this puzzle. it is due again at {updated_card.due}"
        )
        input("Next?")
        print()
