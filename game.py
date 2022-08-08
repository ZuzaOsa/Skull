from random import randint

players = int(input("Number of players: "))

board = [] #cards on the table
hand = []
points = []
active = [] #does player still have cards
roundEnd = 0
highestBet = 0
movingPlayer = 0
cardsNum = 0

for i in range(0, players):
    board.append([])
    points.append(0)
    hand.append([0, 0, 0, 1])
    active.append(1)

def returnCards(player):
    global board
    for i in board[player]:
        hand[player].append(i)
    board[player] = []

def displayBoard():
    print("Number of cards")
    for i in range(0, players):
        print("Player number " + str(i + 1) + " has " + str(len(board[i])))

def show(player, rosesNum):
    global movingPlayer
    movingPlayer = player
    print("Player number " + str(player + 1) + " show " + str(rosesNum) + " roses!")
    if 1 in board[player]:
        returnCards(player)
        if len(hand[player]) == 1:
            print("You lose a skull")
            hand[player].pop()
            return
        choice = input("You have a skull, which card you want to lose?")
        while choice != "S" and choice != "R":
            choice = input("You have to chose rose or skull: ")
        if choice == "S":
            hand[player].remove(1)
        else:
            hand[player].remove(0)
    else:
        rosesNum -= len(board[player])
        returnCards(player)
        if rosesNum > 0:
            print("You need to reveal " + str(rosesNum) + " roses")
            displayBoard()
        while rosesNum > 0:
            move = int(input("Chose card to reveal: ")) - 1
            if len(board[move]) == 0:
                print("This player does not have unrevealed cards")
            else:
                if board[move][-1] == 0:
                    print("It's a rose")
                    rosesNum -= 1
                    hand[move].append(0)
                    board[move].pop()
                else:
                    print("It's a skull, you lose a card")
                    rnd = randint(0, len(hand[player]) - 1)
                    if hand[player][rnd] == 0:
                        print("You lose a rose")
                    else:
                        print("You lose a skull")
                    hand[player].pop(rnd)
                    return
        points[player] += 1
        print("Congratulations, you scored a point!")
        print(points)          

def licitation(player):
    global highestBet
    bets = []
    for i in range(0, players):
        bets.append(0)
    highestBet = 0
    bets[player] = makeBet(player)
    while bets[player] < 1:
        print("You started licitation, bet at least 1 rose")
        bets[player] = makeBet(player)
    for i in range(player + 1, players + player):
        if active[i % players] == 0:
            bets.append(-1)
            continue
        bets[i % players] = makeBet(i % players)
    while bets.count(-1) < players - 1:
        if bets[player] != -1:
            bets[player] = makeBet(player)
        player = (player + 1) % players
    show(bets.index(highestBet), highestBet)

def makeBet(player):
    global highestBet
    global cardsNum
    print(cardsNum)
    bet = int(input("Declaration of player number " + str(player + 1) + ": "))
    if bet == -1:
        return -1
    elif bet <= highestBet:
        print("You need to say at least " + str(highestBet + 1) + " or pass")
        return makeBet(player)
    elif bet > cardsNum:
        print("You can't licitate more roses than cards on the table")
        return makeBet(player)
    else:
        highestBet = bet
        return bet

def makeMove(player):
    global cardsNum
    move = input("Move of player number " + str(player + 1) + ": ")
    if move == "R":
        if 0 in hand[player]:
            hand[player].remove(0)
            board[player].append(0)
            cardsNum += 1
        else:
            print("You do not have a rose")
            makeMove(player)
    elif move == "S":
        if 1 in hand[player]:
            hand[player].remove(1)
            board[player].append(1)
            cardsNum += 1
        else:
            print("You do not have a skull")
            makeMove(player)
    elif move == "L":
        if len(board[player]) == 0:
            print("Put a card first")
            makeMove(player)
        else:
            global roundEnd
            roundEnd = 1
            licitation(player)
    else:
        print("This is not a valid move")
        makeMove(player)


def newRound():
    print("New round starts")
    global roundEnd
    global cardsNum
    roundEnd = 0
    cardsNum = 0
    a = movingPlayer
    for i in range(0, players):
        returnCards(i)
    while roundEnd == 0:
        if active[a] == 0:
            a = (a + 1) % players
            continue
        makeMove(a)
        a = (a + 1) % players


winner = -1

while winner == -1:
    newRound()
    for i in range(0, players):
        if len(hand[i]) == 0:
            active[i] = 0
    if 2 in points:
        winner = points.index(2)
    if active.count(1) == 1:
        winner = active.index(1)

print("The winner is player number " + str(winner + 1))