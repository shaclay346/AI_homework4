from random import randint
from hand_of_the_king import getvalidmoves
import pdb


def get_computer_move(board, cards, banners, turn):
    minimax(board, cards, bannners, player)


def minimax(board, cards, bannners, player):
    '''Returns the best action from a given state in the game for a specific player.'''
    actions = getvalidmoves(board)

    best = actions[0]
    value = minvalue(board, player, best, -math.inf, math.inf)
    for action in actions[1:]:
        v = minvalue(board, player, action,  -math.inf, math.inf)
        if v > value:
            best = action
            value = v
    return best


def minvalue(board, player, action, alpha, beta):
    '''Returns the minimum utility available from a player taking an action on the current board.'''
    # Simulate the action of the current player
    state = board
    temp = state[action]
    state[action] = 0
    # pdb.set_trace()
    nextplayer = math.abs(player-1)

    # Check if we are in a terminal state
    moves = getvalidmoves(state)
    if len(moves) == 0:
        state[action[0], action[1]] = 0
        return 1

    # If not, find minimum utility of possible actions
    beta = math.inf
    for move in moves:
        beta = min(beta, maxvalue(state, nextplayer, move, beta, alpha))
        if alpha > beta:
            print("pruning happenned")
            break

    # set the board back
    state[action] = temp
    return beta


def maxvalue(board, player, action, alpha, beta):
    '''Returns the maximum utility available from a player taking an action on the current board.'''
    # Simulate the action of the current player
    state = board
    state[action[0], action[1]] = player
    nextplayer = 3 - player

    # Check if we are in a terminal state
    moves = getvalidmoves(board)
    if len(moves) == 0:
        return -1

    # If not, find maximum utility of possible actions
    alpha = -math.inf
    for move in moves:
        alpha = max(alpha, minvalue(state, nextplayer, move, alpha, beta))
        if alpha > beta:
            print("pruning happenned")
            break

    state[action[0], action[1]] = 0
    return alpha
