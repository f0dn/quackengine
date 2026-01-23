from piece import Color
from board import Board
from move import Move

class Engine: 
    def __init__(self):
        self.options_dict = {}
        self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        
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
            total_blackpieces += (piece[1].piece_table())[7-blackpositions[index][0], blackpositions[index][1]]
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
                #the king is either in position row1, column 5, or row 8, column5
                for dx1 in range(-1, 1):
                    for dy1 in range(-1, 1):
                        if dx1 == 0 and dy1 == 0:
                            continue
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
                for dx2 in range(-1,1):
                    for dx2 in range(-1,1):
                        if dx2 == 0 and dy2 ==0:
                            continue
                            newx2 = x2+dx2
                            newy2 = x2+dy2
                            wkm = (newx2,newy2)
                            wkmoves.append(wkm)
                            for wkm in wkmoves: 
                                if move in move.src_coords and move in move.target_coords:
                                    threatsow.append(move.src_coords)
                                    bvalue_after_threats -= 1 *piece.piece_value()
        #pawn formation
        #double of a player's own pawn should have a lower value
        #non triangle formation pawns should have a lower value -.2
        #pawns without opposing pawns have higher value
        for column in range(len(self.board)):
        

        total_whitepieces = total_whitepieces - wvalue_after_threats
        total_blackpieces = total_blackpieces -bvalue_after_threats
        difference = total_whitepieces - total_blackpieces
        return difference 
        
        #i need to find what kind of pieces surround the king 

        
        def is_known_opening(self, fen_position):
            if fen_position in self.openings:
                return True
            return False
