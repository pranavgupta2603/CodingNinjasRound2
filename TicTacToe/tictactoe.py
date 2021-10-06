from math import inf as infinity
from random import choice
import platform
import time
from os import system



def wins(state, player):
    #print(state)
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    
    if [player, player, player] in win_state:
        return True
    else:
        return False

def evaluate(state):

    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score

def game_over(state):
    
    return wins(state, HUMAN) or wins(state, COMP)
def valid_move(x, y):

    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):

    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False

def empty_cells(state):
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])
    return cells
def clean():
    
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)

def count_all_score_combos(state, depth, player):
    #print(game_over(state))

    score = evaluate(state)
    if score == 1:
        totF = [1, 0, 0]
        return [-1, -1, score], depth, totF, depth, depth
    if score == -1:
        totF = [0, 0, 1]
        return [-1, -1, score], depth, totF, depth, depth

    if depth == 0 or len(empty_cells(state)) == 0:
        #(hi)
        score = evaluate(state)

        tot = [0, 0, 0]
        if score == 1:
            
            tot[0] = 1
        elif score == 0:
            
            tot[1] = 1
        else:
            tot[2] = 1
        
        return [-1, -1, score], depth, tot, depth, depth

    totF = [0, 0, 0]
    win_depth_max = -1
    lose_depth_max = -1
    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score, depth_use, tot, win_depth, lose_depth = count_all_score_combos(state, depth - 1, -player)
        #print(state)
        #print(tot)
        state[x][y] = 0
        score[0], score[1] = x, y
        for i in range(len(tot)):
            totF[i] = totF[i] + tot[i]
        if win_depth > win_depth_max:
            win_depth_max = win_depth
        if lose_depth > lose_depth_max:
            lose_depth_max = lose_depth
        
    
    return score, depth_use, totF, win_depth_max, lose_depth_max


def chooseTheBestMove(state, depth, player):
    bestMove=""
    bestMoveTot=""
    bestMoveWinDepth=-1
    bestMoveLoseDepth = -1
    for cell in empty_cells(state):
        x, y = cell[0], cell[1]
        state[x][y] = player
        score, depth_use, tot, win_depth, lose_depth = count_all_score_combos(state, depth - 1, -player)
        #print(state)
        #print(cell)
        #print(tot)
        #print(win_depth)
        #print(lose_depth)
        state[x][y] = 0
        if bestMove == "":
            bestMove = cell
            bestMoveTot = tot
            bestMoveWinDepth = win_depth
            bestMoveLoseDepth = lose_depth
            if depth - 1 == win_depth:
                break
            
        else:
            if (bestMoveLoseDepth  == depth - 2):
                bestMove = cell
                bestMoveTot = tot
                bestMoveWinDepth = win_depth
                bestMoveLoseDepth = lose_depth
                if depth - 1 == win_depth:
                    break
                
            if (tot[0] >= bestMoveTot[0] or depth - 1 == win_depth) and depth - 2 != lose_depth:
                bestMove = cell
                bestMoveTot = tot
                bestMoveWinDepth = win_depth
                bestMoveLoseDepth = lose_depth
            if depth - 1 == win_depth:
                break
        #print("************")  
        #print(bestMove)
    return bestMove
    #pint(bestMoveTot)
        
def ai_turn(c_choice, h_choice):
    
    #depth = len(empty_cells(board))
    if len(empty_cells(board)) == 0:
        return

    clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)

    if len(empty_cells(board)) == 9:
        x = choice([0, 1, 2])
        y = choice([0, 1, 2])
    else:
        #print(board)
        move = chooseTheBestMove(board, depth, COMP)

        #print(move)
        x, y = move[0], move[1]

    set_move(x, y, COMP)
    time.sleep(1)
def human_turn(c_choice, h_choice):
    
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    while move < 1 or move > 9:
        try:
            move = int(input('Use numpad (1..9): '))
            coord = moves[move]
            can_move = set_move(coord[0], coord[1], HUMAN)

            if not can_move:
                print('Bad move')
                move = -1
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')
    
board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
depth = 9
COMP = 1
HUMAN = -1
total_scores =[]

#score, d, totF = count_all_score_combos(board, depth, COMP)
#print(totF)
#all_final_cods = []

def main():

    clean()
    h_choice = ''  # X or O
    c_choice = ''  # X or O
    first = ''  # if human is the first

    # Human chooses X or O to play
    while h_choice != 'O' and h_choice != 'X':
        try:
            print('')
            h_choice = input('Choose X or O\nChosen: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Setting computer's choice
    if h_choice == 'X':
        c_choice = 'O'
    else:
        c_choice = 'X'

    # Human may starts first
    clean()
    while first != 'Y' and first != 'N':
        try:
            first = input('First to start?[y/n]: ').upper()
        except (EOFError, KeyboardInterrupt):
            print('Bye')
            exit()
        except (KeyError, ValueError):
            print('Bad choice')

    # Main loop of this game
    while len(empty_cells(board)) > 0 and not game_over(board):
        if first == 'N':
            ai_turn(c_choice, h_choice)
            first = ''
        
        human_turn(c_choice, h_choice)
        ai_turn(c_choice, h_choice)
        
    # Game over message
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, COMP):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')
    time.sleep(3)
    exit()
main()
