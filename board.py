class Board:
    def __init__(self,
                 player_num,
                 active_player_mask,
                 active_player_idx,
                 points,
                 cards_hand,
                 cards_board,
                 active_player_board=None,
                 active_player_hand_roses=None,
                 active_player_hand_skulls=None,
                 ):
        print(active_player_hand_roses)
        self.player_num = player_num
        self.active_player_mask = active_player_mask
        self.active_player_idx = active_player_idx
        self.points = points
        self.cards_hand = cards_hand
        self.cards_board = cards_board
        self.active_player_board = active_player_board,
        self.active_player_hand_roses = active_player_hand_roses,
        self.active_player_hand_skulls = active_player_hand_skulls,

    def display(self):
        print("BOARD")
        # Mark active player
        for i in range(self.player_num):
            print("A" if i == self.active_player_idx else " ", end=" ")
        print()

        print("-" * self.player_num * 2)

        # Print number of cards in hand
        for i in range(self.player_num):
            print(self.cards_hand[i], end=" ")
        print()

        print("-" * self.player_num * 2)

        # Print players
        for i in range(self.player_num):
            print(str(i + 1) if self.active_player_mask[i] else "-", end=" ")
        print()

        # Print points
        for i in range(self.player_num):
            if self.points[i]:
                print("x", end=" ")
            else:
                print(" ", end=" ")
        print()

        for i in range(4):
            for j in range(self.player_num):
                if self.cards_board[j] > i:
                    print("#", end=" ")
                else:
                    print(" ", end=" ")
            print()
