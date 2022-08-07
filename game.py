players = int(input("Number of players: "))

board = [] #cards on the table
hand = []
points = []
active = [] #does player still have cards
bets = []
roundEnd = 0
highestBet = 0

for i in range(0, players):
    board.append([])
    points.append(0)
    hand.append([0, 0, 0, 1])
    active.append(1)
    bets.append(0)

def returnCards(player):
    for i in board[player]:
        hand[player].append(i)
    board[player] = []

def show(player, rosesNum):
    print("Player number " + str(player + 1) + " show " + str(rosesNum) + " roses!")

def licitation(player):
    print("Licitation started")
    bets = []
    highestBet = 0
    bets[player] = makeBet(player)
    while bets[player] == -1:
        print("You started licitation, bet at least 1 rose")
        bets[player] = makeBet(player)
    for i in range(player + 1, players + player):
        if active[i % players] == 0:
            bets.append(-1)
            continue
        bets[i % player] = makeBet(i % players)
    while bets.count(-1) < players - 1:
        if bets[player] != -1:
            bets[player] = makeBet(player)
        player = (player + 1) % players
    show(bets.index(highestBet), highestBet)

def makeBet(player):
    bet = int(input("Declaration od player number " + str(player + 1) + ": "))
    if bet == -1:
        return -1
    elif bet <= highestBet:
        print("You need to say at least " + str(highestBet + 1) + " or pass")
        makeBet(player)
    else:
        highestBet = bet
        return bet

def makeMove(player):
    print(board)
    move = input("Move of player number " + str(player + 1) + ": ")
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
            roundEnd = 1
            licitation(player)
    else:
        print("This is not a valid move")
        makeMove(player)




def newRound():
    roundEnd = 0
    a = 0
    for i in range(0, players):
        returnCards(i)
    while roundEnd == 0:
        if active[a] == 0:
            continue
        makeMove(a)
        a = (a + 1) % players


winner = -1

while winner == -1:
    newRound()
