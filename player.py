from collections import Counter
from queue import LifoQueue
from random import randint

from strategy import Strategy
from utils import Card
from utils import Move


class Player:
    """ Player class contains full information about the player including
        information known only to the player (strategy, cards on hand,
        cards on board) as well as known to everybody (player id, number of
        points)
    """
    def __init__(self, idx: int, strategy: Strategy) -> None:
        self.idx = idx
        self.points = 0
        self.strategy = strategy
        self.stack = []  # Cards on the board
        self.hand = Counter({Card.Rose: 3,
                             Card.Skull: 1})

    def __str__(self) -> str:
        return f"Player {self.idx + 1}"

    def restart(self) -> None:
        # Put all the cards from the board into hand
        for card in self.stack:
            self.hand[card] += 1
        self.stack = []

    def put_card(self, move: Move) -> None:
        #print(self.hand)
        if move == Move.Put_Rose:
            self.hand[Card.Rose] -= 1
            self.stack.append(Card.Rose)
        else:
            self.hand[Card.Skull] -= 1
            self.stack.append(Card.Skull)
        #print(self.hand)

    def add_point(self) -> None:
        self.points += 1

    def lose_card(self):
        cards_num = self.hand.total()
        lost = randint(0, cards_num - 1)
        if lost < self.hand[Card.Rose]:
            self.hand[Card.Rose] -= 1
        else:
            self.hand[Card.Skull] -= 1

    def discard(self, card: Card):
        if card == Card.Rose:
            self.hand[Card.Rose] -= 1
        else:
            self.hand[Card.Skull] -= 1

    @property
    def active(self):
        """ Player is considered active if there is at least one card in hand
            or board
        """
        return len(self.stack) + self.hand.total() > 0
