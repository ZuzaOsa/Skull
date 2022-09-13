import unittest

from queue import LifoQueue
from collections import Counter

from player import Player
from strategy import Strategy
from strategy import RandomStrategy

from utils import Card


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player(idx=0, strategy=RandomStrategy())

    def test_constructor(self):
        self.assertTrue(hasattr(self.player, "idx"))
        self.assertTrue(hasattr(self.player, "points"))
        self.assertTrue(hasattr(self.player, "strategy"))
        self.assertTrue(hasattr(self.player, "stack"))
        self.assertTrue(hasattr(self.player, "hand"))

        self.assertTrue(isinstance(self.player.idx, int))
        self.assertTrue(isinstance(self.player.points, int))
        self.assertTrue(isinstance(self.player.strategy, Strategy))
        self.assertTrue(isinstance(self.player.strategy, RandomStrategy))
        self.assertTrue(isinstance(self.player.stack, list))
        self.assertTrue(isinstance(self.player.hand, Counter))

        self.assertEqual(self.player.idx, 0)
        self.assertEqual(self.player.points, 0)
        self.assertEqual(len(self.player.stack), 0)
        self.assertEqual(self.player.hand[Card.Rose], 3)
        self.assertEqual(self.player.hand[Card.Skull], 1)

    def test_str(self):
        self.assertEqual(str(self.player), "Player 1")

    def test_restart(self):
        self.player.hand = Counter({Card.Rose: 0,
                                    Card.Skull: 0})
        self.player.stack = [Card.Rose, Card.Rose, Card.Skull]
        self.player.restart()
        self.assertEqual(self.player.hand[Card.Rose], 2)
        self.assertEqual(self.player.hand[Card.Skull], 1)
        self.assertEqual(len(self.player.stack), 0)

    def test_active(self):
        self.assertTrue(self.player.active)

        self.player.hand = Counter({Card.Rose: 0,
                                    Card.Skull: 0})
        self.assertFalse(self.player.active)

        self.player.stack.append(Card.Rose)
        self.assertTrue(self.player.active)


if __name__ == '__main__':
    unittest.main()
