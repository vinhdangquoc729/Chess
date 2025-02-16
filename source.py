import numpy as np
import pygame
# initial chessboard:
"""
-2 -3 -4 -5 -6 -4 -3 -2
-1 -1 -1 -1 -1 -1 -1 -1
0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0
0  0  0  0  0  0  0  0
1  1  1  1  1  1  1  1
2  3  4  5  6  4  3  2
"""

class gameWindow:
    def __init__(self, chessboard, size):
        self.chessboard = chessboard
        self.size = size

    def draw(self, display):
        self.chessboard.draw(display, 100)

    def handle_click(self, mx, my):
        self.chessboard.handle_click(mx, my, 100)

class chessboard:
    def __init__(self, size, board = np.array):
        self.board = board
        self.size = size
        self.square_size = size // 8
        self.choosing_square = [-1, -1]
        self.highlighting_square = [-1, -1]
        self.turn = 1

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

    def valid_position_move(self, startX, startY):
        def is_valid(pos):
            return (0 <= pos[0] and pos[0] < 8 and 0 <= pos[1] and pos[1] < 8)

        valid_pos = []
        if (self.board[startX][startY] * self.turn <= 0):
            return valid_pos
        #white pawn
        if (self.board[startX][startY] == 1 and startX < 7):
            if (self.board[startX - 1][startY] == 0):
                valid_pos.append([startX - 1, startY])
                if (startX == 6 and self.board[startX - 2][startY] == 0):
                    valid_pos.append([startX - 2, startY])
            if (startY > 0 and self.board[startX - 1][startY - 1] < 0):
                valid_pos.append([startX - 1, startY - 1])
            if (startY < 7 and self.board[startX - 1][startY + 1] < 0):
                valid_pos.append([startX - 1, startY + 1])

        #black pawn
        if (self.board[startX][startY] == -1 and startX > 0):
            if (self.board[startX + 1][startY] == 0):
                valid_pos.append([startX + 1, startY])
                if (startX == 1 and self.board[startX + 2][startY] == 0):
                    valid_pos.append([startX + 2, startY])
            if (startY > 0 and self.board[startX + 1][startY - 1] > 0):
                valid_pos.append([startX + 1, startY - 1])
            if (startY < 7 and self.board[startX + 1][startY + 1] > 0):
                valid_pos.append([startX + 1, startY + 1])
        
        #rooks
        if (self.board[startX][startY] == 2 or self.board[startX][startY] == -2):
            pos = [[startX + 1, startY], [startX - 1, startY], [startX, startY + 1], [startX, startY - 1]]
            dir = [[1, 0], [-1, 0], [0, 1], [0, -1]]

            for i in range (4):
                while (is_valid(pos[i]) and self.board[pos[i][0]][pos[i][1]] == 0):
                    valid_pos.append(pos[i].copy())
                    pos[i][0] = pos[i][0] + dir[i][0]
                    pos[i][1] = pos[i][1] + dir[i][1]
                if (is_valid(pos[i]) and self.board[pos[i][0]][pos[i][1]] * self.board[startX][startY] < 0):
                    valid_pos.append(pos[i].copy())

        #bisects
        if (self.board[startX][startY] == 4 or self.board[startX][startY] == -4):
            pos = [[startX + 1, startY + 1], [startX - 1, startY + 1], [startX + 1, startY - 1], [startX - 1, startY - 1]]
            dir = [[1, 1], [-1, 1], [1, -1], [-1, -1]]

            for i in range (4):
                while (is_valid(pos[i]) and self.board[pos[i][0]][pos[i][1]] == 0):
                    valid_pos.append(pos[i].copy())
                    pos[i][0] = pos[i][0] + dir[i][0]
                    pos[i][1] = pos[i][1] + dir[i][1]
                if (is_valid(pos[i]) and self.board[pos[i][0]][pos[i][1]] * self.board[startX][startY] < 0):
                    valid_pos.append(pos[i].copy())

        #queens
        if (self.board[startX][startY] == 5 or self.board[startX][startY] == -5):
            pos = [[startX + 1, startY], [startX - 1, startY], [startX, startY + 1], [startX, startY - 1], [startX + 1, startY + 1], [startX - 1, startY + 1], [startX + 1, startY - 1], [startX - 1, startY - 1]]
            dir = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]

            for i in range (8):
                while (is_valid(pos[i]) and self.board[pos[i][0]][pos[i][1]] == 0):
                    valid_pos.append(pos[i].copy())
                    pos[i][0] = pos[i][0] + dir[i][0]
                    pos[i][1] = pos[i][1] + dir[i][1]
                if (is_valid(pos[i]) and self.board[pos[i][0]][pos[i][1]] * self.board[startX][startY] < 0):
                    valid_pos.append(pos[i].copy())
        
        #knights
        if (self.board[startX][startY] == 3 or self.board[startX][startY] == -3):
            dir = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
            for i in range (8):
                locX = startX + dir[i][0]
                locY = startY + dir[i][1]
                if (is_valid([locX, locY]) and self.board[locX][locY] * self.board[startX][startY] <= 0):
                    valid_pos.append([locX, locY])
        
        #kings
        if (self.board[startX][startY] == 6 or self.board[startX][startY] == -6):
            dir = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
            for i in range (8):
                locX = startX + dir[i][0]
                locY = startY + dir[i][1]
                if (is_valid([locX, locY]) and self.board[locX][locY] * self.board[startX][startY] <= 0):
                    valid_pos.append([locX, locY])

        return valid_pos

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
        self.board[endX][endY] = self.board[startX][startY]
        self.board[startX][startY] = 0
        if ((self.board[endX][endY] == 1 or self.board[endX][endY] == -1) and (endX == 0 or endX == 7)):
            self.board[endX][endY] = self.board[endX][endY] * 5

    def draw(self, display, padding):
        square_size = self.square_size
        valid_position_move = self.valid_position_move(self.choosing_square[0], self.choosing_square[1])
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

board = np.array([[-2, -3, -4, -5, -6, -4, -3, -2],
                 [-1, -1, -1, -1, -1, -1, -1, -1],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [2, 3, 4, 5, 6, 4, 3, 2]])

board = chessboard(600, board)
game = gameWindow(board, (800, 800))
pygame.init()

WINDOW_SIZE = (800, 800)
screen = pygame.display.set_mode(WINDOW_SIZE)

def draw(display):
    display.fill('white')
    game.draw(display)
    pygame.display.update()


if __name__ == '__main__':
    running = True
    while running:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    game.handle_click(mx, my)
        draw(screen)