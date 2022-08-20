import random

from game import Game
from strategy import RandomStrategy
from strategy import ManualStrategy


def main():
    #all_players = int(input("Number of players: "))
    all_players = 3

    while all_players < 2:
        all_players = int(input("There has to be at least two players: "))

    #ai_players = int(input("Number of AI players: "))
    ai_players = 2

    while ai_players < 0 or ai_players > all_players:
        ai_players = int(input(f"Number of AI players must be between 0 and {all_players}: "))

    #visible = int(input("Do you want to see AI moves?: "))
    visible = 0

    strategies = [ManualStrategy(player_num=all_players, visible_moves=visible)] * (all_players - ai_players) + [RandomStrategy(player_num=all_players, visible_moves=visible)] * ai_players
    random.shuffle(strategies)

    game = Game(strategies)

    while game.winner is None:
        game.round()

    print(f"The winner is player number {game.winner}")


if __name__ == "__main__":
    main()
