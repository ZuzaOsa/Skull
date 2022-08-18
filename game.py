import random
from typing import List


class Player(object):
    def __init__(self, id):
        self.hand_roses = 3
        self.hand_skulls = 1
        self.id = id
        self.cards_board = []

    def put_card(self, move):
        if move == "R":
            self.hand_roses -= 1
            self.cards_board.append(0)
        else:
            self.hand_skulls -= 1
            self.cards_board.append(1)

    def return_card(self):
        if self.cards_board[-1]:
            self.hand_skulls += 1
        else:
            self.hand_roses += 1
        self.cards_board.pop()

    def discard_card(self, card):
        if card:
            self.hand_skulls = 0
        else:
            self.hand_roses -= 1

    def lose_card(self):
        card = random.randint(0, self.hand_roses + self.hand_skulls - 1)
        if card < self.hand_roses:
            self.hand_roses -= 1
            return 0
        else:
            self.hand_skulls = 0
            return 1


class Board(object):
    def __init__(self, player_num):
        self.player_num = player_num
        self.cards_hand = [4] * player_num
        self.cards_board = [0] * player_num
        self.points = [0] * player_num
        self.card_count = 0

    def discard_card(self, player_id):
        self.cards_hand[player_id] -= 1

    def display(self):
        print("BOARD")
        for i in range(0, self.player_num):
            print(str(i + 1), end=" ")
        print()
        for i in range(0, self.player_num):
            if self.points[i]:
                print("x", end=" ")
            else:
                print(" ", end=" ")
        print()
        for i in range(0, 3):
            for j in range(0, self.player_num):
                if self.cards_board[j] > i:
                    print("#", end=" ")
                else:
                    print(" ", end=" ")
            print()

    def put_card(self, player_id):
        self.cards_hand[player_id] -= 1
        self.cards_board[player_id] += 1
        self.card_count += 1

    def return_card(self, player_id):
        self.cards_board[player_id] -= 1
        self.cards_hand[player_id] += 1


class Strategy(object):
    def __init__(self, player_num):
        self.player_num = player_num

    def make_move():
        pass

    def licitate():
        pass

    def discard():
        pass

    def reveal():
        pass

    def legal_move(self, player: Player):
        legal_moves = []
        if player.hand_roses:
            legal_moves.append("R")
        if player.hand_skulls:
            legal_moves.append("S")
        if player.cards_board:
            legal_moves.append("L")
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

    def legal_discard(self, player: Player):
        legal_discards = ["S"]
        if player.hand_roses:
            legal_discards.append("R")
        return legal_discards


class ManualStrategy(Strategy):
    def make_move(self, board: Board, player: Player):
        board.display()
        legal_moves = self.legal_move(player)
        move = input(f"Player number {player.id + 1} moves: ")
        while move not in legal_moves:
            move = input("This is not a legal move. New move: ")
        return move

    def licitate(self, player: Player, board: Board, start, highest_bet):
        legal_bets = self.legal_bet(board, start, highest_bet)
        move = int(input(f"Declaration of player number {player.id + 1}: "))
        while move not in legal_bets:
            move = int(input("This is not a legal bet. New bet: "))
        return move

    def discard(self, player: Player, board: Board):
        legal_discards = self.legal_discard(player)
        move = input(f"Player number {player.id + 1} discard a card: ")
        while move not in legal_discards:
            move = input("This is not a legal discard. New discard: ")
        if move == "R":
            return 0
        else:
            return 1

    def reveal(self, player: Player, board: Board):
        legal_reveals = self.legal_reveal(board)
        print(legal_reveals)
        move = int(input("Chose card to reveal: ")) + 1
        while move not in legal_reveals:
            move = int(input("This is not a legal reveal. New reveal: ")) - 1
        return move


