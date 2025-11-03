from piece import Color, Piece
from move import Move

class Board:
    board = [[None for _ in range(8)] for _ in range(8)]
    turn = "w"
    castling_avail = "KQkq"
    recent_en_passant_target = "-"
    halfmove_clock = 0
    fullmoves = 1
    fen = ""

    def __init__(self, fen):
        self.fen = fen
        self.from_fen(fen)

    def from_fen(self, fen):
        row = 0
        col = 0

        for idx in range(0, fen.index(" ")):
            if (col == 9):
                col = 0

            if (fen[idx] == "/"):
                row += 1
                col = 0
            elif (fen[idx].isdigit()):
                for _ in range(int(fen[idx])):
                    self.board[row][col] = None
                    col += 1
            else:
                self.board[row][col] = (Piece(fen[idx]), Color.WHITE) if fen[idx].isupper() else (Piece(fen[idx].upper()), Color.BLACK)

                col += 1

    def to_fen(self):
        fen = ""

        # Getting where the pieces are from the board
        rows = [] 
        for row in self.board:
            empty = 0
            fen_row = ""

            for square in row:
                if square is None:
                    empty += 1
                else:
                    if empty > 0:
                        fen_row += str(empty)
                        empty = 0
                    
                    piece, color = square
                    symbol = piece.value.lower() if color == Color.BLACK else piece.value

                    fen_row += symbol
            
            if empty > 0:
                fen_row += str(empty)
            
            rows.append(fen_row)

        # First Field: piece placement
        fen = '/'.join(rows)

        # Can be "compressed" to reduce the lines
        # Second Field: active color
        fen += " " + self.turn

        # Third Field: castling availability
        fen += " " + self.castling_avail

        # Fourth Field: en passant target square
        fen += " " + self.recent_en_passant_target

        # Fifth Field: halfmove clock
        fen += " " + str(self.halfmove_clock)

        # Sixth Field: number of fullmove
        fen += " " + str(self.fullmoves)

        self.fen = fen
        return fen

    def get_possible_moves():
        pass

    def make_moves(self, moves: list[Move]):
        col_num = {
            "a" : 0,
            "b" : 1,
            "c" : 2,
            "d" : 3,
            "e" : 4,
            "f" : 5,
            "g" : 6,
            "h" : 7
        }

        for move in moves:
            from_x, from_y = move.src_coords
            to_x, to_y = move.target_coords

            if move.promoted_to: # promotion move
                color = (self.board[from_x][from_y])[1]

                self.board[from_x][from_y] = None
                self.board[to_x][to_y] = (move.promoted_to, color)
            else:
                moving_piece = self.board[from_x][from_y]

                self.board[from_x][from_y] = None
                self.board[to_x][to_y] = move.chess_piece

                if moving_piece[0] == Piece.KING and abs(from_x - to_x) == 2: # castling move
                    if (from_x - to_x < 0): # castling short side
                        self.board[7][from_y] = None
                        self.board[to_x - 1][to_y] = (Piece.ROOK, moving_piece[1])
                    else: # castling long side
                        self.board[0][from_y] = None
                        self.board[to_x + 1][to_y] = (Piece.ROOK, moving_piece[1])