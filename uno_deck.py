import random

class Deck:
    def __init__(self):
        self.cards = self.create_deck()
        self.shuffle()

    def create_deck(self):
        colors = ['Red', 'Green', 'Blue', 'Yellow']
        values = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', 'Draw Two']
        special_cards = ['Wild', 'Wild Draw Four']
        deck = []

        for color in colors:
            deck.append(f'{color} 0')
            for value in values[1:]:
                deck.extend([f'{color} {value}'])
        
        deck.extend(special_cards * 4)
        return deck

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        if not self.cards:
            self.cards = self.create_deck()
            self.shuffle()
        return self.cards.pop()

    def draw_multiple(self, count):
        return [self.draw_card() for _ in range(count)]
