import random

from abc import abstractmethod

from typing import List

from board import Board
from utils import Move


class Strategy(object):
    def __init__(self, player_num, visible_moves):
        self.player_num = player_num
        self.visible_moves = visible_moves

    @abstractmethod
    def make_move():
        raise NotImplementedError

    @abstractmethod
    def licitate():
        raise NotImplementedError

    @abstractmethod
    def discard():
        raise NotImplementedError

    @abstractmethod
    def reveal():
        raise NotImplementedError

    def get_legal_moves(self, board: Board) -> List[Move]:
        active_player_idx = board.active_player_idx
        legal_moves = [Move.Bet]
        print(board.active_player_hand_roses)
        print(board.active_player_hand_skulls)
        board.display()
        if board.active_player_hand_roses > 0:
            legal_moves.append(Move.Rose)
        if board.active_player_hand_skulls > 0:
            legal_moves.append(Move.Skull)
        return legal_moves

    def legal_bet(self, board: Board, start, highest_bet):
        legal_bets = []
        for i in range(highest_bet + 1, board.card_count + 1):
            legal_bets.append(i)
        if not start:
            legal_bets.append(-1)
        return legal_bets

    def legal_reveal(self, board: Board):
        legal_reveals = []
        for i in range(0, self.player_num):
            if board.cards_board[i]:
                legal_reveals.append(i)
        return legal_reveals

    def legal_discard(self):
        legal_discards = ["S"]
        if player.hand_roses:
            legal_discards.append("R")
        return legal_discards


class ManualStrategy(Strategy):
    def make_move(self, board: Board):
        board.display()
        legal_moves = self.get_legal_moves(board)
        move = self.get_move()
        while move not in legal_moves:
            print("{move} is not a legal move.")
            move = self.get_move()
        return move

    @staticmethod
    def get_move():
        raw_move = input(f"Input move: ")
        if raw_move == "r":
            move = Move.Rose
        elif raw_move == "s":
            move = Move.Skull
        else:
            raise ValueError('Invalid move')
        return move

    def licitate(self, board: Board, start, highest_bet):
        legal_bets = self.legal_bet(board, start, highest_bet)
        move = int(input(f"Declaration of {player}: "))
        while move not in legal_bets:
            move = int(input("This is not a legal bet. New bet: "))
        return move

    def discard(self, board: Board):
        legal_discards = self.legal_discard(player)
        move = input(f"{player} discard a card: ")
        while move not in legal_discards:
            move = input("This is not a legal discard. New discard: ")
        if move == "R":
            return 0
        else:
            return 1

    def reveal(self, board: Board):
        legal_reveals = self.legal_reveal(board)
        print(legal_reveals)
        move = int(input("Chose card to reveal: ")) + 1
        while move not in legal_reveals:
            move = int(input("This is not a legal reveal. New reveal: ")) - 1
        return move


class RandomStrategy(Strategy):
    def make_move(self, board: Board):
        legal_moves = self.get_legal_moves(board)
        move = random.choice(legal_moves)
        if self.visible_moves:
            print(f"{player} moves: {move}")
        return move

    def licitate(self, board: Board, start, highest_bet):
        legal_bets = self.legal_bet(board, start, highest_bet)
        move = random.choice(legal_bets)
        print(f"Declaration of {player}: {move}")
        return move

    def discard(self, board: Board):
        legal_discards = self.legal_discard(player)
        move = random.choice(legal_discards)
        if self.visible_moves:
            print(f"{player} discard a card: {move}")
        if move == "R":
            return 0
        else:
            return 1

    def reveal(self, board: Board):
        legal_reveals = self.legal_reveal(board)
        move = random.choice(legal_reveals)
        print(f"Chose card to reveal: {move + 1}")
        return move
