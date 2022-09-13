import unittest

from queue import LifoQueue
from collections import Counter

from board import Board
from player import Player
from strategy import Strategy
from strategy import RandomStrategy

from utils import Card
from utils import Move
from utils import Phase


class TestBoard(unittest.TestCase):

    def test_constructor(self):
        player_1_hand = Counter({Card.Rose: 1,
                                 Card.Skull: 0})
        player_1_stack = [Card.Rose, Card.Skull]

        player_2_hand = Counter({Card.Unknown: 2})
        player_2_stack = [Card.Unknown]

        player_3_hand = Counter({Card.Unknown: 1})
        player_3_stack = [Card.Unknown]

        player_hands = [player_1_hand, player_2_hand, player_3_hand]
        player_stacks = [player_1_stack, player_2_stack, player_3_stack]

        bets = [Move.Bet_0 for _ in range(3)]

        board = Board(
            phase = Phase.Put_Cards,
            points = [1, 0, 0],
            active_player_mask = [True, True, True],
            bets = bets,
            player_idx = 0,
            player_stacks = player_stacks,
            player_hands = player_hands,
        )

        self.assertTrue(hasattr(board, "phase"))
        self.assertTrue(hasattr(board, "points"))
        self.assertTrue(hasattr(board, "active_player_mask"))
        self.assertTrue(hasattr(board, "bets"))
        self.assertTrue(hasattr(board, "player_idx"))
        self.assertTrue(hasattr(board, "player_stacks"))
        self.assertTrue(hasattr(board, "player_hands"))

        self.assertTrue(isinstance(board.phase, Phase))
        self.assertTrue(isinstance(board.points, list))
        self.assertTrue(isinstance(board.active_player_mask, list))
        self.assertTrue(isinstance(board.active_player_mask[0], bool))
        self.assertTrue(isinstance(board.bets, list))
        self.assertTrue(isinstance(board.bets[0], Move))
        self.assertTrue(isinstance(board.player_idx, int))
        self.assertTrue(isinstance(board.player_stacks, list))
        self.assertTrue(isinstance(board.player_stacks[0], list))
        self.assertTrue(isinstance(board.player_stacks[0][0], Card))
        self.assertTrue(isinstance(board.player_hands, list))
        self.assertTrue(isinstance(board.player_hands[0], Counter))
        self.assertTrue(isinstance(board.player_hands[0][Card.Rose], int))

        self.assertEqual(board.phase, Phase.Put_Cards)
        self.assertEqual(board.points, [1, 0, 0])
        self.assertEqual(board.active_player_mask, [True, True, True])
        self.assertEqual(board.bets, bets)
        self.assertEqual(board.player_idx, 0)
        self.assertEqual(board.player_stacks, player_stacks)
        self.assertEqual(board.player_hands, player_hands)


if __name__ == '__main__':
    unittest.main()
