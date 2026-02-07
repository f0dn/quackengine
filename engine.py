from piece import Color
from piece import Piece
from board import Board
from move import Move
import random
# import threading
# import time

class Engine: 
    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.options_dict = {}
        self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        # self.searching = False
        # self.search_thread = None
        
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

            depth = 1
            nodes = len(moves)
            time_ms = 15
            cp, pv = self.minimax(self.board, depth, float('-inf'), float('inf'))
            pv_str = " ".join(move.to_long_algebraic() for move in pv)

            print(f"info score cp {int(cp)} depth {depth} nodes {nodes} time {time_ms} pv {pv_str}", flush=True)

            best_move = pv[0]
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
            return self.evaluate_position(), []
        possible_moves = board.get_possible_moves()
        if(board.turn == Color.WHITE):
            max_eval = float('-inf')
            best_pv = []
            for move in possible_moves:
                minimax_board = board.copy_board()
                minimax_board.make_moves([move])
                eval, child_pv = self.minimax(minimax_board, depth - 1, alpha, beta)
                if eval > max_eval:
                    max_eval = eval
                    best_pv = [move] + child_pv
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_pv
        else:
            min_eval = float('inf')
            best_pv = []
            for move in possible_moves:
                minimax_board = board.copy_board()
                minimax_board.make_moves([move])
                eval, child_pv = self.minimax(minimax_board, depth - 1, alpha, beta)
                if eval < min_eval:
                    min_eval = eval
                    best_pv = [move] + child_pv
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_pv
