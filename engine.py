from piece import Color
from board import Board
from uci import parse_command, PositionCommand, GoCommand, UCICommand, IsReadyCommand, QuitCommand, SetOptionCommand, UCINewGameCommand, StopCommand
import threading
import time

class Engine: 
    board: Board
    options_dict: set

    def __init__(self, fen: str = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        openings = set()
        try:
            file = open('openings/2moves_v1.epd.txt')
            for position in file:
                openings.add(position)
        except FileNotFoundError:
            pass

        self.options_dict = {}
        self.board = Board(fen, openings)

        self.default_depth = 3
        self.searching = False
        self.stop_event = threading.Event()
        self.search_thread = None
        self.stop_thread = None
        self.best_move = None
        self.best_pv = []

        self.transposition_table = {}
        
        try:
            file = open('openings/2moves_v1.epd.txt')
            self.openings = set()
            for position in file:
                self.openings.add(position)
        except FileNotFoundError:
            self.openings = set()

    def start(self):
        while True:
            user_input = input()
            if(user_input.lower() == "quit"):
                break
            else:
                self.handle_input(user_input)

    def handle_input(self, command_str: str):
        cmd = parse_command(command_str)

        if isinstance(cmd, UCICommand):
            print("id name quackengine", flush=True)
            print("id author project quack", flush=True)

            self.add_options("Hash", "spin", {"default": 1, "min": 1, "max": 128})
            self.add_options("NalimovPath", "string", {"default": "<empty>"})
            self.add_options("NalimovCache", "spin", {"default": 1, "min": 1, "max": 32})
            self.add_options("Nullmove", "check", {"default": "true"})
            self.add_options("Style", "combo", {"default": "Normal", "var": ["Solid", "Normal", "Risky"]})

            print("uciok", flush=True)

        elif isinstance(cmd, IsReadyCommand):
            print("readyok", flush=True)

        elif isinstance(cmd, UCINewGameCommand):
            self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
            self.transposition_table.clear()

        elif isinstance(cmd, PositionCommand):
            if cmd.startpos:
                self.board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
            elif cmd.fen:
                self.board = Board(cmd.fen)

            if cmd.moves:
                self.board.make_moves(cmd.moves)

        elif isinstance(cmd, GoCommand):
            if self.searching:
                return

            if cmd.infinite:
                depth = None
            else:
                depth = cmd.depth if cmd.depth is not None else None

            self.stop_event.clear()
            self.searching = True
            self.best_move = None
            self.best_pv = []
            
            self.search_thread = threading.Thread(target=self.search, args=(depth,), daemon=True)
            if cmd.wtime is not None and cmd.btime is not None:
                if self.board.turn == Color.WHITE:
                    self.stop_thread = threading.Thread(target=self.stop, args=(cmd.wtime, cmd.winc), daemon=True)
                else:
                    self.stop_thread = threading.Thread(target=self.stop, args=(cmd.btime, cmd.binc), daemon=True)
                self.stop_thread.start()
            self.search_thread.start()

        elif isinstance(cmd, StopCommand):
            if self.searching:
                self.stop_event.set()
                self.search_thread.join()
                self.search_thread = None

                print("bestmove " + self.best_move.to_long_algebraic(), flush=True)

        elif isinstance(cmd, SetOptionCommand):
            self.options_dict[cmd.name] = cmd.value

        elif isinstance(cmd, QuitCommand):
            exit()
       
    def search(self, max_depth=None):
        start_time = time.time()
        depth = 1

        while not self.stop_event.is_set():            
            if max_depth is not None and depth > max_depth:
                break
 
            score, pv = self.minimax(depth)
            if self.board.turn == Color.BLACK:
                score = -1 * score

            if self.stop_event.is_set():
                break
            
            if not pv:
                break
            
            self.best_move = pv[0]
            self.best_pv = pv

            elapsed = int((time.time() - start_time) * 1000)
            pv_str = " ".join(move.to_long_algebraic() for move in pv)

            print(f"info depth {depth} score cp {int(score)} time {elapsed} pv {pv_str}", flush=True)

            depth += 1
        
        if not self.stop_event.is_set() and self.best_move:
            print("bestmove " + self.best_move.to_long_algebraic(), flush=True)

        self.searching = False

    def stop(self, time_rem, time_inc):
        if time_inc is not None:
            wait = time_rem * 0.001 * 0.05 + time_inc * 0.001
        else:
            wait = time_rem * 0.001 * 0.05
        time.sleep(wait)
        self.stop_event.set()
        self.searching = False

        if self.best_move is not None:
            print("bestmove " + self.best_move.to_long_algebraic(), flush=True)
        else:
            score, pv = self.minimax(1)
            self.best_move = pv[0]
            
            print(f"info depth {1} score cp {int(score)} time {wait} pv {self.best_move.to_long_algebraic()}", flush=True)
            print("bestmove " + self.best_move.to_long_algebraic(), flush=True)

    def format_info(self, info: list):
        full_info_str = "info "
        for type, value in info:
            full_info_str += f"{type} {value} "
        print(full_info_str, flush=True)
    
    def add_options(self, option_name: str, type: str, value):
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

    def minimax(self, depth: int, alpha: int = float('-inf'), beta: int = float('inf')):
        if self.stop_event.is_set() and depth > 1:
            return 0, []

        if depth == 0:
            return self.board.evaluate_position(), []
        
        key = self.board.to_fen()

        best_tt_move = None
        if key in self.transposition_table:
            stored_depth, stored_score, stored_pv = self.transposition_table[key]

            if stored_depth >= depth:
                return stored_score, stored_pv[:depth]
            if stored_pv:
                best_tt_move = stored_pv[0]
        
        possible_moves = self.board.get_possible_moves()
        if best_tt_move is not None:
            possible_moves = [best_tt_move] + [move for move in possible_moves if move != best_tt_move]
        if(self.board.turn == Color.WHITE):
            max_eval = float('-inf')
            best_pv = []
            for move in possible_moves:
                old_board = self.board.copy_board()
                self.board.make_moves([move])
                eval, child_pv = self.minimax(depth-1, alpha, beta)
                self.board = old_board
                if eval > max_eval:
                    max_eval = eval
                    best_pv = [move] + child_pv
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            self.transposition_table[key] = (depth, max_eval, best_pv)
            return max_eval, best_pv
        else:
            min_eval = float('inf')
            best_pv = []
            for move in possible_moves:
                old_board = self.board.copy_board()
                self.board.make_moves([move])
                eval, child_pv = self.minimax(depth-1, alpha, beta)
                self.board = old_board
                if eval < min_eval:
                    min_eval = eval
                    best_pv = [move] + child_pv
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            self.transposition_table[key] = (depth, min_eval, best_pv)
            return min_eval, best_pv
