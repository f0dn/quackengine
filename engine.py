from piece import Color
class Engine: 
    def __init__(self):
        pass

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
            print("option name Hash type spin default 1 min 1 max 128")
            print("option name NalimovPath type string default <empty>")
            print("option name NalimovCache type spin default 1 min 1 max 32")
            print("option name Nullmove type check default true")
            print("option name Style type combo default Normal var Solid var Normal var Risky")
            print("uciok")
            #engine can send registration checking after the uciok command followed by either registration ok or registration error
            #registration needed for engines that need a username and/or a code to function with all features
        elif(command == "isready"):
            print("readyok")
            #can be sent if engine is calculating, and engine will continue searching after answering
        elif("setoption" in command):
            #should read what GUI set the option to, then engine sets up internal values
            pass
        elif("ucinewgame"):
            #when GUI tells engine that is is searching on a game that it hasn't searched on before
            pass
        elif("debug" in command):
            #engine should send additional infos to the GUI, off by default, can be sent anytime
            pass
        elif("position" in command):
            #needs a new thread
            pass
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

def evaluate_position(self):
    whitepieces = []
    blackpieces = []
    self.board[0][0]
    self.white_moves = []
    self.black_moves = []
    for row in self.board:
        for piece in row: 
            if piece[0] == Color.WHITE: 
                whitepieces.append(piece)
            elif piece[0] == Color.BLACK:
                blackpieces.append(piece)
            else:
                pass
    # The piece should be in the list as [Color][Piece] as [0 or 1]['P' 'N'...]
    total_blackpieces =0
    total_whitepieces = 0
    for piece in blackpieces:
        total_blackpieces += piece.piece_value()
    for piece in whitepieces:
        total_whitepieces +=piece.piece_value()
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
    wfriendly = []
    bfriendly = []
    for row in self.board:
        for piece in row:
            if piece == Piece.KING and piece == Color.WHITE:
                for i in range(9) #or, if i can make a loop that determines how many squares are around the king square
                     for next(piece):
                        wfriendly.append(is_friendly(piece, Color.WHITE))
                        wfriendly_count = wfriendly.count(True)
                        wopponent_count = wfriendly.count(False)
            if piece ==Piece.KING and piece == Color.BLACK:
                for i in range(9): 
                    for next(piece)
                        bfriendly.append(is_friendly(piece, Color.BLACK))
                        bfriendly_count = bfriendly.count(True)
                        bopponent_count = bfriendly.count(False)
    total_whitepieces = total_whitepieces - wvalue_after_threats
    total_blackpieces = total_blackpieces -bvalue_after_threats
    difference = total_whitepieces - total_blackpieces
    return difference 
#i need to find what kind of pieces surround the king 

    