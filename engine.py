from piece import Color
from piece import Piece

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
        return difference 
    #i need to find what kind of pieces surround the king 

    