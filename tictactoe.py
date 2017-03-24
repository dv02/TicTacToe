# Template für Tic-Tac-Toe
# Das 3x3-Spielfeld wird als 2 dimensionale Liste
# repraesentiert, wobei gilt:
#       0 -> leeres Feld
#       1 -> Spieler 1 (X)
#      -1 -> Spieler 2 (O).
# Es gibt einmal die Ausgabe auf der Konsole mit manueller
# Eingabe und dann die interaktive Spielflaeche mit Maus-
# eingabe.

import simplegui
import random
import codeskulptor

####################################################
# globale Variablen
####################################################

# reset the timer because of the AI
codeskulptor.set_timeout(100)

# draw Variablen
WINDOWX = 1000
WINDOWY = 700
GAMESIZE = 500
LINEWIDTH = 6
OFFSETX = 300
OFFSETY = 100
TICKS = 0
FIRSTCOLOR = 'Red'
SECONDCOLOR = 'Blue'
BIG_MESSAGE_COLOR = 'Green'



# list of 3 lists, which contain the colors for each field
colors = [
    ["White" for x in range(3)]
    for x in range(3)]

# list of 3 lists, which contain the colors for
# the radius ufeach field
radiusColors = [
    ["Black" for x in range(3)]
    for x in range(3)]



radiuses = [[1,1,1],   # alles 1
         [1,1,1],
         [1,1,1]]
spielerAnzeige = '' # zeigt an, wer am Zug ist
bigMessage = ''

# rgb array for the colors of the "draw" message
DRAW_MESSAGE_COLORS = [255, 0, 0]

# Spielvariablen
board = [[0,0,0],   # leeres Board
         [0,0,0],
         [0,0,0]]
running = False     # zeigt an, ob ein Spiel laeuft
restarting = False  # tells whether the game is restarting
player = 1          # zeigt aktuellen Spieler an

# Blinking Timer variables
blinkTimer = None
blinked = 0

# important game flags
AI_MODE = 0     # The mode of the ai: 
                # 0 => Turned off
                # 1 => MiniMax
                # 2 => MonteCarlo
AUTO_RESTART = True

# for the AI
corners = [
    (0,0),
    (0,2),
    (2,0),
    (2,2)
    ]

# statistics
wins = [0, 0]
draws = 0
played = 0

# sounds
VOLUME = 0.7
errorSound = simplegui.load_sound('http://5.189.177.192/info/error.mp3')
errorSound.set_volume(VOLUME)
plopSound = simplegui.load_sound('http://5.189.177.192/info/plop.mp3')
plopSound.set_volume(VOLUME)
backGroundMusic  = simplegui.load_sound('http://5.189.177.192/info/background.mp3')
backGroundMusic.set_volume(VOLUME)

# boolean flag for whether the animating
# rainbow background should be toggled on or not.
background = False


####################################################
# Hilfsfunktionen und Test
####################################################

def playMusic():
    '''
    ' Play the global backgroundMusic
    '''
    global backGroundMusic
    backGroundMusic.rewind()
    backGroundMusic.play()

'''
' Helper class for a Timer object which can run a given function
' n times per x milliseconds
'''
class FieldAnimation():
    
    # initilize all fields
    ticks = 0
    maxTicks = 1
    timer = None
    action = None
    fieldRow = -1
    fieldCol = -1
    
    def doTick(self):
        if self.ticks == self.maxTicks:
            self.timer.stop()
            return
        row = self.fieldRow
        col = self.fieldCol
        self.action(row, col, self.ticks)
        self.ticks += 1
    
    def start(self):
        self.timer.start()
        
    def getTicks(self):
        return self.ticks
    
    def getMaxTicks(self):
        return self.maxTicks
    
    def __init__(self, maxTicks, time, action, row, col):
        '''
        ' Creates a new timer, does NOT start it
        ' :param: maxTicks - The maximum ticks before the timer will stop
        ' :param: time - the delay between the actions
        ' :param: action - The action which will be called each tick
        ' :param: row - The row of the field to be animated
        ' :param: col - The column of the field to be animated
        '''
        assert(0<= row and row <= 2, "row must be between 0 and 2")
        assert(0<= col and col <= 2, "col must be between 0 and 2")
        self.maxTicks = maxTicks
        self.fieldRow = row
        self.fieldCol = col
        self.action = action
        self.timer = simplegui.create_timer(time, self.doTick)
        
        
