from evaluate import Evaluation
from board import Color

def test_normal_positive():
    e = Evaluation.normal(100)
    assert e.score == 100
    assert e.mate is None

def test_mate_in_0_white_is_positive():
    e = Evaluation.mate_in(0, Color.WHITE)
    assert e.is_mate()
    assert e.mate > 0

def test_mate_in_0_black_is_negative():
    e = Evaluation.mate_in(0, Color.BLACK)
    assert e.is_mate()
    assert e.mate < 0

def test_mate_in_3_white():
    e = Evaluation.mate_in(3, Color.WHITE)
    assert e.mate == 4

def test_increment_white_mate():
    e = Evaluation.mate_in(0, Color.WHITE)
    assert e.increment_mate().mate == 2

def test_increment_black_mate():
    e = Evaluation.mate_in(0, Color.BLACK)
    assert e.increment_mate().mate == -2