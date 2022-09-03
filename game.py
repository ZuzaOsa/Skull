from typing import Counter, List

from strategy import Strategy
from player import Player
from board import Board

from utils import Phase
from utils import Move
from utils import Card
from utils import Reveal_i
from utils import POINTS_TO_WIN


class Game:
    def __init__(self, strategies: List[Strategy], verbose: bool = True) -> None:
        self.player_num = len(strategies)
        self.players = [Player(idx=i, strategy=strategy)
                        for i, strategy in enumerate(strategies)]

        self.starting_player = self.players[0]
        self.verbose = verbose  # Show all the moves of all the players
        self.winner = None
        self.phase = None
        self.bets = [Move.Bet_0] * self.player_num
        self.revealed = [0] * self.player_num

    def round(self) -> None:
        # Putting cards phase
        self.phase = Phase.Put_Cards
        moving_player = self.starting_player
        while self.phase == Phase.Put_Cards:
            self.print_board()
            if moving_player.active:
                move = moving_player.strategy.get_move(self.get_board(moving_player))
                if self.verbose:
                    print(f"------\nMOVE: {move}\n------\n")
                if move == Move.Bet:
                    self.phase = Phase.Bet
                else:
                    moving_player.put_card(move)
                    moving_player = self.next_player(moving_player)
            else:
                moving_player = self.next_player(moving_player)

        # Betting phase
        while self.phase == Phase.Bet:
            self.print_board()
            if self.bets[moving_player.idx] != Move.Pass:
                move = moving_player.strategy.get_move(self.get_board(moving_player))
                if self.verbose:
                    print(f"------\nMOVE: {move}\n------\n")
                self.bets[moving_player.idx] = move
            if self.end_licitation:
                self.phase = Phase.Reveal
            else:
                moving_player = self.next_player(moving_player)

        # Reveal phase
        declaration = self.get_board().highest_bet
        while self.phase == Phase.Reveal:
            self.print_board()
            if self.revealed[moving_player.idx] < len(moving_player.stack):
                card = moving_player.stack[-self.revealed[moving_player.idx]-1]
                if card == Card.Skull:
                    self.phase = Phase.Discard
                else:
                    self.revealed[moving_player.idx] += 1
                    declaration -= 1
            else:
                if declaration <= 0:
                    moving_player.add_point()
                    self.phase = Phase.Put_Cards
                else:
                    move = Reveal_i.index(moving_player.strategy.get_move(self.get_board(moving_player)))
                    if self.verbose:
                        print(f"------\nMOVE: {move}\n------\n")
                    card = self.players[move].stack[-self.revealed[move]-1]
                    if card == Card.Skull:
                        moving_player.restart()
                        moving_player.lose_card()
                        self.phase = Phase.Put_Cards
                    else:
                        self.revealed[move] += 1
                        declaration -= 1

        # Optional discard phase
        if self.phase == Phase.Discard:
            self.print_board()
            moving_player.restart()
            self.revealed = [0] * self.player_num
            move = moving_player.strategy.get_move(self.get_board(moving_player))
            if self.verbose:
                print(f"------\nMOVE: {move}\n------\n")
            if move == Move.Discard_Rose:
                moving_player.discard(Card.Rose)
            else:
                moving_player.discard(Card.Skull)
        self.starting_player = moving_player
        self.restart()

    def restart(self) -> None:
        self.check_winner()
        for player in self.players:
            player.restart()
            if player.active:
                self.bets[player.idx] = Move.Bet_0
            else:
                self.bets[player.idx] = Move.Pass
        self.revealed = [0] * self.player_num

    def check_winner(self) -> None:
        # Checks if game has finished. If game has finished, sets self.winner
        if POINTS_TO_WIN in self.points:
            winner_idx = self.points.index(POINTS_TO_WIN)
            self.winner = self.players[winner_idx]

        if self.active_player_mask.count(1) == 1:
            self.winner_idx = self.active_player_mask.index(1)
            self.winner = self.players[self.winner_idx]

    def next_player(self, player: Player) -> Player:
        # Helper function, returns the next player to play
        next_player_idx = (player.idx + 1) % self.player_num
        next_player = self.players[next_player_idx]
        return next_player

    def get_board(self, player: Player=None) -> Board:
        """ Get current game state from the perspective of a given player i.e.
            the game state include information only known to the given player
            such as which cards the player has in the hand and/or board.

            If player is None then the board include information only known
            to all the players.
        """
        if player is not None:
            idx = player.idx
        else:
            idx = -1
        player_stacks = []
        player_hands = []
        for i in self.players:
            if i.idx == idx:
                player_hands.append(Counter({Card.Rose: i.hand[Card.Rose], Card.Skull: i.hand[Card.Skull]}))
                player_stacks.append([])
                for card in i.stack:
                    player_stacks[i.idx].append(card)
            else:
                cards_board = len(i.stack)
                cards_hand = i.hand.total()
                player_stacks.append([Card.Unknown] * cards_board)
                player_hands.append(Counter({Card.Unknown: cards_hand}))
            for j in range(1, self.revealed[i.idx] + 1):
                player_stacks[i.idx][-j] = i.stack[-j]
        return Board(self.phase, self.points, self.active_player_mask, self.bets, player_stacks, player_hands, idx)

    def print_board(self):
        print(self.get_board())

    @property
    def points(self):
        return [player.points for player in self.players]

    @property
    def active_player_mask(self):
        return [player.active for player in self.players]

    @property
    def finished(self):
        return self.winner is not None

    @property
    def end_licitation(self):
        if self.bets.count(Move.Pass) == self.player_num - 1:
            return True
        board = self.get_board()
        return board.highest_bet == board.cards_board_num