'''
' Helper class used to create a delay (example: for the computer's move)
'''
class Delay():
    timer = None
    action = None
    arg = None
    ticks = 0
    delay = 1
    
    def doTick(self):
        if self.ticks == 1:
            self.timer.stop()
            return
        if self.arg == None:
            self.action()
        else:
            self.action(self.arg)
        self.ticks += 1
    
    def start(self):
        self.timer.start()
    
    def __init__(self, delay, action, arg = None):
        '''
        ' Creates a new timer, does NOT start it
        ' :param: delay - The delay of the timer
        ' :param: action - The action which will be called each tick
        ' :param: arg - The Argument the method will be called with
        '''
        self.delay = delay
        self.arg = arg
        self.action = action
        self.timer = simplegui.create_timer(delay, self.doTick)
        
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

def showCurrentPlayerMessage():
    '''
    ' Changes the "spielerAnzeige" to the actual
    ' value of the current player
    '''
    global player, spielerAnzeige    
    if player == 1:
        spielerAnzeige = "Der rote Spieler ist an der Reihe!"
    elif player == -1:
        spielerAnzeige = "Der blaue Spieler kann loslegen!"

def emptyBoard():
    '''
    ' This will empty the board
    '''
    global board
    board = [[0,0,0],
             [0,0,0],
             [0,0,0]]

def isEmptyBoard(board):
    '''
    ' This will check if the given board is empty
    ' :param: board - The board to check
    ' :return: True if the board is empty, False otherwise
    '''
    for row in board:
        for entry in row:
            if not entry == 0:
                return False
    return True

