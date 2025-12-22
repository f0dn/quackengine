from engine import Engine
from board import Board

board = Board("r2qkb1r/1ppn1p2/p1np2p1/4p2p/B1P1P2P/5Q2/PP1PNPP1/R1B1K2R w KQkq h6 0 11")
def test_minimax():
    engine = Engine()
    __, move = engine.minimax(board, 2, float('-inf'), float('inf'))
    assert move.to_long_algebraic() == ""
