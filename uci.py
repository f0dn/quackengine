from typing import List, Optional, Self, Type


class Command():
    @classmethod
    def parse(cls, command_str: str) -> Self:
        return cls()


class PositionCommand(Command):
    def __init__(self, startpos: bool, fen: Optional[str], moves: List[str]):
        self.startpos = startpos
        self.fen = fen
        self.moves = moves

    @classmethod
    def parse(cls, command_str: str) -> Self:
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

        return cls(startpos, fen, moves)


class GoCommand(Command):
    def __init__(
        self,
        depth: Optional[int] = None,
        movetime: Optional[int] = None,
        wtime: Optional[int] = None,
        btime: Optional[int] = None,
        winc: Optional[int] = None,
        binc: Optional[int] = None,
        infinite: bool = False,
        searchmoves: Optional[List[str]] = None,
        ponder: bool = False,
        movestogo: Optional[int] = None,
        nodes: Optional[int] = None,
        mate: Optional[int] = None,
    ):
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

    @classmethod
    def parse(cls, command_str: str) -> Self:
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

        keywords = set(kwargs.keys())

        i = 0
        while i < len(tokens):
            token = tokens[i]

            if token in {"depth", "movetime", "wtime", "btime", "winc", "binc", "movestogo", "nodes", "mate"}:
                kwargs[token] = int(tokens[i + 1])
                i += 2

            elif token == "infinite":
                kwargs["infinite"] = True
                i += 1

            elif token == "ponder":
                kwargs["ponder"] = True
                i += 1

            elif token == "searchmoves":
                i += 1
                searchmoves_list = []
                while i < len(tokens) and tokens[i] not in keywords:
                    searchmoves_list.append(tokens[i])
                    i += 1
                kwargs["searchmoves"] = searchmoves_list

            else:
                i += 1

        return cls(**kwargs)


class UCICommand(Command):
    pass


class IsReadyCommand(Command):
    pass


class StopCommand(Command):
    pass


class QuitCommand(Command):
    pass


class UCINewGameCommand(Command):
    pass


COMMAND_MAP: dict[str, Type[Command]] = {
    "position": PositionCommand,
    "go": GoCommand,
    "uci": UCICommand,
    "isready": IsReadyCommand,
    "stop": StopCommand,
    "quit": QuitCommand,
    "ucinewgame": UCINewGameCommand,
}


def parse_command(command_str: str) -> Command:
    if not command_str:
        raise ValueError("Empty command string")

    command_name = command_str.strip().split()[0]

    command_cls = COMMAND_MAP.get(command_name)
    if not command_cls:
        raise ValueError(f"Unknown command: {command_name}")

    return command_cls.parse(command_str)