def testFunction():
    '''
    ' Hier koennen/sollen alle eure Funktionen getestet
    ' werden. Testet regelmaessig, damit sich keine
    ' Fehler ansammeln.
    '''
    testBoard = [[ 0, 1, 0],
                 [-1, 0,-1],
                 [ 0, 1, 0]]
    print "---- RUN TESTS ----"
    print "TestBoard"
    printBoard( testBoard )
    
    print "\n Teste makeMove auf (0,2)"
    testBoard = makeMove( testBoard, 0, 2)
    printBoard( testBoard )
    
    # Index out of bounds!
    #print "\n Teste makeMove auf (0,3)"
    #testBoard = makeMove( testBoard, 0, 3)
    #printBoard( testBoard )
    
    print "\n Teste Change Player mit makeMove auf (2,0)"
    changePlayer()
    testBoard = makeMove( testBoard, 2, 0)
    printBoard( testBoard )

    for i in range(7): print
    #teste testLine()
    print "\n Teste testLine() mit (1, 1, 1)"
    print(" Ergebnis: " + str(testLine([1, 1, 1])))
    print "\n Teste testLine() mit (1, 0, 1)"
    print(" Ergebnis: " + str(testLine([1, 0, 1])))
    print "\n Teste testLine() mit (-1, -1, -1)"
    print(" Ergebnis: " + str(testLine([-1, -1, -1])))
   
    
    #teste testWin()
    testBoard = [[ 0, 1, 0],
                 [-1, 1,-1],
                 [ 0, 1, 0]]
    for i in range(7): print
    print "\nTeste testWin mit:"
    printBoard(testBoard)
    print "Ergebnis testWin: " + str(testWin(testBoard))
    print
    print "\nTeste getWinner mit:"
    printBoard(testBoard)
    print "Ergebnis getWinner: " + str(getWinner(testBoard))
    testBoard = [[ 0, 1, 0],
                 [-1, 0,-1],
                 [ 0, 1, 0]]
    
    
    
    # teste getWinner
    print
    print "\nTeste getWinner mit:"
    printBoard(testBoard)
    print "Ergebnis getWinner: " + str(getWinner(testBoard))
    testBoard = [[ 0, 1, 0],
                 [-1, -1,-1],
                 [ 0, 1, 0]]
    print
    print "\nTeste getWinner mit:"
    printBoard(testBoard)
    print "Ergebnis getWinner: " + str(getWinner(testBoard))
    
    
    
    # teste testDraw()
    testBoard = [[ 1, 1,-1],
                 [-1, 1, 1],
                 [ 1,-1,-1]]
    print
    print "\nTeste testDraw mit:"
    printBoard(testBoard)
    print "Ergebnis testDraw: " + str(testDraw(testBoard))
    
    for i in range(7): print
        
        
        
        
    # teste convertMove( string )  
        
    print "\nTeste convertMove mit: 00"
    print "Ergebnis convertMove: " + str(convertMove("00"))
    print
    print "\nTeste convertMove mit: 12"
    print "Ergebnis convertMove: " + str(convertMove("12"))
    print
    print "\nTeste convertMove mit: a0"
    print "Ergebnis convertMove: " + str(convertMove("a0"))
    print
    print "\nTeste convertMove mit: \"\""
    print "Ergebnis convertMove: " + str(convertMove(""))
    print
    
    
    
    
    # Teste KI (nextMove)
    for i in range(7): print
    print "TESTE KUENSTLICHE INTELLIGENZ\n"
    
    testBoard = [[ 1, 1,-1],
                 [-1, 1, 1],
                 [ 1,-1,-1]]
    print "teste nextMove mit Player = 1, board:"
    printBoard(testBoard)
    print "Ergebnis nextMove: " + str(nextMove(testBoard, 1))
    print
    
    
    
    testBoard = [[ 1, 1, 0],
                 [-1, 1, 1],
                 [ 1,-1,-1]]
    print "teste nextMove mit Player = 1, board:"
    printBoard(testBoard)
    print "Ergebnis nextMove: " + str(nextMove(testBoard, 1))
    print
    
    
    
    testBoard = [[ -1, -1, 0],
                 [ 0, 0, 0],
                 [ 1, 1, 0]]
    print "teste nextMove mit Player = -1, board:"
    printBoard(testBoard)
    print "Ergebnis nextMove: " + str(nextMove(testBoard, -1))
    print
    
    for i in range(7): print
    print "\n---- END TESTS ----"

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
                print 'Fehler in printBoard: board enthaelt '+\
                      'falsches Symbol!'
            if jdx < 2: string += '|'
            jdx += 1
        print string
        if idx < 2: print '---|---|---'
        idx += 1 
    
def convertMove( string ):
    '''
    ' ...
    ' :param: String, entaelt Koordinaten im Format
    '         '00', also zwei Zahlen. Die erste steht
    '         fuer die Reihe, das zweite ist die Zeile.
    ' :return: Tupel (row, col) mit 0 <= row,col <= 2
    '          Bei falscher Eingabe returns (-1,-1).
    '''
    if not len(string) == 2:
        return (-1, -1)
    # muss int sein
    try: 
        return (int(string[0]), int(string[1]))
    except ValueError:
        return (-1, -1)

####################################################
# Spiellogik
####################################################
def makeMove( board, row, col):
    '''
    ' makeMove veraendert das board.
    ' :global: player
    ' :param: board - das aktuelle Spielbrett
    ' :param: row -> Zeilennummer
    ' :param: col -> Spaltennummer.
    ' :return: board
    '''
    global player
    # testet, ob die Zeile und Spalte im erlaubten Bereich sind
    assert (row >= 0 and row <= 2), \
           "Fehler in makeMove: Zeilenindex falsch!(" + str(row) + ", " + str(col) + ")"
    assert (col >= 0 and col <= 2), \
           "Fehler in makeMove: Zeilenindex falsch!(" + str(row) + ", " + str(col) + ")"
        
    if not board[row][col] == 0: return None
    # set the selected field to the player's value
    board[row][col] = player
    
    return board

