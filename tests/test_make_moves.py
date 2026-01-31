from board import Board
from move import Move

def test_pawn_capture():
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    result_board = Board("rnbqkbnr/ppp1pppp/8/3P4/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 2")

    moves_str = "e2e4 d7d5 e4d5"

    moves = [Move.from_long_algebraic(move) for move in moves_str.split()]
    board.make_moves(moves)

    assert board.to_fen() == result_board.to_fen()

def test_allowed_castle():
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    result_board = Board("rn1qkbnr/ppp2ppp/3pb3/4p3/4P3/5N2/PPPPBPPP/RNBQ1RK1 b kq - 3 4")

    moves_str = "e2e4 e7e5 f1e2 d7d6 g1f3 c8e6 e1g1"

    moves = [Move.from_long_algebraic(move) for move in moves_str.split()]
    board.make_moves(moves)

    assert board.to_fen() == result_board.to_fen()

def test_castle_revoked():
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    result_board = Board("rnbq1bnr/ppppkppp/8/4p3/3PP3/8/PPP2PPP/RNBQKBNR w KQ - 1 3")

    moves_str = "e2e4 e7e5 d2d4 e8e7"

    moves = [Move.from_long_algebraic(move) for move in moves_str.split()]
    board.make_moves(moves)

    assert board.to_fen() == result_board.to_fen()

def test_en_passant_target():
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    result_board = Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")

    moves_str = "e2e4" # e2e4 d7d5 e4e5 

    moves = [Move.from_long_algebraic(move) for move in moves_str.split()]
    board.make_moves(moves)

    assert board.to_fen() == result_board.to_fen()
    
def test_en_passant_capture():
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    result_board = Board("rnbqkbnr/ppp1p1pp/5P2/3p4/8/8/PPPP1PPP/RNBQKBNR b KQkq - 0 3")

    moves_str = "e2e4 d7d5 e4e5 f7f5 e5f6"

    moves = [Move.from_long_algebraic(move) for move in moves_str.split()]
    board.make_moves(moves)

    assert board.to_fen() == result_board.to_fen()

def test_ep_target_no_capture():
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    inter_board = Board("rnbqkbnr/1ppppppp/8/p7/4P3/8/PPPP1PPP/RNBQKBNR w KQkq a6 0 2")
    result_board = Board("rnbqkbnr/1ppppppp/B7/p7/4P3/8/PPPP1PPP/RNBQK1NR b KQkq - 1 2")

    moves_str = "e2e4 a7a5"

    moves = [Move.from_long_algebraic(move) for move in moves_str.split()]
    board.make_moves(moves)

    assert board.to_fen() == inter_board.to_fen()

    moves_str = "f1a6"

    moves = [Move.from_long_algebraic(move) for move in moves_str.split()]
    board.make_moves(moves)

    assert board.to_fen() == result_board.to_fen()

def test_rook_bishop_capture(): # also removes castling on black queen side and restarts halfmove clock
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    result_board = Board("1nbqkbnr/1ppppppp/r7/p7/4P3/8/PPPP1PPP/RNBQK1NR w KQk - 0 3")

    moves_str = "e2e4 a7a5 f1a6 a8a6"

    moves = [Move.from_long_algebraic(move) for move in moves_str.split()]
    board.make_moves(moves)

    assert board.to_fen() == result_board.to_fen()

def test_both_half_revoke(): # continues previous by revoking castling on white king side and ensures halfmove clock continues
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    result_board = Board("1nbqkbnr/1ppppppp/1r6/p7/4P3/5N2/PPPP1PPP/RNBQK1R1 b Qk - 3 4")

    moves_str = "e2e4 a7a5 f1a6 a8a6 g1f3 a6b6 h1g1"

    moves = [Move.from_long_algebraic(move) for move in moves_str.split()]
    board.make_moves(moves)

    assert board.to_fen() == result_board.to_fen()