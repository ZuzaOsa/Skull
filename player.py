from strategy import Strategy
from utils import Move
from utils import Card

class Player(object):
    def __init__(self, id: int, strategy: Strategy):
        self.id = id
        self.hand_roses = 3
        self.hand_skulls = 1
        self.cards_board = []
        self.strategy = strategy
        self.points = 0

    def put_card(self, move: Move) -> Card:
        if move == Move.Rose:
            self.hand_roses -= 1
            self.cards_board.append(Card.Rose)
        elif move == Move.Skull:
            self.hand_skulls -= 1
            self.cards_board.append(Card.Skull)
        else:
            raise ValueError("Invalid move")

    def return_card(self) -> None:
        assert len(self.cards_board) > 0
        card = self.cards_board.pop()
        if card == SKULL:
            self.hand_skulls += 1
        elif card == ROSE:
            self.hand_roses += 1
        else:
            raise ValueError("Invalid card")

    def discard_card(self, card: Card) -> None:
        if card == SKULL:
            self.hand_skulls = 0
        elif card == ROSE:
            self.hand_roses -= 1
        else:
            raise ValueError("Invalid card")

    def lose_card(self) -> Card:
        hand = [ROSE] * self.hand_roses + [SKULL] * self.hand_skulls
        card = random.choose(hand)
        if card == ROSE:
            self.hand_roses -= 1
            return ROSE
        elif card == SKULL:
            self.hand_skulls = 0
            return SKULL
        else:
            raise ValueError("Invalid card")

    def score_point(self) -> None:
        self.points += 1

    @property
    def active(self):
        return self.hand_roses + self.hand_skulls + len(self.cards_board) > 0

    def __str__(self):
        return f"Player {self.id}"