def changePlayer():
    '''
    ' This will set the player to 1 if it currently is -1,
    ' else it will be set to -1.
    '''
    global player
    player *= -1  # just change the sign ...

def testLine( line ):
    '''
    ' :param line: Liste mit drei Zahlen
    ' :return:   1, wenn alle Elemente von line == 1
    '           -1, wenn alle Elemente von line ==-1
    '            0, sonst
    '''
    assert (len(line) == 3, "Fehler in testLine: Ungueltige Zeilen-Liste")
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

def testWin( board ):
    '''
    ' Testet, ob es eine Gewinnstellung gibt. Dabei werden
    ' alle Reihen, alle Spalten und die Diagonalen getestet.
    ' Ruft testLine() auf.
    ' :global:   Winner wird gesetzt, falls es eine Gewinn-
    '            stellung gibt.
    ' :return:   True, wenn ein Spieler gewonnen hat
    '            False, sonst
    '''
    
    win = getWinner(board)
    global winner
    winner = win
    if not win == 0:
        return True
    return False

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

def endGame( board ):
    '''
    ' End the game by resetting all
    ' global variables, but only if
    ' there is a winning condition
    ' :global:   running wird auf False gesetzt, falls 
    '            das Spiel zu ende ist.
    ' :return:   True, falls Ende
    '            False, sonst
    '''
    if testWin(board) or testDraw(board):
        global running, FIRSTCOLOR, SECONDCOLOR, bigMessage
        running = False
        FIRSTCOLOR = 'Red'
        SECONDCOLOR = 'Blue'
        bigMessage = ''
        return True
    return False

####################################################
# Graphik Funktionen
####################################################
def drawField( canvas ):
    '''
    ' Draws the field's lines on the canvas
    ' :param: canvas    The canvas object
    '                   on which the lines / border should be drawed on
    '''
    global GAMESIZE, LINEWIDTH, OFFSETX, OFFSETY
    
    # Konstanten zum Zeichnen
    fieldSize = GAMESIZE / 3
    color = 'Blue'
    
    # nuetzliche Abstaende
    p1 = 0
    p2 = GAMESIZE
    p3 = (fieldSize - LINEWIDTH / 2 )
    p4 = (2 * fieldSize + LINEWIDTH / 2)
    
    # borders
    canvas.draw_line((p1+ OFFSETX, p1+ OFFSETY), (p1+ OFFSETX, p2+ OFFSETY), LINEWIDTH, color)
    canvas.draw_line((p1+ OFFSETX, p2+ OFFSETY), (p2+ OFFSETX, p2+ OFFSETY), LINEWIDTH, color)
    canvas.draw_line((p2+ OFFSETX, p1+ OFFSETY), (p2+ OFFSETX, p2+ OFFSETY), LINEWIDTH, color)
    canvas.draw_line((p1+ OFFSETX, p1+ OFFSETY), (p2+ OFFSETX, p1+ OFFSETY), LINEWIDTH, color)
    
    # vertikale Linien
    canvas.draw_line((p3 + OFFSETX, p1 + OFFSETY), (p3 + OFFSETX, p2 + OFFSETY), LINEWIDTH, color)
    canvas.draw_line((p4 + OFFSETX, p1 + OFFSETY), (p4 + OFFSETX, p2 + OFFSETY), LINEWIDTH, color)

    # horizontale Linien
    canvas.draw_line((p1 + OFFSETX, p3 + OFFSETY), (p2 + OFFSETX, p3 + OFFSETY), LINEWIDTH, color)
    canvas.draw_line((p1 + OFFSETX, p4 + OFFSETY), (p2 + OFFSETX, p4 + OFFSETY), LINEWIDTH, color)

