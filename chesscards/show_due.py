from collections import Counter

from chesscards.card import Deck, ChessCard


def per_date(cards: [ChessCard]):
    # Assuming your list of objects is named 'objects_list' and each object has a 'due' attribute
    # First, extract the 'due' dates from each object
    dates = [obj.due.date() for obj in cards]

    # Then, use Counter to count the occurrences of each date
    return Counter(dates).items()


def show(cards: [ChessCard], due: str = "due"):
    print(f"{len(cards)} tactics are {due} for repetition:")
    for date, count in per_date(cards):
        print(f"Date: {date}, Count: {count}")


if __name__ == "__main__":
    d = Deck("selection_1600_1800")
    # d = Deck('top_5_1400_1600')
    d.load()

    show(d.due_until_end_of_day(), "due")
    show(d.due_after_end_of_day(), "not due")
