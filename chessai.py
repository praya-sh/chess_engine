import random

pieceScore = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p":1}
CHECKMATE = 1000
STALEMATE = 0

def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]

def findBestMove(gs, validMoves):
    turnMultiplier = 1 if gs.whiteToMove else -1

    maxScore = -CHECKMATE
    bestMove = None
    for playerMove in validMoves:
        gs.makeMove(playerMove)
        if gs.checkMate:
            score = CHECKMATE
        elif gs.staleMate:
            score = STALEMATE
        else:
            score = turnMultiplier * scoreMaterial(gs.board)
        if (score > maxScore):
            score = maxScore
            bestMove = playerMove
        gs.undoMove()
    return bestMove

#score based on material

def scoreMaterial(board):
    score = 0
    for row in board:
        for square in board:
                if square[0] == 'w':
                    score += pieceScore[square[1]]
                elif square[0] == 'b':
                     score -= pieceScore[square[1]]
    return score

