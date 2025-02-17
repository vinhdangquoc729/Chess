def move_piece(board, startX, startY, endX, endY, enPassant, castling):
    board[endX][endY] = board[startX][startY]
    board[startX][startY] = 0

    if (abs(board[endX][endY]) == 1 and abs(startX - endX) == 2): 
        enPassant = [[(startX + endX) // 2, startY], [endX, endY]]
        #print(enPassant)
    else: 
        if (abs(board[endX][endY]) == 1 and enPassant[0][0] == endX and enPassant[0][1] == endY): board[enPassant[1][0]][enPassant[1][1]] = 0
        enPassant = [[-1, -1], [-1, -1]]

    if (abs(board[endX][endY]) == 6):
        if (abs(startY - endY) == 2): 
            if (endY == 2):
                board[endX][3] = board[endX][0]
                board[endX][0] = 0
            elif (endY == 6):
                board[endX][5] = board[endX][7]
                board[endX][7] = 0
        if (endX == 7): castling[0][0] = True
        else: castling[1][0] = True

    if (startX == 0 and startY == 0 and board[endX][endY] == -6): castling[1][1] = True
    if (startX == 0 and startY == 7 and board[endX][endY] == -6): castling[1][2] = True
    if (startX == 7 and startY == 0 and board[endX][endY] == 6): castling[0][1] = True
    if (startX == 7 and startY == 7 and board[endX][endY] == 6): castling[0][2] = True

    if ((board[endX][endY] == 1 or board[endX][endY] == -1) and (endX == 0 or endX == 7)):
        board[endX][endY] = board[endX][endY] * 5
    #self.choosing_square = [endX, endY]
    return [board, enPassant, castling]