class RandomStrategy(Strategy):
    def make_move(self, board: Board, player: Player):
        board.display()
        legal_moves = self.legal_move(player)
        move = random.choice(legal_moves)
        print(f"Player number {player.id + 1} moves: {move}")
        return move

    def licitate(self, player: Player, board: Board, start, highest_bet):
        legal_bets = self.legal_bet(board, start, highest_bet)
        move = random.choice(legal_bets)
        print(f"Declaration of player number {player.id + 1}: {move}")
        return move

    def discard(self, player: Player, board: Board):
        legal_discards = self.legal_discard(player)
        move = random.choice(legal_discards)
        print(f"Player number {player.id + 1} discard a card: {move}")
        if move == "R":
            return 0
        else:
            return 1

    def reveal(self, player: Player, board: Board):
        legal_reveals = self.legal_reveal(board)
        move = random.choice(legal_reveals)
        print(f"Chose card to reveal: {move + 1}")
        return move


class Game(object):

    def __init__(self, player_num, strategies: List[Strategy]):
        self.player_num = player_num
        self.strategies = strategies
        self.board = Board(player_num)
        self.winner = -1
        self.players = []
        self.starting_player = 0
        self.active = [1] * player_num
        for i in range(0, player_num):
            self.players.append(Player(id=i))

    def restart(self):
        if 2 in self.board.points:
            self.winner = self.board.points.index(2)
            return
        if self.active.count(1) == 1:
            self.winner = self.active.index(1)
            return
        self.board.card_count = 0
        for i in range(0, self.player_num):
            while self.players[i].cards_board:
                self.players[i].return_card()
                self.board.return_card(i)

    def show(self, player: Player, bet):
        self.starting_player = player.id
        print(f"Player number {player.id + 1} won the licitation, let's reveal your cards first")
        while player.cards_board:
            if player.cards_board[-1]:
                print("You have a skull on board, discard a card")
                self.restart()
                move = self.strategies[player.id].discard(player, self.board)
                self.board.discard_card(player.id)
                self.players[player.id].discard_card(move)
                if not self.board.cards_hand[player.id]:
                    self.active[player.id] = 0
                return
            else:
                print("It's a rose")
                self.players[player.id].return_card()
                self.board.return_card(player.id)
                bet -= 1
        if bet <= 0:
            print("Congratulations, you scored a point")
            self.board.points[player.id] += 1
            return
        self.board.display()
        while bet > 0:
            move = self.strategies[player.id].reveal(player, self.board)
            if self.players[move].cards_board[-1]:
                self.restart()
                print("It's a skull, you lose a card")
                self.restart()
                card = self.players[player.id].lose_card()
                self.board.discard_card(player.id)
                if not self.board.cards_hand[player.id]:
                    self.active[player.id] = 0
                if card:
                    print("You lost a skull")
                else:
                    print("You lost a rose")
                return
            else:
                print("It's a rose!")
                bet -= 1
                self.players[move].return_card()
                self.board.return_card(move)
        print("Congratulations, you scored a point")
        self.board.points[player.id] += 1

    def licitation(self, moving_player, board: Board):
        bets = []
        highestBet = 0
        for i in range(0, self.player_num):
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

    def make_turn(self, player_id):
        if self.active[player_id] == 0:
            return 1
        move = self.strategies[player_id].make_move(self.board, self.players[player_id])
        if move == "R" or move == "S":
            self.board.put_card(player_id)
            self.players[player_id].put_card(move)
            return 1
        else:
            self.licitation(player_id, self.board)
            return 0

    def round(self):
        moving_player = self.starting_player
        while self.make_turn(moving_player):
            moving_player = (moving_player + 1) % self.player_num
        self.restart()


all_players = int(input("Number of players: "))

while all_players < 2:
    all_players = int(input("There has to be at least two players: "))

ai_players = int(input("Number of AI players: "))

while ai_players < 0 or ai_players > all_players:
    ai_players = int(input(f"Number of AI players must be between 0 and {all_players}: "))

strategy = [ManualStrategy(player_num=all_players)] * (all_players - ai_players) + [RandomStrategy(player_num=all_players)] * ai_players

game = Game(all_players, strategy)

while game.winner == -1:
    game.round()

print(f"The winner is player number {game.winner + 1}")
