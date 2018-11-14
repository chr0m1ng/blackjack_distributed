from card import Card
import numpy as np


class Deck:
    def __init__(self):
        values = ['2', '3', '4', '5', '6', '7',
                  '8', '9', '10', 'A', 'J', 'Q', 'K']
        hearts = [Card('hearts', x) for x in values]
        spades = [Card('spades', x) for x in values]
        clubs = [Card('clubs', x) for x in values]
        diamonds = [Card('diamonds', x) for x in values]
        self.cards = hearts + spades + clubs + diamonds
        np.random.shuffle(self.cards)

    def pop(self):
        return self.cards.pop()

    def empty(self):
        return len(self.cards) == 0
