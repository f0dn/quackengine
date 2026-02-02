from piece import Color
from board import Board
from move import Move
import random
# import threading
# import time

class Engine: 
    def __init__(self):
        self.options_dict = {}
        self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # self.searching = False
        # self.search_thread = None
        
        # file = open('openings/2moves_v1.epd.txt')
        # self.openings = set()
        # for position in file:
        #     self.openings.add(position)

    def start(self):
        while True:
            user_input = input()
            if(user_input.lower() == "quit"):
                break
            else:
                self.handle_input(user_input)

    def handle_input(self, command: str):
        if(command == "uci"):
            print("id name quackengine", flush=True)
            print("id author project quack", flush=True)
            #find out what options engine should support
            #engine needs to tell the GUI which parameters can be changed in the engine, example below:
            self.add_options("Hash", "spin", {"default": 1, "min": 1, "max": 128})
            self.add_options("NalimovPath", "string", {"default": "<empty>"})
            self.add_options("NalimovCache", "spin", {"default": 1, "min": 1, "max": 32})
            self.add_options("Nullmove", "check", {"default": "true"})
            self.add_options("Style", "combo", {"default": "Normal", "var": ["Solid", "Normal", "Risky"]})
            print("uciok", flush=True)
        elif(command == "isready"):
            print("readyok", flush=True)
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
        elif command.startswith("position"):
            if ("startpos" in command):
                self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                rest = command.split("startpos", 1)[1].strip()
            else:
                fen = command.split("fen", 1)[1].strip()
                
                if "moves" in fen:
                    fen, rest = fen.split("moves", 1)
                    fen = fen.strip()
                    rest = rest.strip()
                else:
                    rest = ""
                
                self.board = Board(fen)
            
            if rest.startswith("moves"):
                rest = rest[5:].strip()
            
            if rest:
                moves = [Move.from_long_algebraic(move) for move in rest.split()]
                self.board.make_moves(moves)
        elif("go" in command):
            #needs a new thread
            #engine needs to send info about the position
            # if ("infinite" in command):
            moves = self.board.get_possible_moves()

            if not moves:
                print("bestmove 0000", flush=True)
                return

            best_move = random.choice(list(moves))

            depth = 1
            nodes = len(moves)
            time_ms = 15
            cp = 13
            pv = best_move.to_long_algebraic()

            print(f"info score cp {cp} depth {depth} nodes {nodes} time {time_ms} pv {pv}", flush=True)

            print("bestmove " + best_move.to_long_algebraic(),  flush=True)

            self.board.make_moves([best_move])

                # if not self.searching:
                #     self.searching = True
                    
                #     def info():
                #         while self.searching:
                #             moves = self.board.get_possible_moves()
                #             print(moves)
                #             time.sleep(0.5)

                #     self.search_thread = threading.Thread(target = info)
                #     self.search_thread.start()
        elif(command == "stop"):
            # self.searching = False
            
            # if self.search_thread:
            #     self.search_thread.join()
            #     self.search_thread = None

            # print(self.calculate_best_move())
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
        print(full_info_str, flush=True)
    
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
        print(f"option name {option_name} type {type} {formatted_value}", flush=True)

    def evaluate_position(self):
        whitepieces = []
        blackpieces = []
        whitepositions = []
        blackpositions = []
        self.board[0][0]
        self.white_moves = []
        self.black_moves = []

        for rowindex, row in enumerate(self.board):
            for columnindex, piece in enumerate(row): 
                if piece[0] == Color.WHITE:
                    whitepieces.append(piece)
                elif piece[1] == Color.BLACK:
                    blackpieces.append(piece)
                    blackpositions.append(tuple[rowindex, columnindex])
                else:
                    pass
        total_blackpieces =0
        total_whitepieces = 0
        for index, piece in enumerate(blackpieces):
            total_blackpieces += piece.piece_value()
            total_blackpieces += (piece[1].piece_table())[blackpositions[index][0], blackpositions[index][1]]
        for piece in whitepieces:
            total_whitepieces +=piece.piece_value()
            total_blackpieces += (piece[1].piece_table())[whitepositions[index][0], whitepositions[index][1]]
        difference = total_whitepieces - total_blackpieces
        #i need to find what kind of pieces surround the king 
