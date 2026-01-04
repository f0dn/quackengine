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
        col = 7
        
        params = []
        params = fen.split()

        for char in reversed(params[0]):
            if col == -1:
                col = 7

            if char == "/":
                row += 1
                col = 7
            elif char.isdigit():
                for _ in range(int(char)):
                    self.board[row][col] = None
                    col -= 1
            else:
                self.board[row][col] = (Piece(char), Color.WHITE) if char.isupper() else (Piece(char.upper()), Color.BLACK)
                col -= 1
        
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
        fen = '/'.join(rows[::-1])

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
                        possible_moves.add(Move(c, r, nc, nr))
                    else:
                        if is_opponent(target, my_color):
                            possible_moves.add(Move(c, r, nc, nr))
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
                        possible_moves.add(Move(c, r, nc, nr))
        
        # Direction definitions
        knight_dirs = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1)]
        bishop_dirs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        rook_dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        queen_dirs = bishop_dirs + rook_dirs
        king_dirs = queen_dirs
        
        # Determine which color to move
        my_color = Color.WHITE if self.turn == Color.WHITE else Color.BLACK
        
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
                        forward = 1  # white moves up the board (row increases)
                        start_row = 1  # white pawns start at row 1 (rank 2)
                    else:
                        forward = -1   # black moves down the board (row decreases)
                        start_row = 6  # black pawns start at row 6 (rank 7)
                    
                    # Pawn captures (diagonal)
                    for dc in [-1, 1]:
                        nr, nc = r + forward, c + dc
                        if on_board(nr, nc):
                            target = board[nr][nc]
                            if is_opponent(target, my_color):
                                possible_moves.add(Move(c, r, nc, nr))
                    
                    # Pawn forward move (one square)
                    nr = r + forward
                    if on_board(nr, c) and board[nr][c] is None:
                        possible_moves.add(Move(c, r, c, nr))
                        
                        # Pawn double move from starting position
                        nr2 = nr + forward
                        if r == start_row and on_board(nr2, c) and board[nr2][c] is None:
                            possible_moves.add(Move(c, r, c, nr2))
        return possible_moves

    def make_moves(self, moves: list[Move]):
        for move in moves:
            from_col, from_row = move.src_coords
            to_col, to_row = move.target_coords

            if move.promoted_to: # promotion move
                color = (self.board[from_row][from_col])[1]

                self.board[from_row][from_col] = None
                self.board[to_col][to_col] = (move.promoted_to, color)
            else:
                moving_piece = self.board[from_row][from_col]

                self.board[from_row][from_col] = None
                self.board[to_row][to_col] = moving_piece

                if moving_piece[0] == Piece.KING and abs(from_col - to_col) == 2: # castling move
                    if (from_col - to_col < 0): # castling short side
                        self.board[from_row][7] = None
                        self.board[to_row][to_col - 1] = (Piece.ROOK, moving_piece[1])
                    else: # castling long side
                        self.board[from_row][0] = None
                        self.board[to_row][to_col + 1] = (Piece.ROOK, moving_piece[1])
    
    def copy_board(self):
        other = Board(self.to_fen())
        return other