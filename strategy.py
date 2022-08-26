from pydoc import plain
import random

from abc import abstractmethod
from typing import Set

from board import Board
from utils import Move
from utils import Card
from utils import Phase
from utils import Bet_i
from utils import Reveal_i


class Strategy:
    @abstractmethod
    def get_move(self, board: Board) -> Move:
        raise NotImplementedError

    @staticmethod
    def get_legal_moves(board: Board) -> Set[Move]:
        legal_moves = set()
        if board.phase == Phase.Put_Cards:
            if Card.Rose in board.player_hands[board.player_idx]:
                legal_moves.add(Move.Put_Rose)
            if Card.Skull in board.player_hands[board.player_idx]:
                legal_moves.add(Move.Put_Skull)
            if board.player_stacks[board.player_idx]:
                legal_moves.add(Move.Bet)
        if board.phase == Phase.Bet:
            assert len(board.bets) == board.player_num
            if board.highest_bet > 0:
                legal_moves.add(Move.Pass)
            for i in range(board.highest_bet + 1, board.cards_board_num + 1):
                legal_moves.add(Bet_i[i])
        if board.phase == Phase.Reveal:
            assert len(board.player_stacks[board.player_idx]) == 0
            for i in range(0, board.player_num):
                if board.player_stacks[i]:
                    legal_moves.add(Reveal_i[i])
        if board.phase == Phase.Discard:
            assert len(board.player_stacks[board.player_idx]) == 0
            legal_moves.add(Move.Discard_Skull)
            if board.player_hands[board.player_idx].total() > 1:
                legal_moves.add(Move.Discard_Rose)
        return legal_moves


class ManualStrategy(Strategy):
    @staticmethod
    def get_move_from_input() -> Move:
        # TODO
        raise NotImplementedError

    def get_move(self, board: Board) -> Move:
        print(board)
        legal_moves = self.get_legal_moves(board)
        move = self.get_move_from_input()
        while move not in legal_moves:
            print(f"{move} is not a legal move")
            move = self.get_move_from_input()
        return move


class RandomStrategy(Strategy):
    def get_move(self, board: Board) -> Move:
        legal_moves = self.get_legal_moves(board)
        move = random.choice(legal_moves)
        return move
