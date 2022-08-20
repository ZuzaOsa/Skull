import random
import collections

from typing import List

from strategy import Strategy
from player import Player
from board import Board

from utils import Card
from utils import Move

ROSE = Card.Rose
SKULL = Card.Skull
BET = Move.Bet

POINTS_TO_WIN = 2


class Game(object):
    def __init__(self, strategies: List[Strategy]):
        self.player_num = len(strategies)
        assert self.player_num >= 2

        self.winner = None
        self.starting_player_idx = 0
        self.players = [Player(id=i + 1, strategy=strategy)
                        for i, strategy in enumerate(strategies)]

    def restart(self):
        assert all(p <= POINTS_TO_WIN for p in self.points)
        if POINTS_TO_WIN in self.points:
            assert points.count(POINTS_TO_WIN) == 1
            winner_idx = points.index(POINTS_TO_WIN)
            self.winner = self.players[winner_idx]
            return

        assert self.active_player_mask.count(True) >= 1
        if self.active_player_mask.count(True) == 1:
            winner_idx = self.active_player_mask.index(True)
            self.winner = self.players[winner_idx]
            return

        for player in self.players:
            player.return_cards()

    def show(self, player: Player, bet: int):
        self.starting_player = player.id
        while player.cards_board:
            if player.cards_board[-1] == Card.Skull:
                self.restart()
                move = player.strategy.discard(self.get_board_from_perspective(player))
                player.discard_card(move)
                return
            else:
                player.return_card()
                bet -= 1

        if bet <= 0:
            player.score_point()
            return

        while bet > 0:
            move = player.strategy.reveal(self.get_board_from_perspective(player))
            if self.players[move].cards_board[-1] == Card.Skull:
                self.restart()
                card = player.lose_card()
                return
            else:
                bet -= 1
                self.players[move].return_card()
        player.score_point()

    def licitation(self, moving_player):
        bets = []
        highestBet = 0
        for i in range(self.player_num):
            if self.active[i]:
                bets.append(0)
            else:
                bets.append(-1)
        bets[moving_player] = self.strategies[moving_player].licitate(self.players[moving_player], board, 1, highestBet)
        highestBet = bets[moving_player]
        moving_player = (moving_player + 1) % self.player_num
        while bets.count(-1) < self.player_num - 1 and highestBet != self.board.card_count:
            if bets[moving_player] == -1:
                moving_player = (moving_player + 1) % self.player_num
                continue
            bets[moving_player] = self.strategies[moving_player].licitate(self.players[moving_player], board, 0, highestBet)
            highestBet = max(highestBet, bets[moving_player])
            moving_player = (moving_player + 1) % self.player_num
        self.show(self.players[bets.index(highestBet)], highestBet)

    def make_turn(self, player):
        if not player.active:
            return True
        move = player.strategy.make_move(self.get_board_from_perspective(player))
        if move in (Move.Rose, Move.Skull):
            player.put_card(move)
            return True
        elif move == Move.Bet:
            self.licitation(player)
            return False
        else:
            raise ValueError('Invalid move')

    def round(self):
        moving_player_idx = self.starting_player_idx
        moving_player = self.players[moving_player_idx]
        while self.make_turn(moving_player):
            moving_player_idx = (moving_player_idx + 1) % self.player_num
            moving_player = self.players[moving_player_idx]
        self.restart()

    @property
    def active_player_mask(self):
        return [player.active for player in self.players]

    @property
    def points(self):
        return [player.points for player in self.players]

    def get_board(self, active_player):
        cards_hand = [player.hand_roses + player.hand_skulls
                      for player in self.players]
        cards_board = [len(player.cards_board) for player in self.players]
        return Board(
            player_num=self.player_num,
            active_player_mask=self.active_player_mask,
            active_player_idx=active_player.id,
            points=self.points,
            cards_hand=cards_hand,
            cards_board=cards_board,
            )

    def get_board_from_perspective(self, active_player):
        cards_hand = [player.hand_roses + player.hand_skulls
                      for player in self.players]
        cards_board = [len(player.cards_board) for player in self.players]
        return Board(
            player_num=self.player_num,
            active_player_mask=self.active_player_mask,
            active_player_idx=active_player.id,
            points=self.points,
            cards_hand=cards_hand,
            cards_board=cards_board,
            active_player_board=active_player.cards_board,
            active_player_hand_roses=active_player.hand_roses,
            active_player_hand_skulls=active_player.hand_skulls,
            )
