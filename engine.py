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

    def is_known_opening(self, fen_position):
        if fen_position in self.openings:
            return True
        return False