def drawX( canvas, row, col ):
    '''
    ' Draw an item at the given position in the board on the screen
    ' :param: canvas The canvas to draw on
    ' :param: row The row (number from 0 to 2, inclusive) of the item
    ' :param: col The column (number from 0 to 2, inclusive) of the item
    '''
    global GAMESIZE, LINEWIDTH, OFFSETX, OFFSETY
    global colors, radiuses, radiusColors
    
    # Konstanten zum Zeichnen
    fieldSize = GAMESIZE / 3 
    
    # Mitte des aktuellen Felds
    x = (col * fieldSize + fieldSize / 2) + OFFSETX
    y = (row * fieldSize + fieldSize / 2) + OFFSETY
    canvas.draw_circle((x, y), radiuses[row][col], 5, radiusColors[row][col], colors[row][col])

def drawO( canvas, row, col ):
    '''
    ' Draw an item at the given position in the board on the screen
    ' :param: canvas The canvas to draw on
    ' :param: row The row (number from 0 to 2, inclusive) of the item
    ' :param: col The column (number from 0 to 2, inclusive) of the item
    '''
    global GAMESIZE, LINEWIDTH, OFFSETX, OFFSETY
    global colors, radiuses, radiusColors
    
    # Konstanten zum Zeichnen
    fieldSize = GAMESIZE / 3
    
    # Mitte des aktuellen Felds
    x = (col * fieldSize + fieldSize / 2) + OFFSETX
    y = (row * fieldSize + fieldSize / 2) + OFFSETY
    canvas.draw_circle((x, y), radiuses[row][col], 5, radiusColors[row][col], colors[row][col])
    
def draw( canvas ):
    '''
    ' Zeichnet Feld und Spielzuege und alle Anzeigen
    ' :param: canvas
    '''
    
    global board, spielerAnzeige, WINDOWY, AI_MODE
    global FIRSTCOLOR, SECONDCOLOR, wins, played, draws
    global TICKS, background
    
    if background:
        t = TICKS % 360
        hsl = "hsl("+str(t)+",100%, 80%)"
        canvas.draw_polygon(
            [(0,0),(0,WINDOWX),(WINDOWX,WINDOWY),(0,WINDOWY)],
            10000,
            hsl)
        TICKS+= 2
    
    # zeichne Spielfeld
    drawField( canvas )
    color = ''
    if player == 1:
        color = FIRSTCOLOR
    elif player == -1:
        color = SECONDCOLOR
    playerOneWins = str(wins[0])
    playerOneLost = str(wins[1])
    drawsString = str(draws)
    if played > 0:
        playerOneWins += " (" + str(int(float(wins[0]) / float(played) * float(100))) + " Prozent)"
        playerOneLost += " (" + str(int(float(wins[1]) / float(played) * float(100))) + " Prozent)"
        drawsString += " (" + str(int(float(draws) / float(played) * float(100))) + " Prozent)"
    canvas.draw_text(spielerAnzeige, (200, 50), 48, color, 'sans-serif')
    canvas.draw_text(bigMessage, (250, WINDOWY - 50), 48, "green", 'sans-serif')
    canvas.draw_text("Spieler 1 Stats", (20, 70), 30, FIRSTCOLOR, 'sans-serif')
    canvas.draw_text("Wins: " + playerOneWins, (20, 90), 20, FIRSTCOLOR, 'sans-serif')
    canvas.draw_text("Draws: " + drawsString, (20, 110), 20, FIRSTCOLOR, 'sans-serif')
    canvas.draw_text("Lost: " + playerOneLost, (20, 130), 20, FIRSTCOLOR, 'sans-serif')
    secondStats = "Spieler 2 Stats"
    if not AI_MODE is 0: secondStats = "Computer Stats"
    canvas.draw_text(secondStats, (20, WINDOWY-120), 30, SECONDCOLOR, 'sans-serif')
    canvas.draw_text("Wins: " + playerOneLost, (20,  WINDOWY-100), 20, SECONDCOLOR, 'sans-serif')
    canvas.draw_text("Draws: " + drawsString, (20,  WINDOWY-80), 20, SECONDCOLOR, 'sans-serif')
    canvas.draw_text("Lost: " + playerOneWins, (20,  WINDOWY-60), 20, SECONDCOLOR, 'sans-serif')
    # Hier muessen jetzt die Spielzuege gezeichnet
    # werden. Schaue dir dazu die Funktion 
    # printBoard() an!
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == -1:
                drawX(canvas, row, col)
            elif board[row][col] == 1:
                drawO(canvas, row, col)
    
