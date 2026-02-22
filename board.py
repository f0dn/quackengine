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
            self.recent_en_passant_target = (ord(params[3][0]) - ord('a'), int(params[3][1])-1)
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
            fen += " " + chr(self.recent_en_passant_target[0] + ord('a')) + str(self.recent_en_passant_target[1]+1)

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
        possible_moves = list()
        
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
                        possible_moves.append(Move(c, r, nc, nr))
                    else:
                        if is_opponent(target, my_color):
                            possible_moves.append(Move(c, r, nc, nr))
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
                        possible_moves.append(Move(c, r, nc, nr))
        
        # Direction definitions
        knight_dirs = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, 2), (1, -2), (2, -1), (2, 1)]
        bishop_dirs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
        rook_dirs = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        queen_dirs = bishop_dirs + rook_dirs
        king_dirs = queen_dirs
        
        # Scan board for pieces
        for r in range(8):
            for c in range(8):
                square = board[r][c]
                if square is None:
                    continue
                
                piece, color = square
                if color != self.turn:
                    continue
                
                # Dispatch based on piece type
                if piece == Piece.BISHOP:
                    add_sliding_moves(r, c, bishop_dirs, self.turn)
                elif piece == Piece.ROOK:
                    add_sliding_moves(r, c, rook_dirs, self.turn)
                elif piece == Piece.QUEEN:
                    add_sliding_moves(r, c, queen_dirs, self.turn)
                elif piece == Piece.KNIGHT:
                    add_step_moves(r, c, knight_dirs, self.turn)
                elif piece == Piece.KING:
                    add_step_moves(r, c, king_dirs, self.turn)
                elif piece == Piece.PAWN:
                    # Pawn direction depends on color
                    if self.turn == Color.WHITE:
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
                            if is_opponent(target, self.turn):
                                possible_moves.append(Move(c, r, nc, nr))
                    
                    # Pawn forward move (one square)
                    nr = r + forward
                    if on_board(nr, c) and board[nr][c] is None:
                        possible_moves.append(Move(c, r, c, nr))
                        
                        # Pawn double move from starting position
                        nr2 = nr + forward
                        if r == start_row and on_board(nr2, c) and board[nr2][c] is None:
                            possible_moves.append(Move(c, r, c, nr2))
        legal_moves = list()

        for move in possible_moves:
            test_board = self.copy_board()
            test_board.make_moves([move])

            if not test_board.is_king_in_check(test_board.board, self.turn):
                legal_moves.append(move)

        return legal_moves

    def make_moves(self, moves: list[Move]):
        for move in moves:
            from_col, from_row = move.src_coords
            to_col, to_row = move.target_coords

            # obtaining object at the coordinates
            moving_piece = self.board[from_row][from_col]
            target = self.board[to_row][to_col]

            # checking if en_passant
            is_en_passant = moving_piece[0] == Piece.PAWN and target is None and from_col != to_col and self.recent_en_passant_target == (to_col, to_row)

            # clear target
            self.recent_en_passant_target = None

            # updating halfmove clock
            if moving_piece[0] == Piece.PAWN or target is not None:
                self.halfmove_clock = 0
            else:
                self.halfmove_clock += 1

            # updating castling rights
            if moving_piece[0] == Piece.KING: # if king moved
                self.castling_avail[moving_piece[1]].clear()
            if moving_piece[0] == Piece.ROOK: # if rook moved
                if from_col == 0:
                    self.castling_avail[moving_piece[1]].discard(Piece.QUEEN)
                elif from_col == 7:
                    self.castling_avail[moving_piece[1]].discard(Piece.KING)
            if target and target[0] == Piece.ROOK: # if rook captured
                opp = Color.BLACK if moving_piece[1] == Color.WHITE else Color.WHITE
                if to_col == 0:
                    self.castling_avail[opp].discard(Piece.QUEEN)
                elif to_col == 7:
                    self.castling_avail[opp].discard(Piece.KING)

            # actual movement
            if move.promoted_to: # promotion move
                color = (self.board[from_row][from_col])[1]

                self.board[from_row][from_col] = None
                self.board[to_row][to_col] = (move.promoted_to, color)
            else:
                if is_en_passant: # en_passant
                    self.board[from_row][to_col] = None
                
                self.board[from_row][from_col] = None
                self.board[to_row][to_col] = moving_piece

                if moving_piece[0] == Piece.PAWN and abs(from_row - to_row) == 2: # en passant target update
                    self.recent_en_passant_target = (from_col, (from_row + to_row) // 2)
                elif moving_piece[0] == Piece.KING and abs(from_col - to_col) == 2: # castling move
                    if (from_col - to_col < 0): # castling short side
                        self.board[from_row][7] = None
                        self.board[to_row][to_col - 1] = (Piece.ROOK, moving_piece[1])
                    else: # castling long side
                        self.board[from_row][0] = None
                        self.board[to_row][to_col + 1] = (Piece.ROOK, moving_piece[1])
            
            if self.turn == Color.BLACK: # updating the fullmove clock
                    self.fullmoves += 1
            # switch turns
            self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE

    def is_king_in_check(self, board, color):
        # find king
        king_r = king_c = None
        for r in range(8):
            for c in range(8):
                sq = board[r][c]
                if sq and sq[0] == Piece.KING and sq[1] == color:
                    king_r, king_c = r, c
                    break
            if king_r is not None:
                break

        enemy = Color.BLACK if color == Color.WHITE else Color.WHITE

        def on_board(r, c):
            return 0 <= r < 8 and 0 <= c < 8

        # check all enemy attacks
        pawn_dir = 1 if enemy == Color.WHITE else -1
        for dc in (-1, 1):
            r, c = king_r + pawn_dir, king_c + dc
            if on_board(r, c):
                sq = board[r][c]
                if sq and sq == (Piece.PAWN, enemy):
                    return True

        knight_dirs = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,2),(1,-2),(2,-1),(2,1)]
        for dr, dc in knight_dirs:
            r, c = king_r + dr, king_c + dc
            if on_board(r, c):
                if board[r][c] == (Piece.KNIGHT, enemy):
                    return True

        directions = [
            (-1,0),(1,0),(0,-1),(0,1),
            (-1,-1),(-1,1),(1,-1),(1,1)
        ]

        for dr, dc in directions:
            r, c = king_r + dr, king_c + dc
            while on_board(r, c):
                sq = board[r][c]
                if sq:
                    p, color = sq
                    if color == enemy:
                        if (
                            (dr == 0 or dc == 0) and p in (Piece.ROOK, Piece.QUEEN) or
                            (dr != 0 and dc != 0) and p in (Piece.BISHOP, Piece.QUEEN)
                        ):
                            return True
                    break
                r += dr
                c += dc

        # king adjacency
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == dc == 0:
                    continue
                r, c = king_r + dr, king_c + dc
                if on_board(r, c):
                    if board[r][c] == (Piece.KING, enemy):
                        return True
        return False
        
    def copy_board(self):
        other = Board(self.to_fen())
        return other
    
    def evaluate_position(self):
        # if self.is_known_opening(self.to_fen()) and self.turn == Color.WHITE:
        #     return float('inf')
        # elif self.is_known_opening(self.to_fen()) and self.turn == Color.BLACK:
        #     return float('-inf')
        whitepieces = []
        blackpieces = []
        whitepositions = []
        blackpositions = []
        self.white_moves = []
        self.black_moves = []

        for rowindex, row in enumerate(self.board):
            for columnindex, piece in enumerate(row): 
                if piece is None:
                    continue
                elif piece[1] == Color.WHITE:
                    whitepieces.append(piece)
                    whitepositions.append((rowindex, columnindex))
                elif piece[1] == Color.BLACK:
                    blackpieces.append(piece)
                    blackpositions.append((rowindex, columnindex))
                else:
                    pass
        total_blackpieces = 0
        total_whitepieces = 0
        for index, piece in enumerate(blackpieces):
            total_blackpieces += piece[0].piece_value()
            total_blackpieces += (piece[0].piece_table())[blackpositions[index][0]][blackpositions[index][1]]
        for index, piece in enumerate(whitepieces):
            total_whitepieces += piece[0].piece_value()
            total_whitepieces += (piece[0].piece_table())[7-whitepositions[index][0]][whitepositions[index][1]]
        
        king_safety = self.evaluate_king_safety()
        total_whitepieces = total_whitepieces + king_safety[0]
        total_blackpieces = total_blackpieces + king_safety[1]

        capture_threats = self.evaluate_capture_threats()
        total_whitepieces = total_whitepieces + capture_threats[0]
        total_blackpieces = total_blackpieces + capture_threats[1]

        difference = total_whitepieces - total_blackpieces
        return difference

    def evaluate_capture_threats(self):
        #Calculate how threats on the pieces affect the position
        #threatsow and threatsob contain all captures (for future implementation and testing)
        threatsob = []
        threatsow = []
        moves = self.get_possible_moves()
        #move.src_coords and move.target_coords to it's for where it's coming for and wwhere going to. can index into boards
        # for self.board[move.src_coords[1][move.src_coords[0]]] == Color.White:
        bvalue_after_threats = 0 
        wvalue_after_threats = 0 
        for columnindex, row in enumerate(self.board): 
            for rowindex, piece in enumerate(row): 
                if piece is None:
                    continue
                elif (self.turn == Color.BLACK) and (piece[1] == Color.WHITE):
                    for move in moves: 
                        if move.target_coords == (rowindex, columnindex): 
                            threatsow.append(move)
                            wvalue_after_threats -= 0.1 * piece[0].piece_value()     
                elif (self.turn == Color.WHITE) and (piece[1] == Color.BLACK):
                    for move in moves: 
                        if move.target_coords == (rowindex, columnindex): 
                            threatsob.append(move)
                            bvalue_after_threats -= 0.1 * piece[0].piece_value()
        return (wvalue_after_threats, bvalue_after_threats)
    
    def evaluate_king_safety(self):
        #i need to find what kind of pieces surround the king
        #threatsowk and threatsobk contain all moves restricting king movement (for testing and future implementation)
        threatsobk = []
        threatsowk = []
        bvalue_king_safety = 0 
        wvalue_king_safety = 0 
        moves = self.get_possible_moves()

        #Next section calculates the extent to which the king is under threat
        threat_king_color = Color.WHITE
        if self.turn == Color.WHITE:
            threat_king_color = Color.BLACK
        else:
            threat_king_color = Color.WHITE
        kmoves = []
        xposking = 0
        yposking = 0
        for y1 in range(len(self.board)):
            for x1 in range(len(self.board[y1])):
                if self.board[y1][x1] is None:
                    continue
                elif (self.board[y1][x1][1] == threat_king_color) and (self.board[y1][x1][0] == Piece.KING):
                    xposking = x1
                    yposking = y1
        for dx1 in (-1, 0, 1):
            for dy1 in (-1, 0, 1):
                if dx1 == 0 and dy1 == 0:
                    continue
                else:
                    newx1 = xposking + dx1
                    newy1 = yposking + dy1
                    if (0 <= newx1 < 8) and (0 <= newy1 < 8):
                        km = (newx1, newy1)
                        kmoves.append(km)
        for move in moves: 
            for km in kmoves:
                if move.target_coords == km:
                    if threat_king_color == Color.BLACK:
                        threatsobk.append(move)
                        bvalue_king_safety -= 0.1 * (self.board[move.src_coords[1]][move.src_coords[0]])[0].piece_value()
                    else:
                        threatsowk.append(move)
                        wvalue_king_safety -= 0.1 * (self.board[move.src_coords[1]][move.src_coords[0]])[0].piece_value()

        return (wvalue_king_safety, bvalue_king_safety)
    