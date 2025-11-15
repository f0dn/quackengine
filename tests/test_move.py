from move import Move
from piece import Piece
from board import Board, Color

def test_pawn_move():
    move = Move.from_long_algebraic("e2e4")
    assert move.src_coords == (4, 1)
    assert move.target_coords == (4, 3)
    assert move.to_long_algebraic() == "e2e4"

def test_piece_move():
    move = Move.from_long_algebraic("f3d4")
    assert move.src_coords == (5, 2)
    assert move.target_coords == (3, 3)
    assert move.to_long_algebraic() == "f3d4"

def test_capture_move():
    move = Move.from_long_algebraic("e2d3")
    assert move.src_coords == (4, 1)
    assert move.target_coords == (3, 2)
    assert move.to_long_algebraic() == "e2d3"

def test_promotion_move():
    move = Move.from_long_algebraic("e7e8q")
    assert move.src_coords == (4, 6)
    assert move.target_coords == (4, 7)
    assert move.promoted_to == Piece.QUEEN
    assert move.to_long_algebraic() == "e7e8q"

def test_piece_capture():
    move = Move.from_long_algebraic("a1e4")
    assert move.src_coords == (0, 0)
    assert move.target_coords == (4, 3)
    assert move.to_long_algebraic() == "a1e4"

def test_board_possible_moves():
    # Position: only a white pawn on b2, white to move
    # This ensures exactly two legal pawn pushes: b2b3 and b2b4
    board = Board(fen="8/8/8/8/8/8/1P6/8 w - - 0 1")
    board.turn = 'w'

    # Normalize to string representation for comparison
    possible_moves = {m.to_long_algebraic() for m in board.get_possible_moves()}

    expected_moves = {"b2b3", "b2b4"}

    assert possible_moves == expected_moves