def makeMoreBlue(row, col, ticks):
    global colors
    redOrGreen = 255 - (ticks * 5) - 5
    color = "rgb(" + str(redOrGreen) + "," + str(redOrGreen) + ",255)"
    colors[row][col] = color

def makeMoreRed(row, col, ticks):
    global colors
    blueOrGreen = 255 - (ticks * 5) - 5
    color = "rgb(255," + str(blueOrGreen) + "," + str(blueOrGreen) + ")"
    colors[row][col] = color

def makeBigger(row, col, ticks):
    global radiuses, GAMESIZE
    fieldSize = GAMESIZE / 3
    maxSize = fieldSize / 2 - 10
    radiuses[row][col] = (maxSize / 50 * ticks ) + 5
    
def blink(val, color):
    global blinked, blinkTimer, board, colors
    blinked += 1
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == val:
                if blinked % 2 == 0:
                    colors[row][col] = color
                else:
                    colors[row][col] = 'Yellow'
                if blinked == 8:
                    colors[row][col] = color
                    blinkTimer.stop()    
    
def blinkBlue():
    blink(-1, "Blue")

def blinkRed():
    blink(1, "Red")
    
def fadeOutField(row, col, ticks):
    global colors, radiusColors
    c = str(int(float(255) * float(ticks) / float(50)))
    radiusColors[row][col] = "rgb(" + c + "," + c + "," + c + ")"
    color = "rgb(" + c + "," + c + "," + c + ")"
    colors[row][col] = color
    
####################################################
# Augmented Intelligence
####################################################
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

def nextMoveMonteCarlo(board, player, repetitions = 100):
    freeFields = get_empty_fields(board)
    values = evaluate_moves(board, player, repetitions)
    for idx in range(len(values)):
        values[idx] = values[idx][2] * player
    maxValue = max(values)
    maxIndex = values.index(maxValue)
    return freeFields[maxIndex]

def count(board, obj):
    '''
    ' Look how often an object is contained in
    ' a 2-dimensional array
    ' :param: board - a 2d array representing the board
    ' :param: obj - The object to look for
    ' :return: The number of occurences of the object in the board
    '''
    occurences = 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == obj:
                occurences += 1
    return occurences

def nextMoveMiniMax(board, player):
    '''
    ' Recursive function which will use minimax
    ' to find the best next move for a given computer
    '
    ' :param: board - A 2-dimensional array representing the board
    ' :param: player - The player whose turn it currently is.
    '                  This argument should almost
    '                  be -1 for the computer
    ' :return: the best move
    '''

    nextPlayer = player * (-1)
    
    # return if there is a winner
    if not getWinner(board) == 0:
        if player is 1: return -1, (-1, -1)
        else: return 1, (-1, -1)
        
    listOfResults = [] # empty array

    if count(board, 0) == 0: # there is no empty field
        return 0, (-1, -1)

    freeFields = []
    for i in range(len(board)):               # could be also "range(3), but this way
        for j in range(len(board[i])):        # the whole game is more variable, and things
            if board[i][j] == 0:              # like a 4x4 field or so could be implemented
                freeFields.append((i, j))     # more easily
    
    for (i, j) in freeFields:
        
        # loop through all the free fields, set the field to the current player...
        board[i][j] = player
        # ... and call the method recursively
        ret, move = nextMoveMiniMax(board, nextPlayer)
        listOfResults.append(ret)
        
        # set the field back to 0
        board[i][j] = 0
        
    # return the best result depending on whose turn it is
    if player is 1:
        maxPossibleValue = max(listOfResults)
        return maxPossibleValue, freeFields[listOfResults.index(maxPossibleValue)]
    else:
        minPossibleValue = min(listOfResults)
        return minPossibleValue, freeFields[listOfResults.index(minPossibleValue)]
    
