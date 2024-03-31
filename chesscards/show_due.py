from collections import Counter
from datetime import datetime

from card import Deck, ChessCard
from dateutil.tz import tzlocal, tzutc


def to_local(dt: datetime):
    return dt.replace(tzinfo=tzutc()).astimezone(tzlocal())


def per_date(cards: [ChessCard]):
    # Assuming your list of objects is named 'objects_list' and each object has a 'due' attribute
    # First, extract the 'due' dates from each object
    dates = [obj.due.date() for obj in cards]

    # Then, use Counter to count the occurrences of each date
    return Counter(dates).items()


if __name__ == "__main__":
    deck = Deck("selection_1600_1800")
    # deck = Deck('top_5_1400_1600')
    deck.load()

    due = deck.due()

    # Now, 'date_counts' is a dictionary where the keys are the dates and the values are the counts
    print(f"{len(due)} tactics are due for repetition:")
    for date, count in per_date(due):
        print(f"Date: {date}, Count: {count}")

    not_due = deck.not_due()

    print(f"{len(not_due)} tactics are not due for repetition until:")
    for date, count in per_date(not_due):
        print(f"Date: {date}, Count: {count}")
