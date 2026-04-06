from uci import parse_command, PositionCommand, GoCommand, UCICommand, IsReadyCommand, QuitCommand, SetOptionCommand, UCINewGameCommand, StopCommand

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
