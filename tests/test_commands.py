from engine import Engine
from uci import parse_command, PositionCommand, GoCommand, UCICommand, IsReadyCommand, QuitCommand, SetOptionCommand, UCINewGameCommand, StopCommand

#testing engine handle_input()
def test_isready(capsys):
    engine = Engine()
    engine.handle_input("isready")
    captured = capsys.readouterr()
    assert captured.out.strip() == "readyok"

def test_postition():
    engine = Engine()
    engine.handle_input("position startpos")
    print(engine.board)
    assert engine.board.to_fen() == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

def test_stop():
    from engine import Engine
    engine = Engine()
    engine.handle_input("stop")
    assert engine.stop_requested is True
    assert engine.searching is False

def test_setoption():
    from engine import Engine
    engine = Engine()
    engine.handle_input("setoption name Hash value 64")
    assert engine.options_dict["Hash"] == "64"

#testing uci parse_command()
def test_position_startpos():
    cmd = parse_command("position startpos")
    assert isinstance(cmd, PositionCommand)
    assert cmd.startpos is True
    assert cmd.fen is None
    assert cmd.moves == []

def test_position_startpos_with_moves():
    cmd = parse_command("position startpos moves e2e4 e7e5")
    assert cmd.startpos is True
    assert cmd.moves is not None
    assert len(cmd.moves) == 2

def test_go_depth():
    cmd = parse_command("go depth 10")
    assert isinstance(cmd, GoCommand)
    assert cmd.depth == 10

def test_uci_command():
    cmd = parse_command("uci")
    assert isinstance(cmd, UCICommand)

def test_isready_command():
    cmd = parse_command("isready")
    assert isinstance(cmd, IsReadyCommand)

def test_stop_command():
    cmd = parse_command("stop")
    assert isinstance(cmd, StopCommand)

def test_quit_command():
    cmd = parse_command("quit")
    assert isinstance(cmd, QuitCommand)

def test_ucinewgame_command():
    cmd = parse_command("ucinewgame")
    assert isinstance(cmd, UCINewGameCommand)

def test_setoption_name_value():
    cmd = parse_command("setoption name Hash value 128")
    assert isinstance(cmd, SetOptionCommand)
    assert cmd.name == "Hash"
    assert cmd.value == "128"
