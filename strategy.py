from pydoc import plain
import random

from abc import abstractmethod
from typing import List

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
    def get_legal_moves(board: Board) -> List[Move]:
        legal_moves = []
        if board.phase == Phase.Put_Cards:
            if board.player_hands[board.player_idx][Card.Rose]:
                legal_moves.append(Move.Put_Rose)
            if board.player_hands[board.player_idx][Card.Skull]:
                legal_moves.append(Move.Put_Skull)
            if board.player_stacks[board.player_idx]:
                legal_moves.append(Move.Bet)
        if board.phase == Phase.Bet:
            assert len(board.bets) == board.player_num
            if board.highest_bet > 0:
                legal_moves.append(Move.Pass)
            for i in range(board.highest_bet + 1, board.cards_board_num + 1):
                legal_moves.append(Bet_i[i])
        if board.phase == Phase.Reveal:
            for i in range(0, board.player_num):
                if Card.Unknown in board.player_stacks[i]:
                    legal_moves.append(Reveal_i[i])
        if board.phase == Phase.Discard:
            legal_moves.append(Move.Discard_Skull)
            if board.player_hands[board.player_idx].total() > 1:
                legal_moves.append(Move.Discard_Rose)
        return legal_moves


class ManualStrategy(Strategy):
    @staticmethod
    def get_move_from_input(phase: Phase, player_idx) -> Move:
        move = input(f"Player number {player_idx + 1} moves: ")
        if phase == Phase.Put_Cards:
            if move == "R":
                return Move.Put_Rose
            if move == "S":
                return Move.Put_Skull
            if move == "B":
                return Move.Bet
        if phase == Phase.Bet:
            if move == "P":
                return Move.Pass
            if move.isnumeric():
                move = int(move)
                if move > 0 and move < 25:
                    return Bet_i[move]
        if phase == Phase.Reveal:
            if move.isnumeric():
                move = int(move) - 1
                if move >= 0 and move < 6:
                    return Reveal_i[move]
        if phase == Phase.Discard:
            if move == "DR":
                return Move.Discard_Rose
            if move == "DS":
                return Move.Discard_Skull
        print("This is not a valid move")
        return None

    def get_move(self, board: Board) -> Move:
        legal_moves = self.get_legal_moves(board)
        print(board)
        move = self.get_move_from_input(board.phase, board.player_idx)
        while move not in legal_moves:
            if move is not None:
                print(f"{move} is not a legal move")
            move = self.get_move_from_input(board.phase, board.player_idx)
        return move


class RandomStrategy(Strategy):
    def get_move(self, board: Board) -> Move:
        legal_moves = self.get_legal_moves(board)
        move = random.choice(legal_moves)
        return move
