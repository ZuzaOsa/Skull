from enum import Enum

MAX_PLAYERS = 6
POINTS_TO_WIN = 2

Card = Enum('Card', ['Rose', 'Skull'])
Move = Enum('Move', ['Put_Rose', 'Put_Skull', 'Bet', 'Pass'] +
                    [f'Bet_{i}' for i in range(1, 4*MAX_PLAYERS + 1)] +
                    [f'Reveal_{i}' for i in range(MAX_PLAYERS)] +
                    [f'Discard_Rose', 'Discard_Skull'])
Phase = Enum('Phase', ['Put_Cards', 'Bet', 'Reveal', 'Discard'])
