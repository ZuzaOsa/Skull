from typing import List

from strategy import Strategy
from player import Player
from board import Board

from utils import Phase
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

    def round(self) -> None:
        # Putting cards phase
        self.phase = Phase.Put_Cards
        # TODO

        # Betting phase
        self.phase = Phase.Bet
        # TODO

        # Reveal phase
        self.phase = Phase.Reveal
        # TODO

        # Optional discard phase
        self.phase = Phase.Discard
        # TODO

        self.restart()

    def restart(self) -> None:
        self.check_winner()
        for player in self.players:
            player.restart()

    def check_winner(self) -> None:
        # Checks if game has finished. If game has finished, sets self.winner
        if POINTS_TO_WIN in self.points:
            winner_idx = self.points.index(POINTS_TO_WIN)
            self.winner = self.players[winner_idx]

        if self.active_player_mask.count(1) == 1:
            self.winner_idx = self.active_player_mask.index(1)
            self.winner = self.players[winner_idx]

    def next_player(self, player: Player) -> Player:
        # Helper function, returns the next player to play
        next_player_idx = (player.idx + 1) % self.player_num
        next_player = self.players[next_player_idx]
        return next_player

    def get_board(self, player=None) -> Board:
        """ Get current game state from the perspective of a given player i.e.
            the game state include information only known to the given player
            such as which cards the player has in the hand and/or board.

            If player is None then the board include information only known
            to all the players.
        """
        # TODO
        raise NotImplementedError

    @property
    def points(self):
        return [player.points for player in self.players]

    @property
    def active_player_mask(self):
        return [player.active for player in self.players]

    @property
    def finished(self):
        return self.winner is not None
