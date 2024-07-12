That’s the design and everything explained down!!!

https://www.figma.com/design/2gerbM45yxP7qm9EBIwPdU/EstateX-Game?m=dev&node-id=0-1&t=8YVlZGJXO8KSlAD1-1

Once you review along with the doc here:
https://docs.google.com/document/d/1GPu_--K5sBtHSV0m5ptjoMAbRshNHl7SYnx3GU2H0Rg/edit?usp=sharing




# UNO Game

This is a text-based UNO game playable in the terminal/console. It supports 2 to 8 players with customizable names.

## How to Run

1. Ensure both `uno.py` and `uno_deck.py` are in the same directory.
2. Run the game with the command:
`sh
python uno.py
`

## Game Rules

UNO Game Rules:
1. Players take turns matching a card from their hand with the current card shown on top of the deck.
2. A match is made by color or number.
3. Special cards (Reverse, Skip, Draw Two, Wild, Wild Draw Four) have special actions.
4. If a player cannot match the top card, they must draw a card from the deck.
5. The first player to get rid of all their cards wins the round.
6. If you have one card left, you must call 'UNO' or draw two penalty cards.
7. Use '-h' anytime to view these rules.
