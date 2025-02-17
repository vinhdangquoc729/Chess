import pygame
import numpy as np
import chessvalidation
import chessmove
import minimax
import time

class chessboard:
    def __init__(self, size, board = np.array):
        self.board = board
        self.size = size
        self.square_size = size // 8
        self.choosing_square = [-1, -1]
        self.highlighting_square = [-1, -1]
        self.turn = 1
        self.enPassant = [[-1, -1], [-1, -1]]
        self.castling = [[False, False, False], [False, False, False]]
        self.surrender = False

        self.img_black = []
        self.img_black.append(pygame.image.load("img\\bp.png"))
        self.img_black.append(pygame.image.load("img\\br.png"))
        self.img_black.append(pygame.image.load("img\\bn.png"))
        self.img_black.append(pygame.image.load("img\\bb.png"))
        self.img_black.append(pygame.image.load("img\\bq.png"))
        self.img_black.append(pygame.image.load("img\\bk.png"))

        self.img_white = []
        self.img_white.append(pygame.image.load("img\\wp.png"))
        self.img_white.append(pygame.image.load("img\\wr.png"))
        self.img_white.append(pygame.image.load("img\\wn.png"))
        self.img_white.append(pygame.image.load("img\\wb.png"))
        self.img_white.append(pygame.image.load("img\\wq.png"))
        self.img_white.append(pygame.image.load("img\\wk.png"))
        
        for i in range (6):
            self.img_black[i] = pygame.transform.smoothscale(self.img_black[i], (self.square_size, self.square_size))
            self.img_white[i] = pygame.transform.smoothscale(self.img_white[i], (self.square_size, self.square_size))

    def is_valid(self, pos):
        return (0 <= pos[0] and pos[0] < 8 and 0 <= pos[1] and pos[1] < 8)

    def valid_position_move(self, startX, startY, opponent = 1):
        return chessvalidation.valid_position_move_no_danger(board = self.board, turn = self.turn * opponent, startX=startX, startY=startY, enPassant = self.enPassant, castling = self.castling)

    def handle_click(self, mx, my, padding):
        mmx = mx - padding
        mmy = my - padding
        posY = mmx // self.square_size
        posX = mmy // self.square_size
        pos = [posY, posX]
        if (self.is_valid(pos)):
            if (self.choosing_square == [posX, posY]):
                self.choosing_square = [-1, -1]
            elif (self.choosing_square == [-1, -1]):
                self.choosing_square = [posX, posY]
            elif (self.valid_position_move(self.choosing_square[0], self.choosing_square[1]).count([posX, posY]) > 0):
                self.move_piece(self.choosing_square[0], self.choosing_square[1], posX, posY)
                self.turn = -self.turn
            else:
                self.choosing_square = [posX, posY]

    def move_piece(self, startX, startY, endX, endY):
        self.choosing_square = [endX, endY]
        self.board, self.enPassant, self.castling = chessmove.move_piece(self.board, startX, startY, endX, endY, self.enPassant, self.castling)
        valid_pos = []
        for i in range (8):
            for j in range(8):
                if (self.board[i][j] * self.turn < 0):
                    valid_pos = valid_pos + self.valid_position_move(i, j, -1)
        if (len(valid_pos) == 0):
            self.surrender = True
        else:
            print (valid_pos)
        
    def point(self):
        point_each = [0, 1, 5, 3, 3, 9, 100]
        p = 0
        for i in range(8):
            for j in range(8):
                p = p + (1 if self.board[i][j] > 0 else -1) * point_each(abs(self.board[i][j]))
        return p

    def draw(self, display, padding):
        square_size = self.square_size
        valid_position_move = self.valid_position_move(self.choosing_square[0], self.choosing_square[1])
        #print(valid_position_move)
        for i in range (8):
            for j in range (8):
                rect = pygame.Rect(padding + i * square_size, padding + j * square_size, square_size, square_size)
                if ((i + j) % 2 == 0):
                    pygame.draw.rect(display, (185, 202, 67) if ([j, i] == self.choosing_square) else (119, 149, 86), rect)
                else:
                    pygame.draw.rect(display, (245, 246, 130) if ([j, i] == self.choosing_square) else (235, 236, 208), rect)
                if (self.board[j][i] < 0):
                    display.blit(self.img_black[-self.board[j][i] - 1], rect)
                elif (self.board[j][i] > 0):
                    display.blit(self.img_white[self.board[j][i] - 1], rect)
        if (self.is_valid(self.choosing_square)):
            for valid_pos in valid_position_move:
                centerY = padding + valid_pos[0] * square_size + square_size // 2
                centerX = padding + valid_pos[1] * square_size + square_size // 2
                radius = square_size // 4
                pygame.draw.circle(display, (185, 202, 67), center = (centerX, centerY), radius = radius)
        #print(minimax.calculate(self.board, self.turn, 3))
    def endgame(self):
        black_king = white_king = False
        for i in range(8):
            for j in range(8):
                if (self.board[i][j] == -6): black_king = True
                elif (self.board[i][j] == 6): white_king = True
        if (not(black_king)):
            print("White wins!")
            return True
        elif(not(white_king)):
            print("Black wins!")
            return True
        else: return False


    def AI_move(self):
        move = minimax.calculate(self.board, self.turn, self.enPassant, self.castling, 3)[1]
        if (len(move) == 0): 
            self.surrender = True
            print("You win!")
            return
        self.move_piece(move[0][0], move[0][1], move[1][0], move[1][1])
        self.choosing_square = move[1]
        self.turn = -self.turn
        #time.sleep(0.5)
