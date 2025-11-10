from enum import Enum

class Color(Enum):
    WHITE = 0
    BLACK = 1

class Piece(Enum):
    PAWN = 'P'
    KNIGHT = 'N'
    BISHOP = 'B'
    ROOK = 'R'
    QUEEN = 'Q'
    KING = 'K'
    def piece_value(self):
        if self == Piece.PAWN:
            return 1
        if self == Piece.BISHOP:
            return 3
        if self ==Piece.KNIGHT:
            return 3
        if self == Piece.ROOK:
            return 5
        if self == Piece.QUEEN: 
            return 9 
        if self == Piece.KING:
            return 100000000000000000000000000000000000
