import pygame as p
import chessengine
import chessai

width = height = 512
Dimension = 8
SQ_SIZE = height//Dimension
max_fps = 15
images = {}

#make global dictionary of images

def loadImages():
    pieces = ['wp','wR','wN','wB','wQ','wK','bp','bR','bN','bB','bQ','bK']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("pieces/"+ piece + ".png"),(SQ_SIZE,SQ_SIZE))


def main():
    p.init()
    screen = p.display.set_mode((width, height))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessengine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False
    animate = False

    loadImages()
    running = True
    sqSelected = ()     #no square selected initially
    playerClicks = []   #keep track of player clicks. [(6,2),(4,4)]

    gameOver = False

    playerOne = True #if human playing white: true and if AI playing white false
    playerTwo = False #same but for black

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos()
                    #print(location)
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    if sqSelected == (row, col):    #select the same square twice(unselect)
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row,col)
                        playerClicks.append(sqSelected) #append for first and second clicks
                    if len(playerClicks) == 2:
                        move = chessengine.Move(playerClicks[0], playerClicks[1], gs.board)
                        #print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])   
                                moveMade = True
                                animate = True
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
            
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                if e.key == p.K_r:
                    gs = chessengine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False
                    gameOver = False

            #AI move finder
        if not gameOver and not humanTurn:
            AIMove = chessai.findBestMove(gs, validMoves)
            if AIMove is None:
                AIMove = chessai.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.movelog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False


        drawGameState(screen,gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, 'Black wins')
            else:
                drawText(screen, 'White wins')
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Draw")
    
            
        clock.tick(max_fps)
        p.display.flip()

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sq selected is a piece that can be moved
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)#transparency value: 0 transparen 255 opaque
            s.fill(p.Color('green'))
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            
            #highlight validmoves
            s.fill(p.Color('green'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*SQ_SIZE, move.endRow*SQ_SIZE))
                

def drawGameState(screen,gs, validMoves, sqSelected):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen,gs.board)


def drawBoard(screen):
    global colors
    colors = [p.Color('white'), p.Color("gray")]
    for r in range(Dimension):
        for c in range(Dimension):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 15  # Increase frames for smoother animation
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    
    # Create a copy of the board for animation
    anim_board = [row[:] for row in board]
    # Remove moving piece from start position
    anim_board[move.startRow][move.startCol] = "--"
    
    for frame in range(frameCount + 1):
        # Calculate intermediate position
        progress = frame / frameCount
        r = move.startRow + dR * progress
        c = move.startCol + dC * progress
        
        # Draw the board
        drawBoard(screen)
        
        # Draw all pieces except moving piece
        for row in range(Dimension):
            for col in range(Dimension):
                piece = anim_board[row][col]
                if piece != "--" and (row, col) != (move.endRow, move.endCol):
                    screen.blit(images[piece], p.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
        # Draw captured piece if any
        if move.pieceCaptured != "--" and frame == 0:
            screen.blit(images[move.pieceCaptured], 
                        p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        
        # Draw moving piece at intermediate position
        screen.blit(images[move.pieceMoved], 
                    p.Rect(int(c * SQ_SIZE), int(r * SQ_SIZE), SQ_SIZE, SQ_SIZE))
        
        p.display.flip()
        clock.tick(60)

def drawText(screen, text):
    font = p.font.SysFont("Helvitica", 32, True, False)
    textObject = font.render(text, 0, p.Color('Black'))
    textLocation  = p.Rect(0, 0, width, height).move(width/2 - textObject.get_width()/2, height/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)

if __name__ == "__main__":
    main()


    

