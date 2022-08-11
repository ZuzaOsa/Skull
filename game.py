import random

players = int(input("Number of players: "))

while players < 2:
    players = int(input("There has to be at least two players: \r"))

playersAI = int(input("Number of AI players: "))

while playersAI < 0 or playersAI > players:
    playersAI = int(input("Number of AI players must be between 0 and " + str(players) + ": "))

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
    global hand
    for i in board[player]:
        hand[player].append(i)
    board[player] = []

def displayBoard():
    for i in range(0, players):
        print(str(i + 1), end = ' ')
    print()
    for i in range(0, players):
        if points[i] == 0:
            print(' ', end = ' ')
        else:
            print('x', end = ' ')
    print()
    for i in range(0, 3):
        for j in range(0, players):
            if len(board[j]) > i:
                print("#", end = ' ')
            else:
                print(" ", end = ' ')
        print()

def show(player, rosesNum):
    global movingPlayer
    global hand
    movingPlayer = player
    print("Player number " + str(player + 1) + " won the licitation!")
    if 1 in board[player]:
        returnCards(player)
        if len(hand[player]) == 1:
            print("You lose a skull")
            hand[player].pop()
            return
        if (player < playersAI):
            legal = ["R", "S"]
            choice = random.choice(legal)
            print("You have a skull on the table, which card you want to lose? " + choice)
        else: 
            choice = input("You have a skull on the table, which card you want to lose? ")
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
            if rosesNum == 1:
                print("You need to reveal 1 rose")
            else:
                print("You need to reveal " + str(rosesNum) + " roses")
            displayBoard()
        while rosesNum > 0:
            if player < playersAI:
                legal = []
                for i in range(0, players):
                    if len(board[i]) != 0:
                        legal.append(i)
                move = random.choice(legal)
                print("Chose card to reveal: " + str(move + 1))
            else:
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
                    rnd = random.randint(0, len(hand[player]) - 1)
                    if hand[player][rnd] == 0:
                        print("You lose a rose")
                    else:
                        print("You lose a skull")
                    hand[player].pop(rnd)
                    return
        points[player] += 1
        print("Congratulations, you scored a point!")
        #print(points)          

def licitation(player):
    global highestBet
    global cardsNum
    global movingPlayer
    movingPlayer = player
    bets = []
    for i in range(0, players):
        bets.append(0)
    highestBet = 0
    bets[player] = makeBet(player)
    movingPlayer = -1
    if highestBet == cardsNum:
        show(player, cardsNum)
        return
    for i in range(player + 1, players + player):
        if active[i % players] == 0:
            bets[i % players] == -1
            continue
        bets[i % players] = makeBet(i % players)
        if highestBet == cardsNum:
            show(i % players, cardsNum)
            return
    while bets.count(-1) < players - 1:
        if bets[player] != -1:
            bets[player] = makeBet(player)
            if highestBet == cardsNum:
                show(player, cardsNum)
                return
        player = (player + 1) % players
    show(bets.index(highestBet), highestBet)

def makeBet(player):
    global highestBet
    global cardsNum
    global movingPlayer
    if player < playersAI:
        legal = []
        if player != movingPlayer:
            legal.append(-1)
        for i in range(highestBet + 1, cardsNum + 1):
            legal.append(i)
        bet = random.choice(legal)
        print("Declaration of player number " + str(player + 1) + ": " + str(bet))
    else:
        bet = int(input("Declaration of player number " + str(player + 1) + ": "))
    if player == movingPlayer:
        if (bet < 0):
            print("You started licitation, bet at least one rose")
            return makeBet(player)
        highestBet = bet
        return bet
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
    if (player < playersAI):
        legal = []
        if 0 in hand[player]:
            legal.append("R")
        if 1 in hand[player]:
            legal.append("S")
        if len(board[player]) != 0:
            legal.append("L")
        move = random.choice(legal)
        print("Move of player number " + str(player + 1) + ": " + move)
    else:
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
    while roundEnd == 0:
        if active[a] == 0:
            a = (a + 1) % players
            continue
        makeMove(a)
        if roundEnd == 0:
            displayBoard()
        a = (a + 1) % players


winner = -1

while winner == -1:
    newRound()
    for i in range(0, players):
        returnCards(i)
        if len(hand[i]) == 0:
            active[i] = 0
    if 2 in points:
        winner = points.index(2)
    if active.count(1) == 1:
        winner = active.index(1)

print("The winner is player number " + str(winner + 1) + "! ")