from board import Board

def test_pawn_moves():
    board = Board(fen="8/3k4/8/8/8/8/1PK5/8 w - - 0 1")

    possible_moves = {m.to_long_algebraic() for m in board.get_possible_moves()}

    expected_moves = {"b2b3", "b2b4", "c2c3", "c2b3", "c2d3", "c2b1", "c2c1", "c2d1", "c2d2"}

    assert possible_moves == expected_moves

def test_knight_moves():
    board = Board(fen="8/8/8/8/3N4/8/2K5/8 w - - 0 1")

    possible_moves = {m.to_long_algebraic() for m in board.get_possible_moves()}

    expected_moves = {"d4c6", "d4e6", "d4b5", "d4f5", "d4b3", "d4f3", "d4e2", "c2c3", "c2b3", "c2d3", "c2b1", "c2c1", "c2d1", "c2d2", "c2b2"}

    assert possible_moves == expected_moves

def test_bishop_moves():
    board = Board(fen="8/8/8/8/8/8/2K5/2B5 w - - 0 1")

    possible_moves = {m.to_long_algebraic() for m in board.get_possible_moves()}

    expected_moves = {
        "c1b2", "c1a3", "c1d2", "c1e3", "c1f4", "c1g5", "c1h6", "c2c3", "c2b3", "c2d3", "c2b1", "c2d1", "c2d2", "c2b2"
    }
    assert possible_moves == expected_moves

def test_rook_moves():
    board = Board(fen="8/8/8/8/8/8/2K5/R7 w - - 0 1")

    possible_moves = {m.to_long_algebraic() for m in board.get_possible_moves()}

    expected_moves = {
        "a1a2", "a1a3", "a1a4", "a1a5", "a1a6", "a1a7", "a1a8",
        "a1b1", "a1c1", "a1d1", "a1e1", "a1f1", "a1g1", "a1h1",
        "c2c3", "c2b3", "c2d3", "c2b1", "c2c1", "c2d1", "c2d2", "c2b2"
        
    }
    assert possible_moves == expected_moves
def test_queen_moves():
    board = Board(fen="8/8/8/8/3Q4/8/2K5/8 w - - 0 1")

    possible_moves = {m.to_long_algebraic() for m in board.get_possible_moves()}

    expected_moves = {
        # Vertical and horizontal
        "d4d1", "d4d2", "d4d3", "d4d5", "d4d6", "d4d7", "d4d8",
        "d4a4", "d4b4", "d4c4", "d4e4", "d4f4", "d4g4", "d4h4",
        # Diagonal
        "d4c3", "d4b2", "d4a1", "d4e5", "d4f6", "d4g7", "d4h8",
        "d4c5", "d4b6", "d4a7", "d4e3", "d4f2", "d4g1",
        # King moves
        "c2c3", "c2b3", "c2d3", "c2b1", "c2c1", "c2d1", "c2d2", "c2b2"
    }
    assert possible_moves == expected_moves 

def test_king_moves():
    board = Board(fen="8/8/8/8/4K3/8/8/8 w - - 0 1")

    possible_moves = {m.to_long_algebraic() for m in board.get_possible_moves()}

    expected_moves = {
        "e4d3", "e4e3", "e4f3",
        "e4d4",         "e4f4",
        "e4d5", "e4e5", "e4f5"
    }
    assert possible_moves == expected_moves

