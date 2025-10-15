from piece import Color, Piece

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