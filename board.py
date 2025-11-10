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

    def get_possible_moves(self):
        """
        Returns a set of possible moves on the board 
        with a move being encoded in long_algebraic form 'e1e4'
        """
        board = self.board
        possible_moves = set()
        
        # Helper: check if position is on board
        def on_board(r, c):
            return 0 <= r < 8 and 0 <= c < 8

        # Helper: check if square is opponent's piece
        def is_opponent(square, my_color):
            if square is None:
                return False
            return square[1] != my_color
        
        # Helper: check if square is friendly piece
        def is_friendly(square, my_color):
            if square is None:
                return False
            return square[1] == my_color
        
        # Helper: add sliding moves (bishop/rook/queen)
        def add_sliding_moves(r, c, directions, my_color):
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                while on_board(nr, nc):
                    target = board[nr][nc]
                    if target is None:
                        possible_moves.add(Move(r, c, nr, nc))
                    else:
                        if is_opponent(target, my_color):
                            possible_moves.add(Move(r, c, nr, nc))
                        break
                    nr += dr
                    nc += dc
        
        # Helper: add single-step moves (knight/king)
        def add_step_moves(r, c, directions, my_color):
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if on_board(nr, nc):
                    target = board[nr][nc]
                    if not is_friendly(target, my_color):
                        possible_moves.add(Move(r, c, nr, nc))
        
        # Direction definitions
        knight_dirs = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1)]
        bishop_dirs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        rook_dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        queen_dirs = bishop_dirs + rook_dirs
        king_dirs = queen_dirs
        
        # Determine which color to move
        my_color = Color.WHITE if self.turn == 'w' else Color.BLACK
        
        # Scan board for pieces
        for r in range(8):
            for c in range(8):
                square = board[r][c]
                if square is None:
                    continue
                
                piece, color = square
                if color != my_color:
                    continue
                
                # Dispatch based on piece type
                if piece == Piece.BISHOP:
                    add_sliding_moves(r, c, bishop_dirs, my_color)
                elif piece == Piece.ROOK:
                    add_sliding_moves(r, c, rook_dirs, my_color)
                elif piece == Piece.QUEEN:
                    add_sliding_moves(r, c, queen_dirs, my_color)
                elif piece == Piece.KNIGHT:
                    add_step_moves(r, c, knight_dirs, my_color)
                elif piece == Piece.KING:
                    add_step_moves(r, c, king_dirs, my_color)
                elif piece == Piece.PAWN:
                    # Pawn direction depends on color
                    if my_color == Color.WHITE:
                        forward = -1  # white moves up the board (row decreases)
                        start_row = 6  # white pawns start at row 6 (rank 2)
                    else:
                        forward = 1   # black moves down the board (row increases)
                        start_row = 1  # black pawns start at row 1 (rank 7)
                    
                    # Pawn captures (diagonal)
                    for dc in [-1, 1]:
                        nr, nc = r + forward, c + dc
                        if on_board(nr, nc):
                            target = board[nr][nc]
                            if is_opponent(target, my_color):
                                possible_moves.add(Move(r, c, nr, nc))
                    
                    # Pawn forward move (one square)
                    nr = r + forward
                    if on_board(nr, c) and board[nr][c] is None:
                        possible_moves.add(Move(r, c, nr, c))
                        
                        # Pawn double move from starting position
                        nr2 = nr + forward
                        if r == start_row and on_board(nr2, c) and board[nr2][c] is None:
                            possible_moves.add(Move(r, c, nr2, c))
        return possible_moves

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