from datetime import datetime

from card import Deck
from dateutil.tz import tzlocal, tzutc


def to_local(dt: datetime):
    return dt.replace(tzinfo=tzutc()).astimezone(tzlocal())


if __name__ == "__main__":
    deck = Deck("selection_1600_1800")
    # deck = Deck('top_5_1400_1600')
    deck.load()

    due = deck.due_shuffle()
    print(f"{len(due)} tactics are due for repetition:")
    for tactic in due:
        print(f"{to_local(tactic.due)} {tactic.id}")

    not_due = deck.not_due()
    print()
    print(f"{len(not_due)} tactics are not due for repetition until:")
    for tactic in not_due:
        print(f"{to_local(tactic.due)} {tactic.id}")
