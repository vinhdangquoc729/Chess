import numpy as np
import pygame
import chessboard
import minimax
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
        if (self.chessboard.surrender == True):
            pygame.font.init()
            my_font = pygame.font.SysFont('Comic Sans MS', 30)
            text_surface = my_font.render('Game Over!', False, (255, 0, 0))
            display.blit(text_surface, (400 - text_surface.get_width() / 2, 30))

    def handle_click(self, mx, my):
        self.chessboard.handle_click(mx, my, 100)

board = np.array([[-2, -3, -4, -5, -6, -4, -3, -2],
                 [-1, -1, -1, -1, -1, -1, -1, -1],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0],
                 [1, 1, 1, 1, 1, 1, 1, 1],
                 [2, 3, 4, 5, 6, 4, 3, 2]])

board = chessboard.chessboard(600, board)
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
    while running and not(board.endgame()):
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if (board.turn == 1): 
                    if event.button == 1:
                        game.handle_click(mx, my)
            else:
                if (board.turn == -1): 
                    board.AI_move()
        draw(screen)
        #print(minimax.calculate())