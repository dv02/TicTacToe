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

# speaker draw variables
SPEAKER_OFFSET_X = 60
SPEAKER_OFFSET_Y = 100
SPEAKER_DISTANCE_Y = 200
SPEAKER_SIZE= 40



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

PREFIX = "http://5.189.177.192/info/"

# sounds
VOLUME = 0.7
errorSound = simplegui.load_sound(PREFIX+'error.mp3')
errorSound.set_volume(VOLUME)
plopSound = simplegui.load_sound(PREFIX+'plop.mp3')
plopSound.set_volume(VOLUME)
backGroundMusic  = simplegui.load_sound(PREFIX+'background.mp3')
backGroundMusic.set_volume(VOLUME)

# images
speakerQuiet = simplegui.load_image(PREFIX+'speaker_quiet.png')
speakerLoud = simplegui.load_image(PREFIX+'speaker_loud.png')

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

def maxOfTwo(a,b):
    '''
    Get the bigger value of the two variables
    
    Arguments:
        a {int,float,double} -- The first value
        b {int,float,double} -- The second value
    '''
    if a > b: return a
    else: return b

def minOfTwo(a,b):
    '''
    Get the lower value of the two variables
    
    Arguments:
        a {int,float,double} -- The first value
        b {int,float,double} -- The second value
    '''
    if a < b: return a
    else: return b

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
        assert(maxTicks >= 0, "maxTicks must be a positive value!")
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
        if self.ticks == 1:     # break if the timer already ticked once
            self.timer.stop()
            return

        # call the passed function with the given argument
        if self.arg == None:
            self.action()
        else:
            self.action(self.arg)
        self.ticks += 1     # increment the ticks so that it'll break in the next execution
    
    def start(self):
        self.timer.start()
    
    def __init__(self, delay, action, arg = None):
        '''
        ' Creates a new timer, does NOT start it
        ' :param: delay - The delay of the timer
        ' :param: action - The action which will be called each tick
        ' :param: arg - The Argument the method will be called with
        '''
        assert(delay >= 0, "the delay must be a positive value!")
        self.delay = delay
        self.arg = arg
        self.action = action
        self.timer = simplegui.create_timer(delay, self.doTick)
        
def copy_list(liste):
    '''
    Create a copy of the list.
    Attention: If the list's values are lists themselves,
    it will return a list containing the exact same content,
    so that no new object gets created,
    but existing object references get put into the list.
    
    Arguments:
        liste {list} -- The list which should be copied
    
    Returns:
        list -- A new list containg all the values of the "liste"
    '''
    newList = []
    for val in liste:
        newList.append(val)
    return newList

def copy_board(board):
    '''
    Create a new version of this board but maintaining
    the old values. Hence, the resulting board will
    look exactly the same as the original, but it's
    a new list with a new reference to the list.
    Calls #copy_list(liste)
    
    Arguments:
        board {list} -- The original board (2d list)
    
    Returns:
        list -- The copy of the original board (2d list)
    '''
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
            if not entry == 0:      # break as soon as there is an empty field
                return False
    return True

