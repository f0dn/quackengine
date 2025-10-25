import pytest
from src.move import Move

def test_pawn_move():
    move = Move("pe2e4")
    assert move.src_square == "e2"
    assert move.target_square == "e4"
    assert move.san_notation() == "e2e4"

def test_piece_move():
    move = Move("Nf3d4")
    assert move.chess_piece == "N"
    assert move.src_square == "f3"
    assert move.target_square == "d4"
    assert move.san_notation() == "f3d4"

def test_capture_move():
    move = Move("pe2xd3")
    assert move.src_square == "e2"
    assert move.target_square == "d3"
    assert move.san_notation() == "e2d3"
