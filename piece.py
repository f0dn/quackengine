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
