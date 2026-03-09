from abc import abstractmethod
from typing import List, Optional

class Command:
     @staticmethod
     @abstractmethod
     def parse(command_str: str) -> "Command":
        pass
     
class PositionCommand(Command):
    def __init__(self, startpos: bool, fen: Optional[str], moves: List[str]):
        self.startpos = startpos
        self.fen = fen
        self.moves = moves

    @staticmethod
    def parse(command_str: str) -> "PositionCommand":
        tokens = command_str.strip().split()
        tokens.pop(0)
        startpos = False
        fen = None
        moves = []

        if tokens[0] == "startpos":
            startpos = True
            tokens.pop(0)
        elif tokens[0] == "fen":
            tokens.pop(0)
            fen = " ".join(tokens[:6])
            tokens = tokens[6:]

        if tokens and tokens[0] == "moves":
            tokens.pop(0)
            moves = tokens

        return PositionCommand(startpos, fen, moves)
        
class GoCommand(Command):
    def __init__(self, depth: Optional[int] = None, movetime: Optional[int] = None, wtime: Optional[int] = None, btime: Optional[int] = None, 
                 winc: Optional[int] = None, binc: Optional[int] = None, infinite: bool = False, searchmoves: Optional[List[str]] = None, 
                 ponder: bool = False, movestogo: Optional[int] = None, nodes: Optional[int] = None, mate: Optional[int] = None):
        self.depth = depth
        self.movetime = movetime
        self.wtime = wtime
        self.btime = btime
        self.winc = winc
        self.binc = binc
        self.infinite = infinite
        self.searchmoves = searchmoves
        self.ponder = ponder
        self.movestogo = movestogo
        self.nodes = nodes
        self.mate = mate

    @staticmethod
    def parse(command_str: str) -> "GoCommand":
        tokens = command_str.strip().split()
        tokens.pop(0)
        kwargs = {
            "depth": None,
            "movetime": None,
            "wtime": None,
            "btime": None,
            "winc": None,
            "binc": None,
            "infinite": False,
            "searchmoves": None,
            "ponder": False,
            "movestogo": None,
            "nodes": None,
            "mate": None,
        }

        keywords = ["depth", "movetime", "wtime", "btime", "winc", "binc", "infinite", "searchmoves", "ponder", "movestogo", "nodes", "mate"]

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token == "depth":
                kwargs["depth"] = int(tokens[i + 1])
                i += 2

            elif token == "movetime":
                kwargs["movetime"] = int(tokens[i + 1])
                i += 2

            elif token == "wtime":
                kwargs["wtime"] = int(tokens[i + 1])
                i += 2

            elif token == "btime":
                kwargs["btime"] = int(tokens[i + 1])
                i += 2

            elif token == "winc":
                kwargs["winc"] = int(tokens[i + 1])
                i += 2

            elif token == "binc":
                kwargs["binc"] = int(tokens[i + 1])
                i += 2

            elif token == "infinite":
                kwargs["infinite"] = True
                i += 1

            elif token == "searchmoves":
                i += 1
                searchmoves_list = []
                while i < len(tokens) and tokens[i] not in keywords:
                    searchmoves_list.append(tokens[i])
                    i += 1
                kwargs["searchmoves"] = searchmoves_list

            elif token == "ponder":
                kwargs["ponder"] = True
                i += 1

            elif token == "movestogo":
                kwargs["movestogo"] = (int)(tokens[i + 1])
                i += 2

            elif token == "nodes":
                kwargs["nodes"] = (int)(tokens[i + 1])
                i += 2

            elif token == "mate":
                kwargs["mate"] = (int)(tokens[i + 1])
                i += 2
            else:
                i += 1

        return GoCommand(**kwargs)

def parse_command(command_str: str) -> Command:
    if not command_str:
        raise ValueError("Empty command string")
    command_name = command_str.strip().split()[0]
    if command_name == "position":
        return PositionCommand.parse(command_str)
    elif command_name == "go":
        return GoCommand.parse(command_str)
    # Other commands
    else:
        raise ValueError(f"Unknown command: {command_name}")
        