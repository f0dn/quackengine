import chess.pgn
import json

class Move:
    def __init__(self, pgn_file_path):
        self.pgn_file_path = pgn_file_path
        self.lan_moves = []

    def extract_lan(self):
        with open(self.pgn_file_path) as pgn:
            game = chess.pgn.read_game(pgn)
            board = game.board()
            for move in game.mainline_moves():
                self.lan_moves.append(move.uci())
                board.push(move)
        return self.lan_moves

    def save_to_json(self, json_file_path=None):
        if json_file_path is None:
            json_file_path = self.pgn_file_path.replace(".pgn", "_lan.json")
        data = {
            "pgn_file": self.pgn_file_path,
            "lan_moves": self.lan_moves
        }
        with open(json_file_path, "w") as f:
            json.dump(data, f, indent=2)
        return json_file_path
