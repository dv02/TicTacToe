import random

board = [
    [0,0,0],
    [0,0,0],
    [0,0,0]
]

def printBoard( board ):
    '''
    ' Bekommt ein Board und gibt es auf der Konsole aus.
    ' Schaut euch die zwei Schleifen an und versteht, was
    ' sie tun!
    ' Die Indexe idx und jdx geben an, in welchem Feld wir
    ' gerade sind. Sie werden benoetigt, da wir nur die
    ' inneren Feldgrenzen zeichnen wollen.
    ' :param: board - 3x3-Spielfeld
    '''
    print
    idx = 0
    for line in board:
        jdx = 0
        string = ''
        for field in line:
            if field == 0:
                string += '   '
            elif field == -1:
                string += ' O '
            elif field == 1:
                string += ' X '
            else:
                print('Fehler in printBoard: board enthaelt falsches Symbol: '+str(field))
            if jdx < 2: string += '|'
            jdx += 1
        print(string)
        if idx < 2: print('---|---|---')
        idx += 1 

def testLine( line ):
    '''
    ' :param line: Liste mit drei Zahlen
    ' :return:   1, wenn alle Elemente von line == 1
    '           -1, wenn alle Elemente von line ==-1
    '            0, sonst
    '''
    if line[0] == 1 and line[1] == 1 and line[2] == 1:
        return 1
    elif line[0] == -1 and line[1] == -1 and line[2] == -1:
        return -1
    return 0

def getWinner( board ):
    '''
    ' Loops through the board to check
    ' wether there is a winning condition.
    ' :param board: A 2 dimensional array representing the board
    ' :return:    The winning player of the
    '             board (-1 or 1) if there is one, 0 otherwise
    '''
    # teste Spalten
    for idx in range(3):
        line = [board[0][idx],board[1][idx],board[2][idx]]
        if not testLine(line) == 0:
            return line[0]
        
    # teste Reihen
    for idx in range(3):
        line = board[idx]
        if not testLine(line) == 0:
            return line[0]
        
    # teste Diagonalen
    line = [board[0][0],board[1][1],board[2][2]]
    if not testLine(line) == 0:
        return line[0]
    line = [board[0][2],board[1][1],board[2][0]]
    if not testLine(line) == 0:
        return line[0]

    # kein Gewinner
    return 0

def testDraw( board ):
    '''
    ' Check if the game should end
    ' as a draw (all fields are filled)
    '''
    for row in board:
        for entry in row:
            # If one field is free, there can't be a
            # draw situation
            if entry == 0:
                return False
    
    return True

def get_empty_fields(board):
    fields = []
    for row in range(3):
        for col in range(3):
            if board[row][col] == 0:
                fields.append((row,col))
    return fields


def random_move(board, player):
    result = 0
    while result == 0:
        emptyFields = get_empty_fields(board)
        if emptyFields == []:
            return 0

        move = random.choice(emptyFields)
        board[move[0]][move[1]] = player
        player*=-1

        result = getWinner(board)
    return result

def copy_list(liste):
    newList = []
    for val in liste:
        newList.append(val)
    return newList

def copy_board(board):
    newBoard = []
    for row in board:
        newBoard.append( copy_list(row) )
    return newBoard

def simulate_moves(board, player, repetitions = 100):
    counter = [0, 0, 0]
    while repetitions > 0:
        newBoard = copy_board(board)
        result = random_move(newBoard, player)
        counter[ result + 1 ] += 1
        repetitions -= 1
    return counter

def evaluate_moves(board, player, repetitions = 100):
    freeFields = get_empty_fields(board)
    results = []
    for field in freeFields:
        board[field[0]][field[1]] = player
        result = simulate_moves(board, player, repetitions)
        results.append(result)
        board[field[0]][field[1]] = 0
    return results

def nextMove(board, player, repetitions = 100):
    freeFields = get_empty_fields(board)
    values = evaluate_moves(board, player, repetitions)
    for idx in range(len(values)):
        values[idx] = values[idx][2] * player
    maxValue = max(values)
    maxIndex = values.index(maxValue)
    return freeFields[maxIndex]

if __name__ == "__main__":
    for i in range(80):print
    player = 1
    while getWinner(board) == 0 and not testDraw(board):
        move = nextMove(board, player, 10000)
        board[move[0]][move[1]] = player
        printBoard(board)
        player *= -1