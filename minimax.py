import chessboard
import chessvalidation
import chessmove
import copy
import random

def point(board):
    point_each = [0, 1, 5, 3, 3, 9, 10000]
    p = 0
    for i in range(8):
        for j in range(8):
            p = p + (1 if board[i][j] > 0 else -1) * point_each[abs(board[i][j])]
    return p

def check_king(board, turn):
    for i in range(8):
        for j in range(8):
            if (board[i][j] * turn == 6): return True
    return False

def calculate(board, turn, enPassant, castling, depth):
    valid_pos = []
    for i in range(8):
        for j in range(8):
            temp_valid = chessvalidation.valid_position_move(board, turn, i, j)
            for valid in temp_valid:
                valid_pos.append([[i, j], valid])
    if (len(valid_pos) == 0): return [turn * 10000, []]
    if (depth == 0): return [point(board), valid_pos[0]]

    random.shuffle(valid_pos)
    # = random.choices(valid_pos, k = 15)
    pt = 0
    move = []
    if (turn > 0):
        max = -10000
        for valid_move in valid_pos:
            result = chessmove.move_piece(board.copy(), valid_move[0][0], valid_move[0][1], valid_move[1][0], valid_move[1][1], enPassant, castling)
            new_board = result[0]
            enPassant = result[1]
            castling = result[2]
            #new_board[valid_move[1][0]][valid_move[1][1]] = new_board[valid_move[0][0]][valid_move[0][1]]
            #new_board[valid_move[0][0]][valid_move[0][1]] = 0
            if (not(check_king(new_board, turn))): return [-10000, []]
            cal = calculate(new_board, -turn, enPassant, castling, depth - 1)[0]
            if (cal > max):
                max = cal
                move = valid_move
        pt = max
    
    else:
        min = 10000
        for valid_move in valid_pos:
            result = chessmove.move_piece(board.copy(), valid_move[0][0], valid_move[0][1], valid_move[1][0], valid_move[1][1], enPassant, castling)
            new_board = result[0]
            enPassant = result[1]
            castling = result[2]
            #new_board[valid_move[1][0]][valid_move[1][1]] = new_board[valid_move[0][0]][valid_move[0][1]]
            #new_board[valid_move[0][0]][valid_move[0][1]] = 0
            if (not(check_king(new_board, turn))): return [10000, []]
            cal = calculate(new_board, -turn, enPassant, castling, depth - 1)[0]
            if (cal < min):
                min = cal
                move = valid_move
        pt = min
    return [pt, move]
            
    
    
