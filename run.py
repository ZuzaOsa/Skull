import random

from game import Game
from strategy import ManualStrategy
from strategy import RandomStrategy

def main():
    num_players = int(input("Number of players: "))
    while num_players < 2:
        num_players = int(input("There has to be at least two players: "))

    num_ai_players = int(input("Number of AI players: "))
    while num_ai_players < 0 or num_ai_players > num_players:
        num_ai_players = int(input(f"Number of AI players must be between 0 and {num_players}: "))

    #verbose = int(input("Do you want to see AI moves?: "))
    verbose = 1
    # TODO Display moves only if verbose == 1

    strategies = [ManualStrategy()] * (num_players - num_ai_players) + [RandomStrategy()] * num_ai_players
    random.shuffle(strategies)

    game = Game(strategies, verbose=verbose)

    while not game.finished:
        game.round()

    print(f"The winner is {game.winner}")

if __name__ == "__main__":
    main()
