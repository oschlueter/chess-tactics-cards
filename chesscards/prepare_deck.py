from card import Deck

if __name__ == "__main__":
    # Deck.create_from_csv("selection_1600_1800", "extract.csv")
    deck = Deck.create_from_csv("yusupov", "yusupov.csv", source="book")
    deck.save_deck()

