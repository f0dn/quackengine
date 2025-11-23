from piece import Color, Piece
from move import Move

class Board:
    def __init__(self, fen):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = Color.WHITE
        self.castling_avail: dict[Color, set[Piece]] = {Color.BLACK : set(), Color.WHITE: set()}
        self.recent_en_passant_target: tuple[int, int] | None = None
        self.halfmove_clock = 0
        self.fullmoves = 1

        row = 0
        col = 0
        
        params = []
        params = fen.split()

        for char in params[0]:
            if col == 9:
                col = 0

            if char == "/":
                row += 1
                col = 0
            elif char.isdigit():
                for _ in range(int(char)):
                    self.board[row][col] = None
                    col += 1
            else:
                self.board[row][col] = (Piece(char), Color.WHITE) if char.isupper() else (Piece(char.upper()), Color.BLACK)

                col += 1
        
        self.turn = Color(params[1])
        for char in params[2]:
            if char == "-":
                break
            elif char.isupper():
                self.castling_avail[Color.WHITE].add(Piece(char.upper()))
            elif char.islower():
                self.castling_avail[Color.BLACK].add(Piece(char.upper()))
        if params[3] == "-":
            pass
        else:
            self.recent_en_passant_target = tuple[ord(params[3][0]) - ord('a'), int(params[3][1])-1]
        self.halfmove_clock = int(params[4])
        self.fullmoves = int(params[5])

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
        fen += " " + self.turn.value

        # Third Field: castling availability
        fen += " "
        arr = sorted(map(lambda x: x.value, list(self.castling_avail[Color.WHITE])))
        fen += "".join(arr)
        arr2 = sorted(map(lambda x: x.value.lower(), list(self.castling_avail[Color.BLACK])))
        fen += "".join(arr2)
        if len(arr) == 0 and len(arr2) == 0:
            fen += "-"

        # Fourth Field: en passant target square
        if self.recent_en_passant_target is None:
            fen += " -"
        else:
            fen += " " + chr(self.recent_en_passant_target[0] + ord('a')) + (self.recent_en_passant_target[1]+1)

        # Fifth Field: halfmove clock
        fen += " " + str(self.halfmove_clock)

        # Sixth Field: number of fullmove
        fen += " " + str(self.fullmoves)

        self.fen = fen
        return fen

    def get_possible_moves():
        pass

    def make_moves(self, moves: list[Move]):
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