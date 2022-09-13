from queue import LifoQueue
from collections import Counter

from player import Player
from board import Board
from strategy import RandomStrategy

from utils import Card
from utils import Move
from utils import Phase


player_1_hand = Counter({Card.Rose: 1,
                         Card.Skull: 0})
player_1_stack = [Card.Rose, Card.Skull]

player_2_hand = Counter({Card.Unknown: 2})
player_2_stack = [Card.Unknown]

player_3_hand = Counter({Card.Unknown: 1})
player_3_stack = [Card.Unknown]

player_hands = [player_1_hand, player_2_hand, player_3_hand]
player_stacks = [player_1_stack, player_2_stack, player_3_stack]

bets = [Move.Bet_0, Move.Bet_3, Move.Pass]

board = Board(
    phase = Phase.Bet,
    points = [1, 0, 1],
    active_player_mask = [True, True, True],
    bets = bets,
    player_idx = 0,
    player_stacks = player_stacks,
    player_hands = player_hands,
)

print(board)
