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
    def __init__(self, depth: Optional[int] = None, movetime: Optional[int] = None, wtime: Optional[int] = None, btime: Optional[int] = None, winc: Optional[int] = None, binc: Optional[int] = None, infinite: bool = False):
        self.depth = depth
        self.movetime = movetime
        self.wtime = wtime
        self.btime = btime
        self.winc = winc
        self.binc = binc
        self.infinite = infinite

    @staticmethod
    def parse(command_str: str) -> "GoCommand":
        tokens = command_str.strip().split()
        tokens.pop(0)

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
        