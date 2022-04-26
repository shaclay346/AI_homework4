from random import randint
from hand_of_the_king import getvalidmoves
import pdb

# method to createe a copy of the board, cards and banners lists


def createCopies(board, cards, banners):
    copy = []

    for i in range(len(board)):
        copy.append(board[i])

    copyCards = []
    # copy the cards
    for i in range(len(cards)):
        copyCards.append(cards[i])

    copyBanners = []
    # copy the banners
    for i in range(len(banners)):
        copyBanners.append(banners[i])

    return copy, copyCards, copyBanners


def get_computer_move(board, cards, banners, turn):
    result = createCopies(board, cards, banners)

    # this should be ok, since I'm overwriting
    # the saved address of those things, to the new addresses of what was returned
    board = result[0]
    cards = result[1]
    banners = result[2]
    minimax(board, cards, bannners, player)


def simulateMove(board, cards, banner, move, player):
    # so wherever the 1 card is and wherever it moves to, if anything at a position +-6 from where one card was to where it will go
    # needs to be set to 0
    # cards = gui.items[:-1]
    x1 = board.index(1)  # index of the 1-card on the board
    # print(f'moving from {x1} to {x}')

    # Remove captured cards from board
    # d = gui.width + 100  # distance to move cards
    color = board[x]  # color of the main captured card
    cards[x].move(d, 0)
    board[x] = 1  # the 1-card moves here
    collection[color - 2] += 1
    if abs(x - x1) < COLS:  # move is either left or right
        dx = (x - x1) * (CARD_SIZE + MARGIN)
        dy = 0
        if x < x1:  # left
            possible = range(x + 1, x1)
        else:  # right
            possible = range(x1 + 1, x)
    else:  # move is either up or down
        dx = 0
        dy = ((x - x1) // COLS) * (CARD_SIZE + MARGIN)
        if x < x1:  # up
            possible = range(x + COLS, x1, COLS)
        else:  # down
            possible = range(x1 + COLS, x, COLS)

    for i in possible:
        if board[i] == color:
            cards[i].move(d, 0)
            board[i] = 0  # there is no card in this position anymore
            collection[color - 2] += 1

    # Move the 1-card to the correct position
    cards[x0].move(dx, dy)
    board[x1] = 0

    # Check to see if current player should capture a banner
    if cards[turn][color - 2] >= cards[abs(turn - 1)][color - 2]:
        # add the banner to the player's collection
        banners[turn][color - 2] = 1
        banners[abs(turn - 1)][color - 2] = 0


def minimax(board, cards, bannners, player):
    '''Returns the best move from a given state in the game for a specific player.'''
    result = createCopies(board, cards, banners)
    board = result[0]
    cards = result[1]
    banners = result[2]

    moves = getvalidmoves(board)
    best = moves[0]

    value = minvalue(board, cards, player, best)
    for move in moves[1:]:
        v = minvalue(board, player, move)
        if v > value:
            best = move
            value = v

    return best


def minvalue(board, cards, banners, player, move):
    '''Returns the minimum utility available from a player taking an move on the current board.'''
    # Simulate the move of the current player
    result = createCopies(board, cards, banners)
    board = result[0]
    cards = result[1]
    banners = result[2]

    # simulate the move on the copies of the game items
    temp = simulateMove(board, cards, banner, move, player)
    nextplayer = math.abs(player-1)

    # Check if we are in a terminal state
    moves = getvalidmoves(board)
    if len(moves) == 0:
        return 1

    # If not, find minimum utility of possible moves
    value = float('inf')
    for move in moves:
        value = min(value, maxvalue(board, cards, banners, nextplayer, move))

    return value


def maxvalue(board, cards, banners, player, move):
    '''Returns the maximum utility available from a player taking an move on the current board.'''
    # Simulate the move of the current player
    result = createCopies(board, cards, banners)
    board = result[0]
    cards = result[1]
    banners = result[2]

    simulateMove(board, cards, banner, move, player)
    nextplayer = math.abs(player-1)

    # Check if we are in a terminal state
    moves = getvalidmoves(board)
    if len(moves) == 0:
        return -1

    # If not, find maximum utility of possible moves
    value = float('-inf')
    for move in moves:
        value = max(value, minvalue(board, cards, banners, nextplayer, move))

    return value
