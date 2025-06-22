from castleRights import CastleRights 

class GameState():
    def __init__(self):
        self.board = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR" ],
            ["bp","bp","bp","bp","bp","bp","bp","bp" ],
            ["--","--","--","--","--","--","--","--" ],
            ["--","--","--","--","--","--","--","--" ],
            ["--","--","--","--","--","--","--","--" ],
            ["--","--","--","--","--","--","--","--" ],
            ["wp","wp","wp","wp","wp","wp","wp","wp" ],
            ["wR","wN","wB","wQ","wK","wB","wN","wR" ]
        ]
        self.moveFunctions = {'p':self.getPawnMoves, 'R':self.getRookMoves
                              ,'N': self.getKnightMoves, 'B': self.getBishopMoves, 'Q':self.getQueenMoves,
                              'K': self.getKingMoves}                                                                       
        self.whiteToMove = True
        self.movelog = []
        
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () #sqauares where enpassant is possible
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]



    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)       
        self.whiteToMove = not self.whiteToMove

        #update king location
        if move.pieceMoved == 'wK':
            self.whiteKingLocation = (move.endRow, move.endCol)
        if move.pieceMoved == 'bK':
            self.blackKingLocation = (move.endRow, move.endCol)

        #simple pawn promotion(for now)
        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] +'Q'

        #enpassant
        if move.isEnpassantMove == True:
            self.board[move.startRow][move.endCol] = '--'
        
        #update enpassant possible
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = () # reset to null if another move is made

        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else:   #queenside castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        self.enpassantPossibleLog.append(self.enpassantPossible)

        #update castling rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))


    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            #update king position
            if move.pieceMoved == 'wK':
                self.whiteKingLocation = (move.startRow, move.startCol)
            if move.pieceMoved == 'bK':
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo enpassant
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = '--'
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                

            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            #undo castling rights
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(newRights.wks,newRights.bks,
                                                      newRights.wqs,newRights.bqs)

            #undo castle move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2:# kingside
                    self.board[move.endRow][move.endCol+1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--'
                else: #queenside castle
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = '--'

            self.checkMate = False
            self.staleMate = False

            
    
    def updateCastleRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False

        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.wks = False
        
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0: #left rook
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastlingRights.bks = False

        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False

    def getValidMoves(self):#considering checks
        #generate all possible move
        tempEnpassantPossible = self.enpassantPossible
        tempCastlingRights = CastleRights(self.currentCastlingRights.wks,self.currentCastlingRights.bks,
                                          self.currentCastlingRights.wqs,self.currentCastlingRights.bqs)
        moves = self.getAllPossibleMoves()

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)

        #make the move
        for i in range(len(moves)-1, -1, -1): #going backwards because of possible remove bug
            self.makeMove(moves[i])

            #generate all opponent moves
            
            #see if the king is attacked. if attacked, not valid
            self.whiteToMove = not self.whiteToMove #the make move function switches turns. so need to switch back
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove #to counteract the undomove which also switches turns
            self.undoMove()
        
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:       #for when we undo moves after checkmate or stalemate
            self.checkMate = False
            self.staleMate = False
        
        self.enpassantPossible = tempEnpassantPossible   #save enpassantpossible moves when doing undo
        self.currentCastlingRights = tempCastlingRights

        return moves
    
    #determine if the current player is in check
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    #determing if square r, c is under attack
    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove #switch back turn
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
        

    def getAllPossibleMoves(self):#not considering checks
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == "b" and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r,c,moves) #gets function from dictionary
        return moves
                    
    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:          
            if self.board[r-1][c] == "--":
                moves.append(Move((r,c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == "--":
                    moves.append(Move((r,c), (r-2,c), self.board))
            if c - 1>=0: 
                if self.board[r-1][c-1][0] == "b":
                    moves.append(Move((r,c), (r-1,c-1), self.board))
                if (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r - 1, c - 1), self.board, isEnpassantMove=True))
            if c +1<=7: 
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c), (r-1,c+1), self.board))
                if (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r - 1, c + 1), self.board, isEnpassantMove=True))

        if not self.whiteToMove:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2,c), self.board))
            if c - 1>=0: 
                if self.board[r+1][c-1][0] == "w":
                    moves.append(Move((r,c), (r+1,c-1), self.board))
                if (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c +1<=7: 
                if self.board[r+1][c+1][0] == "w":
                    moves.append(Move((r,c), (r+1,c+1), self.board))   
                if (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r,c), (r + 1, c + 1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):

        if self.whiteToMove:
            ally, enemy = 'w', 'b'
        else:
            ally, enemy = 'b', 'w'

        # 2) four straight‐line directions: down, up, right, left
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                end_row, end_col = r + dr*i, c + dc*i
                # check if still on board
                if not (0 <= end_row < 8 and 0 <= end_col < 8):
                    break
                
                if self.board[end_row][end_col] == "--":
                    # empty square: legal move, keep going
                    moves.append(Move((r, c), (end_row, end_col), self.board))
                else:
                    # occupied: if it's an enemy, capture it; then stop
                    if self.board[end_row][end_col][0] == enemy:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    # whether enemy or ally, we cannot jump past it
                    break
    def getKnightMoves(self, r, c, moves):
        if self.whiteToMove:
            ally, enemy = 'w', 'b'
        else:
            ally, enemy = 'b', 'w'

        # 2) all 8 L-shaped jumps
        knight_offsets = [
            ( 2,  1), ( 2, -1),
            (-2,  1), (-2, -1),
            ( 1,  2), ( 1, -2),
            (-1, 2), (-1, -2)
        ]

        for dr, dc in knight_offsets:
            end_row, end_col = r + dr, c + dc
            # skip off-board
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                if end_piece == "--":
                    # empty: legal move
                    moves.append(Move((r, c), (end_row, end_col), self.board))
                elif end_piece[0] == enemy:
                    # capture possible
                    moves.append(Move((r, c), (end_row, end_col), self.board))
                # if it’s an ally, we just ignore it
    def getBishopMoves(self, r, c, moves):
        if self.whiteToMove:
            ally, enemy = 'w', 'b'
        else:
            ally, enemy = 'b', 'w'

        # Four diagonal directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                end_row = r + dr * i
                end_col = c + dc * i
                # off-board?
                if not (0 <= end_row < 8 and 0 <= end_col < 8):
                    break
                end_piece = self.board[end_row][end_col]
                if end_piece == "--":
                    # empty square: legal move
                    moves.append(Move((r, c), (end_row, end_col), self.board))
                else:
                    # occupied: if it’s an enemy, we can capture it, then stop
                    if end_piece[0] == enemy:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                    # whether ally or enemy, we cannot go further
                    break   
    def getQueenMoves(self, r, c, moves):
        if self.whiteToMove:
            ally, enemy = 'w', 'b'
        else:
            ally, enemy = 'b', 'w'

        directions = [
            ( 1,  0),  # down
            (-1,  0),  # up
            ( 0,  1),  # right
            ( 0, -1),  # left
            ( 1,  1),  # down-right
            ( 1, -1),  # down-left
            (-1,  1),  # up-right
            (-1, -1)   # up-left
        ]

        for dr, dc in directions:
            for i in range(1, 8):
                end_row = r + dr * i
                end_col = c + dc * i
                # off-board?
                if not (0 <= end_row < 8 and 0 <= end_col < 8):
                    break
                end_piece = self.board[end_row][end_col]
                if end_piece == "--":
                    # empty square: legal move
                    moves.append(Move((r, c), (end_row, end_col), self.board))
                else:
                    # occupied: capture if enemy, then stop
                    if self.board[end_row][end_col][0] == enemy:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
                        break     
                    if self.board[end_row][end_col][0] == ally:
                        break

    def getKingMoves(self, r, c, moves):
        if self.whiteToMove:
            ally, enemy = 'w', 'b'
        else:
            ally, enemy = 'b', 'w'

        # 2) all eight directions, but only one step
        directions = [
            ( 1,  0),  # down
            (-1,  0),  # up
            ( 0,  1),  # right
            ( 0, -1),  # left
            ( 1,  1),  # down-right
            ( 1, -1),  # down-left
            (-1,  1),  # up-right
            (-1, -1)   # up-left
        ]

        for dr, dc in directions:
            end_row, end_col = r + dr, c + dc
            # ensure we're still on the board
            if 0 <= end_row < 8 and 0 <= end_col < 8:
                end_piece = self.board[end_row][end_col]
                # if empty, or occupied by enemy, it's a legal move
                if end_piece == "--" or end_piece[0] == enemy:
                    moves.append(Move((r, c), (end_row, end_col), self.board))

        
    
    #generate all valid castle moves for the king at (r, c)
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r,c):
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks):
            self.getKingsideCastleMoves(r, c, moves)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs):
            self.getQueensideCastleMoves(r, c, moves)
        
    def getKingsideCastleMoves(self, r, c, moves):
        if c + 2 < 8:  # Only proceed if c+2 is within board limits
            if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
                if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c + 2):
                    moves.append(Move((r,c), (r,c+2), self.board, isCastleMove=True))


    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r,c), (r,c-2), self.board, isCastleMove = True))


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0 }
    
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7 }
    
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove=False, isCastleMove=False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        
        
        self.isPawnPromotion = False
        if (self.pieceMoved == 'wp' and self.endRow == 0) or (self.pieceMoved == 'bp' and self.endRow == 7):
            self.isPawnPromotion = True

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            # self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'
            if self.pieceMoved == 'bp':
                self.pieceCaptured = 'wp'
            else:
                self.pieceCaptured = 'bp'

        self.isCastleMove = isCastleMove

        self.moveID = self.startRow * 1000 + self.startCol *100 + self.endRow*10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
