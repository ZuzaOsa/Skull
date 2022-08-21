from abc import abstractmethod
from typing import Set

from board import Board
from utils import Move


class Strategy:
    @abstractmethod
    def get_move(self, board: Board) -> Move:
        raise NotImplementedError

    @staticmethod
    def get_legal_moves(board: Board) -> Set[Move]:
        # TODO
        raise NotImplementedError
        legal_moves = set()
        ...
        return legal_moves


class ManualStrategy(Strategy):
    @staticmethod
    def get_move_from_input() -> Move:
        # TODO
        raise NotImplementedError

    def get_move(self, board: Board) -> Move:
        print(board)
        legal_moves = self.get_legal_moves(board)
        move = get_move_from_input()
        while move not in legal_moves:
            print(f"{move} is not a legal move")
            move = get_move_from_input()
        return move


class RandomStrategy(Strategy):
    def get_move(self, board: Board) -> Move:
        legal_moves = self.get_legal_moves(board)
        move = random.choice(legal_moves)
        return move
