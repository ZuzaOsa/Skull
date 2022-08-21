from collections import Counter
from queue import LifoQueue

from strategy import Strategy
from utils import Card


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
        self.stack = LifoQueue()  # Cards on the board
        self.hand = Counter({Card.Rose: 3,
                             Card.Skull: 1})

    def __str__(self) -> str:
        return f"Player {self.idx + 1}"

    def restart(self) -> None:
        # Put all the cards from the board into hand
        while not self.stack.empty():
            card = self.stack.get()
            self.hand[card] += 1

    @property
    def active(self):
        """ Player is considered active if there is at least one card in hand
            or board
        """
        return not self.stack.empty() or sum(self.hand.values()) > 0

    # TODO rest of the methods
    ...
