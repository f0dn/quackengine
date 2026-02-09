from piece import Color
from piece import Piece
from board import Board
from move import Move

class Engine: 
    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.options_dict = {}
        self.board = Board(fen)
        
        file = open('openings/2moves_v1.epd.txt')
        self.openings = set()
        for position in file:
            self.openings.add(position)

    def start(self):
        while True:
            user_input = input()
            if(user_input.lower() == "quit"):
                break
            else:
                self.handle_input(user_input)

    def handle_input(self, command: str):
        if(command == "uci"):
            print("id name quackengine")
            print("id author project quack")
            #find out what options engine should support
            #engine needs to tell the GUI which parameters can be changed in the engine, example below:
            self.add_options("Hash", "spin", {"default": 1, "min": 1, "max": 128})
            self.add_options("NalimovPath", "string", {"default": "<empty>"})
            self.add_options("NalimovCache", "spin", {"default": 1, "min": 1, "max": 32})
            self.add_options("Nullmove", "check", {"default": "true"})
            self.add_options("Style", "combo", {"default": "Normal", "var": ["Solid", "Normal", "Risky"]})
            print("uciok")
        elif(command == "isready"):
            print("readyok")
            #can be sent if engine is calculating, and engine will continue searching after answering
        elif("setoption" in command):
            #should read what GUI set the option to, then engine sets up internal values
            pass
        elif(command == "ucinewgame"):
            #when GUI tells engine that is is searching on a game that it hasn't searched on before
            pass
        elif("debug" in command):
            #engine should send additional infos to the GUI, off by default, can be sent anytime
            pass
        elif("position" in command):
            if ("startpos" in command):
                self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
            else:
                start_index = command.find("fen") + 4
                end_index = command.find("moves") - 1
                self.board = Board(command[start_index:end_index])
            
            moves = [Move.from_long_algebraic(move) for move in command[(command.find("moves") + 6):].split(' ')]
            self.board.make_moves(moves)
        elif("go" in command):
            self.calculate_best_move()
            #needs a new thread
            #engine needs to send info about the position
            pass
        elif(command == "stop"):
            self.calculate_best_move()
            #possibly ponder as well
            pass
        elif(command == "ponderhit"):
            #ponder is when engine calculates opponent's next move during opponent's turn
            #normal search is when engine calculates its own move during its own turn
            #when user plays expected move, then engine should continue searching but switch from pondering to normal search
            pass

    def calculate_best_move(self):
        #just best move or also info?
        pass

    def format_info(self, list_of_tuples):
        full_info_str = "info "
        for type, value in list_of_tuples:
            full_info_str += f"{type} {value} "
        print(full_info_str)
    
    def add_options(self, option_name, type, value):
        self.options_dict[option_name] = {"type": type, "value": value} #value would be a dict of default, min, max etc
        parts = []
        for k, v in value.items():
            if isinstance(v, list):
                for item in v:
                    parts.append(f"{k} {item}")
            else:
                parts.append(f"{k} {v}")
        formatted_value = " ".join(parts)
        print(f"option name {option_name} type {type} {formatted_value}")

    def evaluate_position(self):
        if self.is_known_opening(self.board.to_fen()) and self.board.turn == Color.WHITE:
            return float('inf')
        elif self.is_known_opening(self.board.to_fen()) and self.board.turn == Color.BLACK:
            return float('-inf')
        whitepieces = []
        blackpieces = []
        whitepositions = []
        blackpositions = []
        self.white_moves = []
        self.black_moves = []

        for rowindex, row in enumerate(self.board.board):
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
        pawn_formation = self.evaluate_pawn_formation()
        bishops = self.evaluate_bishops()
        
        king_safety = self.evaluate_king_safety()
        total_whitepieces = total_whitepieces + king_safety[0]
        total_blackpieces = total_blackpieces + king_safety[1]

        capture_threats = self.evaluate_capture_threats()
        total_whitepieces = total_whitepieces + capture_threats[0]
        total_blackpieces = total_blackpieces + capture_threats[1]

        difference = total_whitepieces - total_blackpieces +bishops + pawn_formation
        return difference
    def evaluate_pawn_formation(self):  
        wtotal_pawn_value = 0 
        btotal_pawn_value = 0 
        wpass_pawn_value = 0 
        bpass_pawn_value=0
        for y in range(len(self.board.board)):
            for x in range(len(self.board.board[y])):
                piece = self.board.board[y][x]
                if piece is None: 
                    continue
                if piece[0] == Piece.PAWN and piece[1] == Color.WHITE:  
                    wpass_pawn = True
                    wpass_pawn_value = 0 
                    if (y==0) or (y==1) or (y==2) or (y==3) or (y==4) or (y==5) or (y ==6) or (y==7) or (y==8):
                        wpawn_value = (y/10)*piece[0].piece_value()
                        wtotal_pawn_value +=wpawn_value 
                        for dy in (1, (7-y)):
                            wother_pawn = self.board.board[y][x]
                            if piece is None: 
                                continue
                            if wother_pawn[0] == Piece.PAWN and wother_pawn[1] == Color.WHITE: 
                                wpass_pawn = False
                                wpass_pawn_value -=30
                                wtotal_pawn_value += wpass_pawn_value
                                break
                            else: 
                                wpass_pawn_value +=100
                                wtotal_pawn_value +=wpass_pawn_value
                                break
                if piece[0] == Piece.PAWN and piece[1] == Color.BLACK:  
                    bpass_pawn = True
                    bpass_pawn_value = 0 
                    if (y==0) or (y==1) or (y==2) or (y==3) or (y==4) or (y==5) or (y ==6) or (y==7) or (y==8):
                        bpawn_value = (y/10)*piece[0].piece_value()
                        btotal_pawn_value +=bpawn_value 
                        for dy in (1, (7-y)):
                            bother_pawn = self.board.board[y][x]
                            if piece is None: 
                                continue
                            if bother_pawn[0] == Piece.PAWN and bother_pawn[1] == Color.BLACK: 
                                bpass_pawn = False
                                bpass_pawn_value -=30
                                btotal_pawn_value += bpass_pawn_value
                                break
                            else: 
                                bpass_pawn_value +=100
                                btotal_pawn_value +=bpass_pawn_value
                                break
        difference = wtotal_pawn_value - btotal_pawn_value 
        return difference                 
                            
    def evaluate_bishops(self):            
        # wbishop_formation #double bishop 
        wbishop_value = 0
        for wbx in range(len(self.board.board)):
            for wby in range(len(self.board.board[y])):
                wpiece = self.board.board[y][x]
                if wpiece is None: 
                    continue
                if wpiece[0] == Piece.BISHOP:
                    for wbdx in range(-1,1):
                        for wbdy in range(-1,1):
                            wnew_pawn = self.board.board[y][x]
                            if wbdx ==0 and wbdy ==0:
                                continue
                            if wnew_pawn[0] == Piece.BISHOP and wnew_pawn[1] == Color.WHITE:
                                    wbishop_value += 45
        # bbishop_formawtion - double bishop
            bbishop_value = 0
            for bbx in range(len(self.board.board)):
                bpiece = self.board.board.board[y][x]
                for bby in range(len(self.board[y])):
                    if bpiece is None: 
                        continue
                    if bpiece[0] == Piece.BISHOP:
                        for bbdx in range(-1,1):
                            for bbdy in range(-1,1):
                                bnew_pawn = self.board.board[y][x]
                                if bbdx ==0 and bbdy ==0:
                                    continue
                                if bnew_pawn[0] == Piece.BISHOP and bnew_pawn[1] == Color.BLACK:
                                    bbishop_value += 45
        difference = wbishop_value - bbishop_value 
        return difference 
    
        

    def evaluate_capture_threats(self):
        #Calculate how threats on the pieces affect the position
        #threatsow and threatsob contain all captures (for future implementation and testing)
        threatsob = []
        threatsow = []
        moves = self.board.get_possible_moves()
        #move.src_coords and move.target_coords to it's for where it's coming for and wwhere going to. can index into boards
        # for self.board[move.src_coords[1][move.src_coords[0]]] == Color.White:
        bvalue_after_threats = 0 
        wvalue_after_threats = 0 
        for columnindex, row in enumerate(self.board.board): 
            for rowindex, piece in enumerate(row): 
                if piece is None:
                    continue
                elif (self.board.turn == Color.BLACK) and (piece[1] == Color.WHITE):
                    for move in moves: 
                        if move.target_coords == (rowindex, columnindex): 
                            threatsow.append(move)
                            wvalue_after_threats -= 0.1 * piece[0].piece_value()     
                elif (self.board.turn == Color.WHITE) and (piece[1] == Color.BLACK):
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
        moves = self.board.get_possible_moves()

        #Next section calculates the extent to which the king is under threat
        threat_king_color = Color.WHITE
        if self.board.turn == Color.WHITE:
            threat_king_color = Color.BLACK
        else:
            threat_king_color = Color.WHITE
        kmoves = []
        xposking = 0
        yposking = 0
        for y1 in range(len(self.board.board)):
            for x1 in range(len(self.board.board[y1])):
                if self.board.board[y1][x1] is None:
                    continue
                elif (self.board.board[y1][x1][1] == threat_king_color) and (self.board.board[y1][x1][0] == Piece.KING):
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
                        bvalue_king_safety -= 0.1 * (self.board.board[move.src_coords[1]][move.src_coords[0]])[0].piece_value()
                    else:
                        threatsowk.append(move)
                        wvalue_king_safety -= 0.1 * (self.board.board[move.src_coords[1]][move.src_coords[0]])[0].piece_value()

        return (wvalue_king_safety, bvalue_king_safety)

    def is_known_opening(self, fen_position):
        if fen_position in self.openings:
            return True
        return False

    def minimax(self, board, depth, alpha, beta):
        if depth == 0:
            return self.evaluate_position(), None
        possible_moves = board.get_possible_moves()
        if(board.turn == Color.WHITE):
            max_eval = float('-inf')
            best_move = None
            for move in possible_moves:
                minimax_board = board.copy_board()
                minimax_board.make_moves(move)
                eval, _ = self.minimax(minimax_board, depth - 1, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in possible_moves:
                minimax_board = board.copy_board()
                minimax_board.make_moves(move)
                eval, _ = self.minimax(minimax_board, depth - 1, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
