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
        self.castleRights = True

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.movelog.append(move)
        self.whiteToMove = not self.whiteToMove

    def undoMove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):#considering checks
        return self.getAllPossibleMoves()

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
            if c +1<=7: 
                if self.board[r-1][c+1][0] == "b":
                    moves.append(Move((r,c), (r-1,c+1), self.board))

        if not self.whiteToMove:
            if self.board[r+1][c] == "--":
                moves.append(Move((r,c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == "--":
                    moves.append(Move((r,c), (r+2,c), self.board))
                if c - 1>=0: 
                    if self.board[r+1][c-1][0] == "w":
                        moves.append(Move((r,c), (r+1,c-1), self.board))
                if c +1<=7: 
                    if self.board[r+1][c+1][0] == "w":
                        moves.append(Move((r,c), (r+1,c+1), self.board))

    
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
                    if end_piece[0] == enemy:
                        moves.append(Move((r, c), (end_row, end_col), self.board))
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


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                    "5": 3, "6": 2, "7": 1, "8": 0 }
    
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                    "e": 4, "f": 5, "g": 6, "h": 7 }
    
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol *100 + self.endRow*10 + self.endCol


    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self,r,c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