####################################################
# Input Handler
####################################################

def resetVars():
    '''
    ' This will reset all needed variables and clear the board
    '''
    global board, player, winner, running, blinkTimer
    global spielerAnzeige, blinked, bigMessage, BIG_MESSAGE_COLOR
    global AI_MODE, radiuses, radiusColors
    player = 1
    if AI_MODE is 0: showCurrentPlayerMessage()
    winner = 0
    running = True
    emptyBoard()
    blinked = 0
    radiuses = [[1,1,1],   # alles 1
         [1,1,1],
         [1,1,1]]
    bigMessage = ''
    BIG_MESSAGE_COLOR = 'Green'
    if not blinkTimer == None:
        blinkTimer.stop()
    radiusColors = [["Black", "Black", "Black"],   # alles schwarz
         ["Black", "Black", "Black"],
         ["Black", "Black", "Black"]]

def newGame():
    '''
    ' This will reset all needed variables, clear the board,
    ' and start a new match.
    '''
    global board
    
    for row in range(len(board)):
        for col in range(len(board[row])):
            FieldAnimation( 50, 20, fadeOutField, row, col).start()
    Delay(2 * 1000, resetVars).start()
    
def getMove( inString ):
    '''
    ' Handles the user's input, makes the move
    ' and checks if the game should end.
    ' :param: inString - enthaelt Eingabe aus dem 
    '                    Textfeld
    '''
    global board, winner, bigMessage, player, running
    global spielerAnzeige, FIRSTCOLOR, SECONDCOLOR, blinkTimer
    global AI_MODE, played, draws, wins
    global AUTO_RESTART, restarting
    
    # only handle an input if the game is running
    if not running:
        return
    
    (row, col) = convertMove( inString )
    
    # if the move was invalid (e.g. the fields is
    # already taken)
    if makeMove(board, row, col) == None:
        if not AI_MODE is 0:
            return
        
        # play the error sound
        global errorSound
        errorSound.rewind()
        errorSound.play()
        return
    
    global plopSound
    plopSound.rewind()
    plopSound.play()
    
    # start the animation which will change
    # the field's color from white to either
    # blue or red ( player is -1 or 1 )
    animationMethod = makeMoreBlue if player is -1 else makeMoreRed
    animation = FieldAnimation(50, 10, animationMethod, row, col)
    animation.start()
    
    bigger = FieldAnimation(50, 10, makeBigger, row, col)
    bigger.start()
    
    if endGame(board):
        spielerAnzeige = ""
        
        # change the statistics
        played += 1
        if winner == 1:
            wins[0] += 1
            bigMessage = "Spieler Rot hat gewonnen!"
            blinkTimer = simplegui.create_timer(500, blinkRed)
            blinkTimer.start()
        elif winner == -1:
            wins[1] += 1
            if not AI_MODE is 0:
                bigMessage = "Der Computer war zu gut!"
            else:
                bigMessage = "Spieler Blau war einfach besser!"
            blinkTimer = simplegui.create_timer(500, blinkBlue)
            blinkTimer.start()
        # It's a draw...
        else:
            draws += 1
            bigMessage = "UNENTSCHIEDEN"
        if AUTO_RESTART:
            
            # 4.5 seconds if the method should wait
            # for the "blinking" to finish
            # (so there has to be a winner),
            # 1 second if the game ended as a draw
            time = 4500 if not winner is 0 else 1000
            
            Delay(time, newGame).start()
        return
    
    # at this point there is no winner
    # so far AND it's not a draw
    
    changePlayer()
    
    # check if it's the computer's turn
    if not AI_MODE is 0 and player == -1:
        
        # predefined positions for the first turn
        # of the computer, because otherwise
        # there would be too much time spent on
        # calculating it.
        if count(board,1) is 1:
            if board[1][1] is 0:
                move = (1,1)
            else:
                # some randomness for the corners
                # as it doesnt depend at all
                # because of the symmetry
                global corners
                move = random.choice(corners)
        else:
            # use minimax to get the next move for
            # the current board
            if AI_MODE is 1:
                move = nextMoveMiniMax(board, player)[1]
            elif AI_MODE is 2:
                move = nextMoveMonteCarlo(board, player, 800)
            
        string = str(move[0]) + str(move[1])
        # short delay to make it look a bit more like
        # a real player ( 0.6 to 1.3 seconds )
        delay_time = random.randint(600,1300)
        delay = Delay(delay_time, getMove, string)
        delay.start()
        
    # update the "current player message", but only
    # if the match is not versus the AI
    if AI_MODE is 0: showCurrentPlayerMessage()
        
