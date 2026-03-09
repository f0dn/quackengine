from engine import Engine
import time

def test_specified_depth(capsys):
    engine = Engine()
    depth = 2 # MODIFY IF NEEDED

    engine.handle_input("position startpos moves e2e4 e7e5")
    engine.handle_input(f"go depth {depth}")

    engine.search_thread.join()

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split('\n')

    assert len(output_lines) == (depth + 1)
    

def test_infinite(capsys):
    engine = Engine()

    engine.handle_input("position startpos moves e2e4 e7e5")
    engine.handle_input("go infinite")
    time.sleep(7)
    engine.handle_input("stop")

    captured = capsys.readouterr()
    output_lines = captured.out.strip().split('\n')

    recent_line = output_lines[-2].split()
    bestmove_line = output_lines[-1].split()

    assert bestmove_line[1] == recent_line[9]