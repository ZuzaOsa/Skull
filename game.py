players = int(input("Number of players: "))

board = [] #cards on the table
hand = []
points = []
active = [] #does player still have cards

for i in range(0, players):
    board.append([])
    points.append(0)
    hand[i].append([0, 0, 0, 1])
    active.append(1)

def returnCards(player):
    for i in board[player]:
        hand[player].append(i)
    board[player] = []

def licitation(player):
    pass

def makeMove(player):
    move = input("Move of player number " + str(i + 1) + ": ")
    if move == "R":
        if 0 in hand[player]:
            hand[player].remove(0)
            board[player].append(0)
        else:
            print("You do not have a rose")
            makeMove(player)
    elif move == "S":
        if 1 in hand[player]:
            hand[player].remove(1)
            board[player].append(1)
        else:
            print("You do not have a skull")
            makeMove(player)
    elif move == "L":
        if len(board[player]) == 0:
            print("Put a card first")
            makeMove(player)
        else:
            licitation(player)



def newRound():
    for i in range(0, players):
        returnCards(i)
    for i in range(0, players):
        if active[i] == 0:
            continue
        makeMove(i)


winner = -1

while winner == -1:
    newRound()