def testFunction():
    '''
    Short testing function for all the different
    methods regarding the main game logic
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
    
    # This will throw an index out of bounds!
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
    
    
    
    
    # Teste KI (nextMoveMiniMax and nextMoveMonteCarlo)
    for i in range(7): print
    print "TESTE KUENSTLICHE INTELLIGENZ\n"
    
    testBoard = [[ 1, 1,-1],
                 [-1, 1, 1],
                 [ 1,-1,-1]]
    print "teste nextMoveMiniMax und nextMoveMonteCarlo mit Player = 1, board:"
    printBoard(testBoard)
    print "Ergebnis nextMoveMiniMax: " + str(nextMoveMiniMax(testBoard, 1))
    print "Ergebnis nextMoveMonteCarlo: " + str(nextMoveMonteCarlo(testBoard, 1, 800))
    print
    
    
    
    testBoard = [[ 1, 1, 0],
                 [-1, 1, 1],
                 [ 1,-1,-1]]
    print "teste nextMoveMiniMax und nextMoveMonteCarlo mit Player = 1, board:"
    printBoard(testBoard)
    print "Ergebnis nextMoveMiniMax: " + str(nextMoveMiniMax(testBoard, 1))
    print "Ergebnis nextMoveMonteCarlo: " + str(nextMoveMonteCarlo(testBoard, 1, 800))
    print
    
    
    
    testBoard = [[ -1, -1, 0],
                 [ 0, 0, 0],
                 [ 1, 1, 0]]
    print "teste nextMoveMiniMax und nextMoveMonteCarlo mit Player = -1, board:"
    printBoard(testBoard)
    print "Ergebnis nextMoveMiniMax: " + str(nextMoveMiniMax(testBoard, -1))
    print "Ergebnis nextMoveMonteCarlo: " + str(nextMoveMonteCarlo(testBoard, -1, 800))
    print
    
    for i in range(7): print
    print "\n---- END TESTS ----"

def printBoard( board ):
    '''
    Prints out the board in the following format:
         X | . | O 
        ---|---|---
         . | X | . 
        ---|---|---
         X | O | O 
    
    Arguments:
        board {list} -- The board (2d list)
    '''
    print
    idx = 0
    for line in board:
        jdx = 0
        string = ''
        for field in line:
            if field == 0:
                string += ' . '
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
    Convert the string to a list containing two ints:
    The row and the column the string stands for.
    
    Arguments:
        string {string} -- enthaelt Koordinaten im Format
              '00', also zwei Zahlen. Die erste steht
              fuer die Reihe, das zweite ist die Zeile.
    
    Returns:
        list -- A list containg 2 ints which stand for the row and the column
    '''
    if not len(string) == 2:
        return (-1, -1)
    # muss int sein
    try: 
        return (int(string[0]), int(string[1]))
    except ValueError:
        return (-1, -1)
    return (-1, -1)

