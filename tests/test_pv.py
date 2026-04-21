from engine import Engine
from board import Board
from evaluate import Evaluation

board = Board("8/P2p1b2/2p1Pr2/1B3PK1/n1p5/1k6/5p1p/B3N3 w - - 0 1")
def test_lengths():
    engine = Engine()
    for depth in range(1, 3):
        __, moves = engine.minimax(board, depth, Evaluation.normal(float('-inf')), Evaluation.normal(float('inf')))
        assert len(moves) == depth
