
def valid_position_move(board, turn, startX, startY, enPassant = [[-1, -1], [-1, -1]], castling = [[False, False, False], [False, False, False]]):
    def is_valid(pos):
        return (0 <= pos[0] and pos[0] < 8 and 0 <= pos[1] and pos[1] < 8)

    valid_pos = []
    #print(board)
    if (board[startX][startY] * turn <= 0):
        return valid_pos
    #white pawn
    if (board[startX][startY] == 1 and startX < 7):
        if (board[startX - 1][startY] == 0):
            valid_pos.append([startX - 1, startY])
            if (startX == 6 and board[startX - 2][startY] == 0):
                valid_pos.append([startX - 2, startY])
        if (startY > 0 and board[startX - 1][startY - 1] < 0):
            valid_pos.append([startX - 1, startY - 1])
        if (startY < 7 and board[startX - 1][startY + 1] < 0):
            valid_pos.append([startX - 1, startY + 1])
        if (startY > 0 and [startX - 1, startY - 1] == enPassant[0]):
            valid_pos.append(enPassant[0])
        if (startY < 7 and [startX - 1, startY + 1] == enPassant[0]):
            valid_pos.append(enPassant[0])

    #black pawn
    if (board[startX][startY] == -1 and startX > 0):
        if (board[startX + 1][startY] == 0):
            valid_pos.append([startX + 1, startY])
            if (startX == 1 and board[startX + 2][startY] == 0):
                valid_pos.append([startX + 2, startY])
        if (startY > 0 and board[startX + 1][startY - 1] > 0):
            valid_pos.append([startX + 1, startY - 1])
        if (startY < 7 and board[startX + 1][startY + 1] > 0):
            valid_pos.append([startX + 1, startY + 1])
        #enPassant
        if (startY > 0 and [startX + 1, startY - 1] == enPassant[0]):
            valid_pos.append(enPassant[1])
        if (startY < 7 and [startX + 1, startY + 1] == enPassant[0]):
            valid_pos.append(enPassant[1])
    
    #rooks
    if (board[startX][startY] == 2 or board[startX][startY] == -2):
        pos = [[startX + 1, startY], [startX - 1, startY], [startX, startY + 1], [startX, startY - 1]]
        dir = [[1, 0], [-1, 0], [0, 1], [0, -1]]

        for i in range (4):
            while (is_valid(pos[i]) and board[pos[i][0]][pos[i][1]] == 0):
                valid_pos.append(pos[i].copy())
                pos[i][0] = pos[i][0] + dir[i][0]
                pos[i][1] = pos[i][1] + dir[i][1]
            if (is_valid(pos[i]) and board[pos[i][0]][pos[i][1]] * board[startX][startY] < 0):
                valid_pos.append(pos[i].copy())

    #bisects
    if (board[startX][startY] == 4 or board[startX][startY] == -4):
        pos = [[startX + 1, startY + 1], [startX - 1, startY + 1], [startX + 1, startY - 1], [startX - 1, startY - 1]]
        dir = [[1, 1], [-1, 1], [1, -1], [-1, -1]]

        for i in range (4):
            while (is_valid(pos[i]) and board[pos[i][0]][pos[i][1]] == 0):
                valid_pos.append(pos[i].copy())
                pos[i][0] = pos[i][0] + dir[i][0]
                pos[i][1] = pos[i][1] + dir[i][1]
            if (is_valid(pos[i]) and board[pos[i][0]][pos[i][1]] * board[startX][startY] < 0):
                valid_pos.append(pos[i].copy())

    #queens
    if (board[startX][startY] == 5 or board[startX][startY] == -5):
        pos = [[startX + 1, startY], [startX - 1, startY], [startX, startY + 1], [startX, startY - 1], [startX + 1, startY + 1], [startX - 1, startY + 1], [startX + 1, startY - 1], [startX - 1, startY - 1]]
        dir = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]

        for i in range (8):
            while (is_valid(pos[i]) and board[pos[i][0]][pos[i][1]] == 0):
                valid_pos.append(pos[i].copy())
                pos[i][0] = pos[i][0] + dir[i][0]
                pos[i][1] = pos[i][1] + dir[i][1]
            if (is_valid(pos[i]) and board[pos[i][0]][pos[i][1]] * board[startX][startY] < 0):
                valid_pos.append(pos[i].copy())
    
    #knights
    if (board[startX][startY] == 3 or board[startX][startY] == -3):
        dir = [[-2, -1], [-2, 1], [-1, -2], [-1, 2], [1, -2], [1, 2], [2, -1], [2, 1]]
        for i in range (8):
            locX = startX + dir[i][0]
            locY = startY + dir[i][1]
            if (is_valid([locX, locY]) and board[locX][locY] * board[startX][startY] <= 0):
                valid_pos.append([locX, locY])
    
    #kings
    if (board[startX][startY] == 6 or board[startX][startY] == -6):
        dir = [[-1, -1], [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0], [1, 1]]
        for i in range (8):
            locX = startX + dir[i][0]
            locY = startY + dir[i][1]
            if (is_valid([locX, locY]) and board[locX][locY] * board[startX][startY] <= 0):
                valid_pos.append([locX, locY])

    #white king castling
    if (board[startX][startY] == 6):
        if (not castling[0][0]):
            if (not castling[0][1]):
                check = True
                for i in range(1, startY):
                    if (board[startX][i] != 0): check = False
                if (check): valid_pos.append([startX, startY - 2])
            if (not castling[0][2]):
                check = True
                for i in range(startY + 1, 7):
                    if (board[startX][i] != 0): check = False
                if (check): valid_pos.append([startX, startY + 2])

    #black king castling
    if (board[startX][startY] == -6):
        if (not castling[1][0]):
            if (not castling[1][1]):
                check = True
                for i in range(1, startY):
                    if (board[startX][i] != 0): check = False
                if (check): valid_pos.append([startX, startY - 2])
            if (not castling[1][2]):
                check = True
                for i in range(startY + 1, 8):
                    if (board[startX][i] != 0): check = False
                if (check): valid_pos.append([startX, startY + 2])
    valid_pos = [i for i in valid_pos if is_valid(i)]
    return valid_pos