from move import Move
from piece import Piece

def test_pawn_move():
    move = Move("e2e4")
    assert move.src_coords == (4, 1)
    assert move.target_coords == (4, 3)
    assert move.to_long_algebraic() == "e2e4"

def test_piece_move():
    move = Move("f3d4")
    assert move.src_coords == (5, 2)
    assert move.target_coords == (3, 3)
    assert move.to_long_algebraic() == "f3d4"

def test_capture_move():
    move = Move("e2d3")
    assert move.src_coords == (4, 1)
    assert move.target_coords == (3, 2)
    assert move.to_long_algebraic() == "e2d3"

def test_promotion_move():
    move = Move("e7e8q")
    assert move.src_coords == (4, 6)
    assert move.target_coords == (4, 7)
    assert move.promoted_to == Piece.QUEEN
    assert move.to_long_algebraic() == "e7e8q"

def test_piece_capture():
    move = Move("a1e4")
    assert move.src_coords == (0, 0)
    assert move.target_coords == (4, 3)
    assert move.to_long_algebraic() == "a1e4"
