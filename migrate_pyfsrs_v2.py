import datetime

from chesscards.card import Deck

if __name__ == '__main__':
    for name in ['yusupov', 'selection_1600_1800']:
        d = Deck(name)
        d.load()

        for card in d.cards:
            card.due = card.due.replace(tzinfo=datetime.timezone.utc)

            if hasattr(card, 'last_review'):
                card.last_review = card.last_review.replace(tzinfo=datetime.timezone.utc)

        d.save_deck()
