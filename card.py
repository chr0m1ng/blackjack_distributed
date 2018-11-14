class Card:
    def __init__(self, suit, value):
        self.suit = suit
        try:
            self.value = int(value)
        except:
            if value == 'A':
                self.value = 1
            elif value == 'J' or value == 'Q' or value == 'K':
                self.value = 10

    def __str__(self):
        return '%s of %s' % (self.value, self.suit)
