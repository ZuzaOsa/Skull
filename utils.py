from enum import Enum
from enum import unique

MAX_PLAYERS = 6
POINTS_TO_WIN = 2


class Phase(Enum):
    Put_Cards = "Put Cards"
    Bet = "Bet"
    Reveal = "Reveal"
    Discard = "Discard"

    def __str__(self):
        return self.value


class Card(Enum):
    Rose = 'R'
    Skull = 'S'
    Unknown = '#'

    def __str__(self):
        return self.value


# TOOD this looks ugly, find a better way to define multiple enum values
@unique
class Move(Enum):
    # Moves during Put_Cards phase
    Put_Rose = 'R'
    Put_Skull = 'S'
    Bet = 'B'

    # Moves during Discard phase
    Discard_Rose = 'DR'
    Discard_Skull = 'DS'

    # Moves during Reveal phase
    Reveal_0 = '0'
    Reveal_1 = '1'
    Reveal_2 = '2'
    Reveal_3 = '3'
    Reveal_4 = '4'
    Reveal_5 = '5'

    # Moves during Bet phase
    Pass = 'P'
    Bet_0 = " "
    Bet_1 = 1
    Bet_2 = 2
    Bet_3 = 3
    Bet_4 = 4
    Bet_5 = 5
    Bet_6 = 6
    Bet_7 = 7
    Bet_8 = 8
    Bet_9 = 9
    Bet_10 = 10
    Bet_11 = 11
    Bet_12 = 12
    Bet_13 = 13
    Bet_14 = 14
    Bet_15 = 15
    Bet_16 = 16
    Bet_17 = 17
    Bet_18 = 18
    Bet_19 = 19
    Bet_20 = 20
    Bet_21 = 21
    Bet_22 = 22
    Bet_23 = 23
    Bet_24 = 24

    def __str__(self):
        return str(self.value)


Bet_i = [
    Move.Bet_0, Move.Bet_1, Move.Bet_2, Move.Bet_3, Move.Bet_4, Move.Bet_5,
    Move.Bet_6, Move.Bet_7, Move.Bet_8, Move.Bet_9, Move.Bet_10, Move.Bet_11,
    Move.Bet_12, Move.Bet_13, Move.Bet_14, Move.Bet_15, Move.Bet_16,
    Move.Bet_17, Move.Bet_18, Move.Bet_19, Move.Bet_20, Move.Bet_21,
    Move.Bet_22, Move.Bet_23, Move.Bet_24, Move.Pass]

Reveal_i = [
    Move.Reveal_0, Move.Reveal_1, Move.Reveal_2, Move.Reveal_3, Move.Reveal_4,
    Move.Reveal_5]