####################################################
# Spiellogik
####################################################
def makeMove( board, row, col):
    '''x
    Sets the field at the given location to the current player
    
    Arguments:
        board {list} -- The board (2d list)
        row {int} -- The row of the field
        col {int} -- The column of the field
    
    Returns:
        list -- The new, modified board if everything was fine, or None, if the selected field is already taken
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
    canvas.draw_line((p1 + OFFSETX, p1 + OFFSETY), (p1 + OFFSETX, p2 + OFFSETY), LINEWIDTH, color)
    canvas.draw_line((p1 + OFFSETX, p2 + OFFSETY), (p2 + OFFSETX, p2 + OFFSETY), LINEWIDTH, color)
    canvas.draw_line((p2 + OFFSETX, p1 + OFFSETY), (p2 + OFFSETX, p2 + OFFSETY), LINEWIDTH, color)
    canvas.draw_line((p1 + OFFSETX, p1 + OFFSETY), (p2 + OFFSETX, p1 + OFFSETY), LINEWIDTH, color)
    
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
    
def drawBackground(canvas):
    '''
    Draw the rainbow background on the given canvas
    
    Arguments:
        canvas {canvas} -- The canvas to draw on
    '''

    global TICKS

    t = TICKS % 360
    # convert the ticks to a number
    # from 0 to 359 that we can use for the css "hsl" function.

    # use the css function with 100% saturation and 80% light
    hsl = "hsl("+str(t)+", 100%, 80%)"

    # draw a huge rectangle the fill the whole screen
    canvas.draw_polygon(
        [(0,0),(0,WINDOWX),(WINDOWX,WINDOWY),(0,WINDOWY)],
        10000,
        hsl)
    TICKS+= 2

def drawSpeakerSymbols(canvas):
    global SPEAKER_OFFSET_X, SPEAKER_OFFSET_Y, SPEAKER_DISTANCE_Y
    global WINDOWY, WINDOWX, SPEAKER_SIZE, speakerQuiet, speakerLoud
    global VOLUME

    width = speakerLoud.get_width()
    height = speakerLoud.get_height()

    # break if the image isn't loaded yet
    if width == 0:
        return
    center_dest_x = WINDOWX - SPEAKER_OFFSET_X
    center_dest_y = SPEAKER_OFFSET_Y

    p1 = center_dest_x - 10
    p2 = center_dest_x
    p3 = center_dest_y + SPEAKER_DISTANCE_Y - 25
    p4 = center_dest_y + 25


    canvas.draw_polygon(
        [(p1, p3), (p2, p3), (p2, p4), (p1,p4) ],
        10,
        "#CCE3EB")

    if VOLUME > 0:
        p5 = p4 + int(((1.0-VOLUME) * float(SPEAKER_DISTANCE_Y-25-SPEAKER_SIZE)))
        canvas.draw_polygon(
            [(p1, p3), (p2, p3), (p2, p5), (p1,p5) ],
            4,
            "blue")


    canvas.draw_image(speakerLoud,(width/2,height/2),(width, height),(center_dest_x, center_dest_y),(SPEAKER_SIZE,SPEAKER_SIZE))

    canvas.draw_image(
        speakerQuiet,
        (width/2,height/2),
        (width, height),
        (center_dest_x, center_dest_y + SPEAKER_DISTANCE_Y),
        (SPEAKER_SIZE,SPEAKER_SIZE))

def draw( canvas ):
    '''
    ' Zeichnet Feld und Spielzuege und alle Anzeigen
    ' :param: canvas
    '''
    

    # draw the rainbow background if the global flag is set
    if background:
        drawBackground(canvas)

    drawSpeakerSymbols( canvas )
    
    # zeichne Spielfeld
    drawField( canvas )

    color = ''
    if player == 1:
        color = FIRSTCOLOR
    elif player == -1:
        color = SECONDCOLOR


    # draw all the statistics for player 1
    playerOneWins = str(wins[0])
    playerOneLost = str(wins[1])
    drawsString = str(draws)
    if played > 0:
        playerOneWins += " (" + str(int(float(wins[0]) / float(played) * 100.0)) + " Prozent)"
        playerOneLost += " (" + str(int(float(wins[1]) / float(played) * 100.0)) + " Prozent)"
        drawsString += " (" + str(int(float(draws) / float(played) * 100.0)) + " Prozent)"
    canvas.draw_text(spielerAnzeige, (200, 50), 48, color, 'sans-serif')
    canvas.draw_text(bigMessage, (250, WINDOWY - 50), 48, "green", 'sans-serif')
    canvas.draw_text("Spieler 1 Stats", (20, 70), 30, FIRSTCOLOR, 'sans-serif')
    canvas.draw_text("Wins: " + playerOneWins, (20, 90), 20, FIRSTCOLOR, 'sans-serif')
    canvas.draw_text("Draws: " + drawsString, (20, 110), 20, FIRSTCOLOR, 'sans-serif')
    canvas.draw_text("Lost: " + playerOneLost, (20, 130), 20, FIRSTCOLOR, 'sans-serif')



    # draw all the statistics for player 2
    secondStats = "Spieler 2 Stats"
    if not AI_MODE is 0: secondStats = "Computer Stats"
    canvas.draw_text(secondStats, (20, WINDOWY-120), 30, SECONDCOLOR, 'sans-serif')
    canvas.draw_text( "Wins: " + playerOneLost, ( 20,  WINDOWY - 100 ), 20, SECONDCOLOR, 'sans-serif' )
    canvas.draw_text( "Draws: " + drawsString, ( 20,  WINDOWY - 80 ), 20, SECONDCOLOR, 'sans-serif' )
    canvas.draw_text( "Lost: " + playerOneWins, ( 20,  WINDOWY - 60 ), 20, SECONDCOLOR, 'sans-serif' )
   

    # draw all circles inside of the fields   
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == -1:
                drawX(canvas, row, col)
            elif board[row][col] == 1:
                drawO(canvas, row, col)
    
def makeMoreBlue(row, col, ticks):
    '''Animation tick function which will make the specific field a bit more blue, depending on the ticks
        
    Arguments:  
        row {[int]} -- [The row of the field]
        col {[int]} -- [The col of the field]
        ticks {[int]} -- [The ticks passed since the timer was started]
    '''
    global colors
    redOrGreen = 255 - (ticks * 5) - 5
    color = "rgb(" + str(redOrGreen) + "," + str(redOrGreen) + ",255)"
    colors[row][col] = color

def makeMoreRed(row, col, ticks):
    '''Animation tick function which will make the specific field a bit more red, depending on the ticks
        
    Arguments:  
        row {[int]} -- [The row of the field]
        col {[int]} -- [The col of the field]
        ticks {[int]} -- [The ticks passed since the timer was started]
    '''
    global colors
    blueOrGreen = 255 - (ticks * 5) - 5
    color = "rgb(255," + str(blueOrGreen) + "," + str(blueOrGreen) + ")"
    colors[row][col] = color

def makeBigger(row, col, ticks):
    '''Animation tick function which will make the specific field a bit bugger, depending on the ticks
        
    Arguments:  
        row {[int]} -- [The row of the field]
        col {[int]} -- [The col of the field]
        ticks {[int]} -- [The ticks passed since the timer was started]
    '''
    global radiuses, GAMESIZE
    fieldSize = GAMESIZE / 3
    maxSize = fieldSize / 2 - 10
    radiuses[row][col] = (maxSize / 50 * ticks ) + 5
    
def blink(val, color):
    '''
    This function will set a field's color either to its original color or
    to "Yellow", depending on the ticks passed since the timer was started.
    
    Arguments: 
        color {String} -- The original color of the field
        val {int} -- The value of the field (whether it's occupied by player 1 or -1)
    '''
    global blinked, blinkTimer, board, colors
    blinked += 1
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == val:
                if blinked % 2 == 0:    # change the color every second time
                    colors[row][col] = color
                else:
                    colors[row][col] = 'Yellow'
                if blinked == 8:
                    colors[row][col] = color
                    blinkTimer.stop()
    
def blinkBlue():
    '''
    Shortcut function calling #blink(val,color) with "Blue" as the color
    '''
    blink(-1, "Blue")

def blinkRed():
    '''
    Shortcut function calling #blink(val,color) with "Red" as the color
    '''
    blink(1, "Red")
    
def fadeOutField(row, col, ticks):
    '''
    Changes the color and radius color of the field at
    the given row / col to a rgb value (0 - 255).
    This value depends on how many ticks have passed since
    the timer was started. The color will always be a grayish one,
    so all the r,g and b values are equal.
    
    Arguments:
        row {int} -- The row of the field
        col {int} -- The column of the field
        ticks {int} -- The ticks which have passed since the timer was started
    '''
    global colors, radiusColors

    # 255 should be the maximum value, 50.0 is used because
    # it should update every 50 milliseconds
    c = str(  int(  255.0 * float(ticks) / 50.0  )  )

    color = "rgb("+c+","+c+","+c+")"
    colors[row][col] = color
    radiusColors[row][col] = color
    
####################################################
# Augmented Intelligence
####################################################
def get_empty_fields(board):
    '''
    Loops through the board and returns a list of lists, saying which fields in the board are empty.
    
    Arguments:
        board {list} -- The board (2 dimensional array)
    
    Returns:
        list -- A list of lists which consist of 2 ints, determining the position of the empty field. Example: [ (0,0), (1,2), (2,1) ]
    '''
    fields = []   # instantiate the list
    for row in range(3):        # loop through all elements of the board
        for col in range(3):
            if board[row][col] == 0:    # check if the element is empty, then append it to the list
                fields.append((row,col))
    return fields

def random_move(board, player):
    '''
    Fills up the board with random moves as long as there
    is no winner. Useful for the MonteCarlo AI.
    
    Arguments:
        board {list} -- The board (2d list)
        player {int} -- An int determining the player (-1 or 1)
    
    Returns:
        number -- The winner of the created situation
    '''
    result = 0
    while result == 0:
        emptyFields = get_empty_fields(board)
        if emptyFields == []:   # if there is no empty field, it's a draw, so we return 0 here.
            return 0

        move = random.choice(emptyFields)      # make a move at one random of these fields.
        board[move[0]][move[1]] = player
        player*=-1      # change the player, so that is opponent will make a random move in the next loop

        result = getWinner(board)
    return result

def simulate_moves(board, player, repetitions = 100):
    '''
    Make x repetitions (x = repetitions), make a random move at each of
    them and store whether the player has lost, won, or if it's a draw.
    
    Arguments:
        board {list} -- The board (2d list)
        player {int} -- The player (-1 or 1)
    
    Keyword Arguments:
        repetitions {number} -- The number of repetitions (default: {100})
    
    Returns:
        list -- A list containg 3 ints (lost, draw, won)
    '''
    counter = [0, 0, 0]     # instantiate the counting list
    while repetitions > 0:
        newBoard = copy_board(board)        # I dont really want to modify the real board (this method will be "call-by-reference")
        result = random_move(newBoard, player)         # evaluate the random move and store its result
        counter[ result + 1 ] += 1
        # a bit hacky: count up the element in the list which is at the
        # "result+1"-th position (if the result is -1 its 0,
        # if it's 0 the position is 1, if the result is 1 the position will be 0)
        
        repetitions -= 1
    return counter

def evaluate_moves(board, player, repetitions = 100):
    '''
    Get the results of all the different random moves
    
    Arguments:
        board {list} -- The board (2d list)
        player {int} -- The player (-1 or 1)
    
    Keyword Arguments:
        repetitions {number} -- How often the random function should be called (higher repetitions => better move) (default: {100})
    
    Returns:
        list -- List of lists containg 3 ints (lost, draws, wins) which are the results of #simulate_moves(board, player, repetitions)
    '''
    freeFields = get_empty_fields(board)    # get all the empty fields
    results = []

    for field in freeFields:
        board[field[0]][field[1]] = player      # set the field to the player's value
        result = simulate_moves(board, player, repetitions)
        # go through all the possible combinations of this field and get their results

        results.append(result)
        board[field[0]][field[1]] = 0       # "undo" the move, so that the board remains the same.

    return results

def nextMoveMonteCarlo(board, player, repetitions = 100):
    '''
    Get the best move for a given player in a given
    situation using the Monte Carlo algorithm
    
    Arguments:
        board {list} -- The board (2d list)
        player {int} -- The player (-1 or 1)
    
    Keyword Arguments:
        repetitions {number} -- The number of repetitions. The higher it is, the better the resulting move will be (default: {100})
    
    Returns:
        list -- A list containg 2 ints which stand for the row and the column of the calculated best move
    '''
    freeFields = get_empty_fields(board)

    values = evaluate_moves(board, player, repetitions)     # get all of the results
    for idx in range(len(values)):

        # Loop through them and multiply the "wins" value by
        # the current player so that it doesn't really
        # matter which player's turn it is anymore
        values[idx] = values[idx][2] * player

    maxValue = max(values)
    maxIndex = values.index(maxValue)   # get the field which is the most likely to win
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

def addVolume(summand):
    '''
    Increment the volume by the given amount.
    Note: The volume won't be less than 0 or greater than 1.
    This will also change the volume of all sounds.
    
    Arguments:
        summand {float} -- The summand which will be added to the current volume. Can be negative
    '''
    global VOLUME, errorSound, plopSound, backGroundMusic

    VOLUME = maxOfTwo( 0, minOfTwo( 1, VOLUME + summand ) )

    errorSound.set_volume(VOLUME)
    plopSound.set_volume(VOLUME)
    backGroundMusic.set_volume(VOLUME)

def mouseHandler( pos ):
    '''
    ' Handles the user's mouse click, only if the game is running
    ' :param: pos - Tupel mit Koordinaten des Mausclicks 
    '               pos[0] - x-Koordinate
    '               pos[1] - y-Koordinate
    '''

    global WINDOWX, WINDOWY, GAMESIZE, OFFSETX, OFFSETY
    global LINEWIDTH, board, running, AI_MODE, player
    global SPEAKER_OFFSET_X, SPEAKER_OFFSET_Y
    global SPEAKER_SIZE, SPEAKER_DISTANCE_Y, speakerLoud

    center_dest_x = WINDOWX - SPEAKER_OFFSET_X  # get the center of the image
    center_dest_y = SPEAKER_OFFSET_Y

    x = pos[0]
    y = pos[1]

    # declare 4 variables for the upper and lower y coordinate and the left and right x bounds
    left  = ( center_dest_x - ( SPEAKER_SIZE / 2 ) )
    right = ( center_dest_x + ( SPEAKER_SIZE / 2 ) )
    upper = ( center_dest_y - ( SPEAKER_SIZE / 2 ) )
    lower = ( center_dest_y + ( SPEAKER_SIZE / 2 ) )

    # if the x coordinate could be on a speaker symbol
    if x >= left and x <= right:
        # check if it's the upper speaker symbol
        if y >= upper and y <= lower:
            addVolume(0.1)
            return
        # check if it's the lower speaker symbol
        elif y >= upper+SPEAKER_DISTANCE_Y and y <= lower+SPEAKER_DISTANCE_Y:
            addVolume(-0.1)
            return

    # only continue if the game is running
    if not running:
        return
    
    # cancel if it's the computer's move
    if not AI_MODE is 0 and player == -1:
        return
    
    # subtract the offests so that we end up with x and y between 0 and WINDOWX / WINDOWY
    x -= OFFSETX
    y -= OFFSETY
    
    # Check if the clicked position is inside the actual game
    if x < 0 or y < 0 or x > GAMESIZE or y > GAMESIZE:
        return
    fieldSize = GAMESIZE / 3
    row = int( y / fieldSize ) % 3  # break it down into a number from 0 to 2
    col = int( x / fieldSize ) % 3

    # perform the move calling #getMove(inString) with
    # the string value of the field's position
    getMove(str(row) + str(col))
    
def setComputer(mode):
    '''
    Change the AI_MODE to either
    0 => AI is turned off
    1 => AI will use MiniMax algorithm
    2 => AI will use Monte Carlo approach
    , hide the "current player message"
    (because it's obvious that it's almost always the player's turn)
    and reset the statistics if he changes the mode
    
    Arguments:
        mode {int} -- The new mode: 
        0 => AI is turned off
        1 => AI will use MiniMax algorithm
        2 => AI will use Monte Carlo approach
    '''
    global AI_MODE, running, wins, played, draws, board
    # if there's a match running which has already been started,
    # break the method and play an error sound
    if running and not isEmptyBoard(board):
        global errorSound
        errorSound.rewind()
        errorSound.play()
        return

    # Break if the new mode is the same as the old one
    if mode is AI_MODE: return

    if not mode is 0:
        global spielerAnzeige   # reset the current player message
        spielerAnzeige = ""
    else:
        showCurrentPlayerMessage()  # or show it, if the AI is turned off
    
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
    '''
    Set the global background flag to its opposite value.
    The variable will later on be used in #draw(canvas)
    to either draw the rainbow background or not
    '''
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

# testFunction()

# Start the frame animation
frame.start()
resetVars()

# Start the music's timer
playMusic()
simplegui.create_timer(1000 * (60 + 41), playMusic).start()