from piece import Color
from piece import Piece
PawnTable = [
     0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
     5,  5, 10, 27, 27, 10,  5,  5,
     0,  0,  0, 25, 25,  0,  0,  0,
     5, -5,-10,  0,  0,-10, -5,  5,
     5, 10, 10,-25,-25, 10, 10,  5,
     0,  0,  0,  0,  0,  0,  0,  0
]
KnightTable = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-20,-30,-30,-20,-40,-50,
]
BishopTable = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-40,-10,-10,-40,-10,-20,
]
KingTable = [
  -30, -40, -40, -50, -50, -40, -40, -30,
  -30, -40, -40, -50, -50, -40, -40, -30,
  -30, -40, -40, -50, -50, -40, -40, -30,
  -30, -40, -40, -50, -50, -40, -40, -30,
  -20, -30, -30, -40, -40, -30, -30, -20,
  -10, -20, -20, -20, -20, -20, -20, -10, 
   20,  20,   0,   0,   0,   0,  20,  20,
   20,  30,  10,   0,   0,  10,  30,  20
]
KingTableEndGame = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]

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
                whitepositions.append(tuple[rowindex, columnindex])
            elif piece[1] == Color.BLACK:
                blackpieces.append(piece)
                blackpositions.append(tuple[rowindex, columnindex])
            else:
                pass
    total_blackpieces = 0
    total_whitepieces = 0
    for index, piece in enumerate(blackpieces):
        total_blackpieces += piece.piece_value()
        if piece[1] == Piece.PAWN:
            total_blackpieces += PawnTable[7-blackpositions[index][0], blackpositions[index][1]]
        elif piece[1] == Piece.KNIGHT:
            total_blackpieces += KnightTable[7-blackpositions[index][0], blackpositions[index][1]]
        elif piece[1] == Piece.BISHOP:
            total_blackpieces += BishopTable[7-blackpositions[index][0], blackpositions[index][1]]
        elif piece[1] == Piece.KING:
            total_blackpieces += KingTable[7-blackpositions[index][0], blackpositions[index][1]]
    for piece in whitepieces:
        total_whitepieces +=piece.piece_value()
        if piece[1] == Piece.PAWN:
            total_whitepieces += PawnTable[whitepositions[index][0], whitepositions[index][1]]
        elif piece[1] == Piece.KNIGHT:
            total_whitepieces += KnightTable[whitepositions[index][0], whitepositions[index][1]]
        elif piece[1] == Piece.BISHOP:
            total_whitepieces += BishopTable[whitepositions[index][0], whitepositions[index][1]]
        elif piece[1] == Piece.KING:
            total_whitepieces += KingTable[whitepositions[index][0], whitepositions[index][1]]
    difference = total_whitepieces - total_blackpieces
    return difference
   # threatsob = []
    # threatsow = []
    # if element in self.blackpieces == element in self.white_moves:
    #     threatsob.append(element)
    # if element in self.whitepieces == element in self.black_moves:
    #     threatsow.append(element)
    # if threatsob == 'P':
    #     self.black_material_value -=1
    # if threatsob == 'B':
    #     self.black_material_value -=3
    # if threatsob == 'N':
    #     self.black_material_value -=3
    # if threatsob == 'R':
    #     self.black_material_value -=5
    # if threatsob == 'Q':
    #     self.black_material_value -=9
    # if threatsow == 'P':
    #     self.white_material_value -=1
    # if threatsow == 'B':
    #     self.white_material_value -=3
    # if threatsow == 'N':
    #     self.white_material_value -=3
    # if threatsow == 'R':
    #     self.white_material_value -=5
    # if threatsow == 'Q':
    #     self.white_matieral_value -=9
