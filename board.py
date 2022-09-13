from typing import List
from typing import Counter
from typing import TypeVar

from utils import Phase
from utils import Card
from utils import Move
from utils import Bet_i

Queue = TypeVar("Queue")


class Board:
    """ Board is used to represent the current game state from a perspective
        of a given player. Board object should be immutable.
    """
    def __init__(
            self,
            phase: Phase,
            points: List[int],
            active_player_mask: List[bool],
            bets: List[Move],
            player_stacks: List[List[Card]],
            player_hands: List[Counter[Card]],
            player_idx: int,
            ) -> None:
        self.player_num = len(points)
        self.phase = phase
        self.points = points
        self.active_player_mask = active_player_mask
        self.bets = bets
        self.player_stacks = player_stacks
        self.player_hands = player_hands
        self.player_idx = player_idx

        assert len(self.active_player_mask) == self.player_num
        assert len(self.bets) == self.player_num

    def __str__(self) -> str:
        out = ""
        out += "*" * 30
        out += '\n'
        out += f"Phase: {self.phase} \n"
        out += "*" * 30
        out += '\n'

        # Mark current player
        for i in range(self.player_num):
            out += "A " if i == self.player_idx else "  "
        out += "     <- Active player"
        out += '\n'
        out += "-" * (2 * self.player_num) + '\n'

        # Print players
        for i in range(self.player_num):
            out += f"{str(i + 1)} " if self.active_player_mask[i] else "- "
        out += "     <- Player number"
        out += '\n'
        out += "-" * (2 * self.player_num) + '\n'

        # Print points
        for i in range(self.player_num):
            out += "x " if self.points[i] else "  "
        out += "     <- Points"
        out += '\n'
        out += "-" * (2 * self.player_num) + '\n'

        # Print number of cards in hand
        max_cards_in_hand = max([sum(hand.values())
                                for hand in self.player_hands])
        for i in range(max_cards_in_hand):
            for j in range(self.player_num):
                card = None
                if self.player_hands[j][Card.Rose] > 0:
                    self.player_hands[j][Card.Rose] -= 1
                    card = Card.Rose
                elif self.player_hands[j][Card.Skull] > 0:
                    self.player_hands[j][Card.Skull] -= 1
                    card = Card.Skull
                elif self.player_hands[j][Card.Unknown] > 0:
                    self.player_hands[j][Card.Unknown] -= 1
                    card = Card.Unknown

                out += f"{card} " if card is not None else "  "
            if i == 0:
                out += "     <- Cards in hand"
            out += '\n'
        out += "-" * (2 * self.player_num) + '\n'

        # Print bets
        for bet in self.bets:
            out += f"{bet} "
        out += "     <- Bets"
        out += '\n'
        out += "-" * (2 * self.player_num) + '\n'

        # Print cards on board
        max_cards_in_stack = max([len(stack) for stack in self.player_stacks])
        for i in range(max_cards_in_stack - 1, -1, -1):
            for j in range(self.player_num):
                if len(self.player_stacks[j]) > i:
                    card = self.player_stacks[j][i]
                    out += f"{card} "
                else:
                    out += "  "
            if i == max_cards_in_stack - 1:
                out += "     <- Board"
            out += '\n'
        out += "*" * 30
        out += '\n'

        return out

    @property
    def cards_board_num(self):
        cards = 0
        for i in self.player_stacks:
            cards += len(i)
        return cards

    @property
    def highest_bet(self):
        bet = 0
        for i in self.bets:
            if i == Move.Pass:
                continue
            bet = max(bet, Bet_i.index(i))
        return bet