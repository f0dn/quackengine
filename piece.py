from enum import Enum

class Color(Enum):
    WHITE = "w"
    BLACK = "b"

class Piece(Enum):
    PAWN = 'P'
    KNIGHT = 'N'
    BISHOP = 'B'
    ROOK = 'R'
    QUEEN = 'Q'
    KING = 'K'