#Lines 89-111 Calculate how threats on the pieces affect the position 
        threatsob = []
        threatsow = []
        moves = self.get_possible_moves()
        #move.src_coords and move.target_coords to it's for where it's coming for and wwhere going to. can index into boards
        #if we are black
        self.board[move.src_coords[1]][move.src_coords[0] #in move, (file, rank) is column, row
        # for self.board[move.src_coords[1][move.src_coords[0]]] == Color.White:
        bvalue_after_threats = 0 
        wvalue_after_threats = 0 
        for row in self.board: 
            for piece in row: 
                if piece == Color.WHITE: 
                    for move in moves: 
                        if move in move.src_coords and move in move.target_coords: 
                            threatsow.append(move.src_coords)
                            wvalue_after_threats-= 0.1 * piece.piece_value()     
                elif piece == Color.BLACK: 
                    for move in moves: 
                        if move in move.src_coords and move in move.target_coords:
                            threatsob.append(move.src_coords)
                            bvalue_after_threats -= 0.1 *piece.piece_value()
        #Next section calculates the extent to which the king is under threat
        wkmoves= []
        bkmoves = []
        #for black king
        for y1 in range(len(self.board)):
            for x1 in range(len(self.board[y])):
                bking = self.board[y1][x1]
                if piece[1] == Piece.KING:   
                #the king is either in position row1, column 5, or row 8, column5
                    for dx1 in range(-1, 1):
                        for dy1 in range(-1, 1):
                            if dx1 == 0 and dy1 == 0:
                                continue
                            else:
                                newx1 = x1 + dx1
                                newy1 = y1 + dy1
                                bkm = (newx1, newy1)
                                bkmoves.append(bkm)
                                for bkm in bkmoves: 
                                    if move in move.src_coords and move in move.target_coords:
                                        threatsob.append(move.src_coords)
                                        bvalue_after_threats -= 1 *piece.piece_value()
                                
        #for white king
        for y2 in range(len(self.board)):
            for x2 in range(len(self.board[y])):
                wking = self.board[y2][x2]
                if piece[0] == Piece.KING:
                    for dx2 in range(-1,1):
                        for dx2 in range(-1,1):
                            if dx2 == 0 and dy2 ==0:
                                continue
                            else:
                                newx2 = x2+dx2
                                newy2 = y2+dy2
                                wkm = tuple[(newx2,newy2)]
                                wkmoves.append(wkm)
                                for wkm in wkmoves: 
                                    if move in move.src_coords and move in move.target_coords:
                                        threatsow.append(move.src_coords)
                                        bvalue_after_threats -= 1 *piece.piece_value()
        #pawn formation
        #double of a player's own pawn should have a lower value
        #non triangle formation pawns should have a lower value -.2
        #pawns without opposing pawns have higher value
    
        pawn_value = .1*piece.piece_value()
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if piece[0] == Piece.PAWN:  
                friendlypawn = self.board[y][x]
                    if y = 1:
                        pawn_value = .1*piece.piece_value()
                    if y = 2:
                        pawn_value = .2*piece.piece_value()
                    if y = 3:
                        pawn_value = .3*piece.piece_value()
                    if y = 4:
                        pawn_value = .4*piece.piece_value()
                    if y = 5:
                        pawn_value = .5*piece.piece_value()
                    if y = 6:
                        pawn_value = .6*piece.piece_value()
                    if y = 7:
                        pawn_value = .7*piece.piece_value()
                    if y = 8:
                        pawn_value = .8*piece.piece_value()
                        for dy1 in range(1,7): #pass pawn
                            if not move in move.src_coords:
                                pawn_value = 2*piece.piece_value()

                        for dy1 in range(-1,-7): #second pawn behind first
                            if move in move.src_coords:
                                pawn_value = .7*piece.piece_value()
        # wbishop_formation #double bishop 
        wbishop_value = 0
        for wbx in range(len(self.board)):
            for wby in range(len(self.board[y])):
                if piece[0] == Piece.BISHOP:
                    for wbdx in range(-1,1):
                        for wbdy in range(-1,1):
                            if wbdx ==0 and wbdy ==0:
                                continue
                            else:
                                if piece[0] == Piece.BISHOP:
                                    wbishop_value = 45
        # bbishop_formawtion - double bishop
            bbishop_value = 0
            for bbx in range(len(self.board)):
                for bby in range(len(self.board[y])):
                    if piece[1] == Piece.BISHOP:
                        for bbdx in range(-1,1):
                            for bbdy in range(-1,1):
                                if bbdx ==0 and bbdy ==0:
                                    continue
                                else:
                                    if piece[1] == Piece.BISHOP:
                                        bbishop_value = 45
                        
        total_whitepieces = total_whitepieces + wbishop_value
        total_blackpieces = total_blackpieces + bbishop_value
        total_whitepieces = total_whitepieces - wvalue_after_threats
        total_blackpieces = total_blackpieces -bvalue_after_threats
        difference = total_whitepieces - total_blackpieces
        return difference
        
        #i need to find what kind of pieces surround the king 

    def minimax(self, board, depth, alpha, beta):
        if depth == 0:
            return self.evaluate_position(), None
        possible_moves = board.get_possible_moves()
        if(board.turn == Color.WHITE):
            max_eval = float('-inf')
            best_move = None
            for move in possible_moves:
                minimax_board = board.copy_board()
                minimax_board.make_moves([move])
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
                minimax_board.make_moves([move])
                eval, _ = self.minimax(minimax_board, depth - 1, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
