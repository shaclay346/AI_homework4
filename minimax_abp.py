from random import randint
from hand_of_the_king import getvalidmoves
import pdb
import math
from copy import copy, deepcopy

# method to createe a copy of the board, cards and banners lists


def createCopies(board, cards, banners):
    copyBoard = []

    for i in range(len(board)):
        copyBoard.append(board[i])

    # copy the cards
    # copy.deepcopy(x)
    copyCards = deepcopy(cards)
    # for i in range(len(cards)):
    #     for j in range(len(cards[i])):
    #         copyCards[i][j] = cards[i][j]

    copyBanners = deepcopy(banners)
    # copy the banners
    # for i in range(len(banners)):
    #     for j in range(len(banners[i])):
    #         copyBanners[i][j] = banners[i][j]

    return copyBoard, copyCards, copyBanners


def get_computer_move(board, cards, banners, turn):
    result = createCopies(board, cards, banners)

    # this should be ok, since I'm overwriting
    # the saved address of those things, to the new addresses of what was returned
    board = result[0]
    cards = result[1]
    banners = result[2]
    return minimax(board, cards, banners, turn)


# x is move
# collection is the 1d array that comes from the cards
def simulateMove(board, cards, banners, x, player):
    # so wherever the 1 card is and wherever it moves to, if anything at a position +-6 from where one card was to where it will go
    # needs to be set to 0
    # cards = gui.items[:-1]
    collection = cards[player]
    turn = player
    # x0 = board.index(1)
    x1 = board.index(1)  # index of the 1-card on the board
    # print(f'moving from {x1} to {x}')

    # Remove captured cards from board
    # d = gui.width + 100  # distance to move cards
    color = board[x]  # color of the main captured card
    # cards[x].move(d, 0)
    board[x] = 1  # the 1-card moves here
    collection[color - 2] += 1
    if abs(x - x1) < 4:  # move is either left or right
        if x < x1:  # left
            possible = range(x + 1, x1)
        else:  # right
            possible = range(x1 + 1, x)
    else:  # move is either up or down
        if x < x1:  # up
            possible = range(x + 6, x1, 6)
        else:  # down
            possible = range(x1 + 6, x, 6)

    for i in possible:
        if board[i] == color:
            # cards[i].move(d, 0)
            board[i] = 0  # there is no card in this position anymore
            collection[color - 2] += 1

    # Move the 1-card to the correct position
    # don't even know if I need this or not, or any of the dx, dy shit

    board[x1] = 0

    # pdb.set_trace()

    # Check to see if current player should capture a banner
    if cards[turn][color - 2] >= cards[abs(turn - 1)][color - 2]:
        # add the banner to the player's collection
        banners[turn][color - 2] = 1
        banners[abs(turn - 1)][color - 2] = 0


def minimax(board, cards, banners, player):
    '''Returns the best move from a given state in the game for a specific player.'''
    result = createCopies(board, cards, banners)
    board = result[0]
    cards = result[1]
    banners = result[2]

    moves = getvalidmoves(board)
    best = moves[0]

    value = minvalue(board, cards, banners, player, best, -math.inf, math.inf)
    for move in moves[1:]:
        v = minvalue(board, cards, banners, player, move, -math.inf, math.inf)
        if v > value:
            best = move
            value = v

    return best


def minvalue(board, cards, banners, player, move, alpha, beta):
    '''Returns the minimum utility available from a player taking an move on the current board.'''
    # Simulate the move of the current player
    result = createCopies(board, cards, banners)
    board = result[0]
    cards = result[1]
    banners = result[2]

    # simulate the move on the copies of the game items
    temp = simulateMove(board, cards, banners, move, player)
    nextplayer = abs(player-1)

    # Check if we are in a terminal state
    moves = getvalidmoves(board)
    # might need another way to return in terminal state
    # like if there are no more moves and max player has more cards
    if len(moves) == 0:
        return 1

    # If not, find minimum utility of possible moves
    beta = math.inf
    for move in moves:
        beta = min(beta, maxvalue(board, cards, banners,
                   nextplayer, move, alpha, beta))
        if alpha > beta:
            # print("pruning happenned")
            break

    return beta


def maxvalue(board, cards, banners, player, move, alpha, beta):
    '''Returns the maximum utility available from a player taking an move on the current board.'''
    # Simulate the move of the current player
    result = createCopies(board, cards, banners)
    board = result[0]
    cards = result[1]
    banners = result[2]

    simulateMove(board, cards, banners, move, player)
    nextplayer = abs(player-1)

    # Check if we are in a terminal state
    moves = getvalidmoves(board)
    if len(moves) == 0:
        return -1

    # If not, find maximum utility of possible moves
    alpha = float('-inf')
    for move in moves:
        alpha = max(alpha, minvalue(board, cards, banners,
                    nextplayer, move, alpha, beta))
        if alpha > beta:
            # print("pruning happenned")
            break

    return alpha
