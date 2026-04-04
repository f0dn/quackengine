from engine import Engine
from board import Board

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