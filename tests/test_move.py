from move import Move

def square_convert(coords):
    return chr(coords[0] + ord('a')) + str(coords[1] + 1)

def test_pawn_move():
    move = Move("pe2e4")
    assert move.chess_piece == "P"
    assert square_convert(move.src_coords) == "e2"
    assert square_convert(move.target_coords) == "e4"
    assert move.to_long_algebraic() == "e2e4"

def test_piece_move():
    move = Move("Nf3d4")
    assert move.chess_piece == "N"
    assert square_convert(move.src_coords) == "f3"
    assert square_convert(move.target_coords) == "d4"
    assert move.to_long_algebraic() == "f3d4"

def test_capture_move():
    move = Move("pe2xd3")
    assert move.chess_piece == "P"
    assert square_convert(move.src_coords) == "e2"
    assert square_convert(move.target_coords) == "d3"
    assert move.is_capture is True
    assert move.to_long_algebraic() == "e2d3"

def test_promotion_move():
    move = Move("pe7e8q")
    assert move.chess_piece == "P"
    assert square_convert(move.src_coords) == "e7"
    assert square_convert(move.target_coords) == "e8"
    assert move.promoted_to == "q"
    assert move.to_long_algebraic() == "e7e8q"

def test_piece_capture():
    move = Move("Qa1xe4")
    assert move.chess_piece == "Q"
    assert square_convert(move.src_coords) == "a1"
    assert square_convert(move.target_coords) == "e4"
    assert move.is_capture is True
    assert move.to_long_algebraic() == "a1e4"
