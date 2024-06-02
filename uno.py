import uno_deck
import os
import time

GAME_RULES = """
UNO Game Rules:
1. Players take turns matching a card from their hand with the current card shown on top of the deck.
2. A match is made by color or number.
3. Special cards (Reverse, Skip, Draw Two, Wild, Wild Draw Four) have special actions.
4. If a player cannot match the top card, they must draw a card from the deck.
5. The first player to get rid of all their cards wins the round.
6. If you have one card left, you must call 'UNO' or draw two penalty cards.
7. Use '-h' anytime to view these rules.

Press any key to continue...
"""

class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.called_uno = False

    def draw(self, deck, count=1):
        self.hand.extend(deck.draw_multiple(count))

    def play_card(self, card):
        self.hand.remove(card)
        return card

    def has_won(self):
        return len(self.hand) == 0

    def has_one_card(self):
        return len(self.hand) == 1

    def calculate_score(self):
        score = 0
        for card in self.hand:
            if card.endswith('Draw Two') or card.endswith('Reverse') or card.endswith('Skip'):
                score += 20
            elif card.startswith('Wild'):
                score += 50
            else:
                value = card.split()[-1]
                if value.isdigit():
                    score += int(value)
                else:
                    score += 10
        return score

class UNOGame:
    def __init__(self, player_names):
        self.deck = uno_deck.Deck()
        self.players = [Player(name) for name in player_names]
        self.discard_pile = []
        self.current_player_index = 0
        self.direction = 1
        self.init_hands()
        self.init_discard_pile()

    def init_hands(self):
        for player in self.players:
            player.draw(self.deck, 7)

    def init_discard_pile(self):
        card = self.deck.draw_card()
        while 'Wild' in card or 'Draw Four' in card:
            self.deck.cards.insert(0, card)
            card = self.deck.draw_card()
        self.discard_pile.append(card)

    def next_player(self, steps=1):
        self.current_player_index = (self.current_player_index + steps * self.direction) % len(self.players)

    def play_turn(self):
        player = self.players[self.current_player_index]
        top_card = self.discard_pile[-1]
        self.clear_screen()
        print(f"\n{player.name}'s turn. Top card: {top_card}")
        print(f"Your hand: {player.hand}")

        if player.has_one_card() and not player.called_uno:
            print("You forgot to call UNO! Drawing two penalty cards.")
            player.draw(self.deck, 2)

        player.called_uno = False

        playable_cards = [card for card in player.hand if self.is_playable(card, top_card)]
        if playable_cards:
            print(f"Playable cards: {playable_cards}")
            card = self.get_card_choice(player, playable_cards)
            self.discard_pile.append(player.play_card(card))
            print(f"{player.name} played {card}")

            if player.has_one_card():
                self.call_uno(player)

            if player.has_won():
                print(f"{player.name} has won the game!")
                self.display_final_scores()
                return True

            if 'Reverse' in card:
                self.direction *= -1
            if 'Skip' in card:
                self.next_player()
            if 'Draw Two' in card:
                self.next_player()
                self.players[self.current_player_index].draw(self.deck, 2)
            if 'Wild' in card or 'Wild Draw Four' in card:
                new_color = self.choose_color(player)
                print(f"{player.name} changed color to {new_color}")
                self.discard_pile[-1] = f'{new_color} Wild'
                if 'Draw Four' in card:
                    self.next_player()
                    self.players[self.current_player_index].draw(self.deck, 4)
        else:
            player.draw(self.deck)
            print(f"{player.name} drew a card")

        self.next_player()
        self.end_turn()
        return False

    def get_card_choice(self, player, playable_cards):
        while True:
            choice = input(f"{player.name}, choose a card to play from {playable_cards}: ")
            if choice in playable_cards:
                return choice
            else:
                print("Invalid choice. Please choose a playable card.")

    def is_playable(self, card, top_card):
        card_parts = card.split()
        top_parts = top_card.split()
        card_color = card_parts[0] if len(card_parts) > 1 else ''
        card_value = card_parts[-1]
        top_color = top_parts[0] if len(top_parts) > 1 else ''
        top_value = top_parts[-1]
        return card_color == top_color or card_value == top_value or 'Wild' in card

    def choose_color(self, player):
        colors = ['Red', 'Green', 'Blue', 'Yellow']
        while True:
            color = input(f"{player.name}, choose a color ({', '.join(colors)}): ").capitalize()
            if color in colors:
                return color

    def call_uno(self, player):
        call = input().strip().lower()
        if call == 'uno':
            player.called_uno = True
            print(f"{player.name} successfully called UNO!")

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def end_turn(self):
        input("Press any key to end your turn and pass to the next player...")
        self.clear_screen()

    def display_final_scores(self):
        print("\nFinal Scores:")
        for player in self.players:
            score = player.calculate_score()
            print(f"{player.name}: {score} points")

    def start(self):
        print("Starting UNO game!")
        while True:
            if self.play_turn():
                break

if __name__ == "__main__":
    player_names = input("Enter player names separated by commas: ").split(',')
    game = UNOGame([name.strip() for name in player_names])
    game.start()
