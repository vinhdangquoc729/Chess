import chessboard
import chessvalidation
import copy
import random

def point(board):
    point_each = [0, 1, 5, 3, 3, 9, 100]
    p = 0
    for i in range(8):
        for j in range(8):
            p = p + (1 if board[i][j] > 0 else -1) * point_each[abs(board[i][j])]
    return p

def calculate(board, turn, depth):
    valid_pos = []
    for i in range(8):
        for j in range(8):
            temp_valid = chessvalidation.valid_position_move(board, turn, i, j)
            for valid in temp_valid:
                valid_pos.append([[i, j], valid])
    if (len(valid_pos) == 0): return [turn * 10000, []]
    if (depth == 0): return [point(board), valid_pos[0]]

    random.shuffle(valid_pos)
    #valid_pos = random.choices(valid_pos, k = 10)
    pt = 0
    move = []
    if (turn > 0):
        max = -10000
        for valid_move in valid_pos:
            new_board = copy.copy(board)
            new_board[valid_move[1][0]][valid_move[1][1]] = new_board[valid_move[0][0]][valid_move[0][1]]
            new_board[valid_move[0][0]][valid_move[0][1]] = 0
            cal = calculate(new_board, -turn, depth - 1)[0]
            if (cal > max):
                max = cal
                move = valid_move
        pt = max
    
    else:
        min = 10000
        for valid_move in valid_pos:
            new_board = copy.copy(board)
            new_board[valid_move[1][0]][valid_move[1][1]] = new_board[valid_move[0][0]][valid_move[0][1]]
            new_board[valid_move[0][0]][valid_move[0][1]] = 0
            cal = calculate(new_board, -turn, depth - 1)[0]
            if (cal < min):
                min = cal
                move = valid_move
        pt = min
    return [pt, move]
            
    
    
