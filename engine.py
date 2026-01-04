from piece import Color
from piece import Piece
from board import Board
from move import Move

class Engine: 
    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.options_dict = {}
        self.board = Board(fen)
        
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

        difference = total_whitepieces - total_blackpieces
        return difference/100
        
        #i need to find what kind of pieces surround the king 

    def evaluate_king_safety(self):
        #i need to find what kind of pieces surround the king 
        #Lines 89-111 Calculate how threats on the pieces affect the position 
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
                elif (self.board.turn == Color.BLACK) & (piece[1] == Color.WHITE):
                    for move in moves: 
                        if move.target_coords == (rowindex, columnindex): 
                            threatsow.append(move)
                            wvalue_after_threats -= 0.1 * piece[0].piece_value()     
                elif (self.board.turn == Color.WHITE) & (piece[1] == Color.BLACK):
                    for move in moves: 
                        if move.target_coords == (rowindex, columnindex): 
                            threatsob.append(move)
                            bvalue_after_threats -= 0.1 * piece[0].piece_value()

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
                elif (self.board.board[y1][x1][1] == threat_king_color) & (self.board.board[y1][x1][0] == Piece.KING):
                    xposking = x1
                    yposking = y1
        for dx1 in range(-1, 1):
            for dy1 in range(-1, 1):
                if dx1 == 0 and dy1 == 0:
                    continue
                else:
                    newx1 = xposking + dx1
                    newy1 = yposking + dy1
                    if (0 <= newx1 < 8) & (0 <= newy1 < 8):
                        km = (newx1, newy1)
                        kmoves.append(km)
        for move in moves: 
            for km in kmoves:
                if move.target_coords == km:
                    if threat_king_color == Color.BLACK:
                        threatsob.append(move)
                        bvalue_after_threats -= 0.1 * (self.board.board[move.src_coords[1]][move.src_coords[0]])[0].piece_value()
                    else:
                        threatsow.append(move)
                        wvalue_after_threats -= 0.1 * (self.board.board[move.src_coords[1]][move.src_coords[0]])[0].piece_value()

        # wkmoves= []
        # bkmoves = []
        # #for black king
        # xposking = 0
        # yposking = 0
        # for y1 in range(len(self.board.board)):
        #     for x1 in range(len(self.board.board[y1])):
        #         if self.board.board[y1][x1] is None:
        #             continue
        #         elif (self.board.board[y1][x1][1] == Color.BLACK) & (self.board.board[y1][x1][0] == Piece.KING):
        #             xposking = x1
        #             yposking = y1
        # #the king is either in position row1, column 5, or row 8, column5
        # for dx1 in range(-1, 1):
        #     for dy1 in range(-1, 1):
        #         if dx1 == 0 and dy1 == 0:
        #             continue
        #         else:
        #             newx1 = xposking + dx1
        #             newy1 = yposking + dy1
        #             bkm = (newx1, newy1)
        #             bkmoves.append(bkm)
        # for move in moves: 
        #     for bkm in bkmoves:
        #         if move.target_coords == bkm:
        #             threatsob.append(move)
        #             bvalue_after_threats -= 0.1 * (self.board.board[move.src_coords[1]][move.src_coords[0]])[0].piece_value()
                                
        # #for white king
        # xposking = 0
        # yposking = 0
        # for y2 in range(len(self.board.board)):
        #     for x2 in range(len(self.board.board[y2])):
        #         if self.board.board[y2][x2] is None:
        #             continue
        #         elif (self.board.board[y2][x2][1] == Color.WHITE) & (self.board.board[y2][x2][0] == Piece.KING):
        #             xposking = x2
        #             yposking = y2
        # for dx2 in range(-1,1):
        #     for dy2 in range(-1,1):
        #         if dx2 == 0 and dy2 == 0:
        #             continue
        #         else:
        #             newx2 = xposking + dx2
        #             newy2 = yposking + dy2
        #             wkm = (newx2, newy2)
        #             wkmoves.append(wkm)        
        # for move in moves:
        #     for wkm in wkmoves:
        #         if move.target_coords == wkm:
        #             threatsow.append(move)
        #             wvalue_after_threats -= 0.1 * (self.board.board[move.src_coords[1]][move.src_coords[0]])[0].piece_value()

        return (wvalue_after_threats, bvalue_after_threats)

        
def is_known_opening(self, fen_position):
    if fen_position in self.openings:
        return True
    return False