def toggleAutoRestart():
    '''
    ' This will set AUTO_RESTART to the
    ' opposite of the current value
    '''
    global AUTO_RESTART
    AUTO_RESTART = not AUTO_RESTART

def mouseHandler( pos ):
    '''
    ' Handles the user's mouse click, only if the game is running
    ' :param: pos - Tupel mit Koordinaten des Mausclicks 
    '               pos[0] - x-Koordinate
    '               pos[1] - y-Koordinate
    '''

    global WINDOWX, WINDOWY, GAMESIZE, OFFSETX, OFFSETY
    global LINEWIDTH, board, running, AI_MODE, player
    
    # only continue if the game is running
    if not running:
        return
    
    #cancel if it's the computer's move
    if not AI_MODE is 0 and player == -1:
        return
    
    x = pos[0] - OFFSETX
    y = pos[1] - OFFSETY
    
    # Check if the clicked position is inside the actual game
    if x < 0 or y < 0 or x > GAMESIZE or y > GAMESIZE:
        return
    fieldSize = GAMESIZE / 3
    row = int(y/fieldSize)%3
    col = int(x/fieldSize)%3
    getMove(str(row) + str(col))
    
def setComputer(mode):
    global AI_MODE, running, wins, played, draws, board
    if running and not isEmptyBoard(board):
        global errorSound
        errorSound.rewind()
        errorSound.play()
        return
    if mode is AI_MODE: return
    if not mode is 0:
        global spielerAnzeige
        spielerAnzeige = ""
    else:
        showCurrentPlayerMessage()
    
    # reset stats
    wins = [0, 0]
    played = 0
    draws = 0
    AI_MODE = mode
    
def computerMinimax():
    setComputer(1)

def computerMonteCarlo():
    setComputer(2)

def computerOff():
    setComputer(0)
    
def toggleBackground():
    global background
    background = not background
            
            
####################################################
# Setup and start frame
####################################################
frame = simplegui.create_frame("Home", WINDOWX, WINDOWY)
frame.set_canvas_background('White')

frame.add_input('Zug', getMove, 100)

frame.add_button("Start New Game", newGame)
frame.add_button("Computer ausschalten", computerOff)
frame.add_button("Computer MiniMax modus", computerMinimax)
frame.add_button("Computer MonteCarlo modus", computerMonteCarlo)

# Commented out because I think it's better
# when the game will always restart on its own 
#frame.add_button("Toggle AutoRestart", toggleAutoRestart)

frame.add_button("Toggle Background", toggleBackground)

frame.set_draw_handler(draw)
frame.set_mouseclick_handler( mouseHandler )


####################################################
# Starte GUI und Tests
####################################################

#testFunction()

# Start the frame animation
frame.start()
resetVars()

# Start the music's timer
playMusic()
simplegui.create_timer(1000 * (60 + 41), playMusic).start()