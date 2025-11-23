from board import Board

def test_board_setup():
    board = Board("6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0")
    assert board.to_fen() == "6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0"
    board = Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    assert board.to_fen() == "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
    board = Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    assert board.to_fen() == "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
    board = Board("r1bqk1nr/1ppp1ppp/p1n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQkq - 0 5")
    assert board.to_fen() == "r1bqk1nr/1ppp1ppp/p1n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQkq - 0 5"
    board = Board("r1bqk1nr/1pppbppp/p1n5/8/2BPP3/5N2/PP3PPP/RNBQK2R w KQkq - 1 7")
    assert board.to_fen() == "r1bqk1nr/1pppbppp/p1n5/8/2BPP3/5N2/PP3PPP/RNBQK2R w KQkq - 1 7"
    board = Board("R7/1bP2ppk/p6p/1p6/5n2/2N5/PP3PPP/6K1 b - - 0 26")
    assert board.to_fen() == "R7/1bP2ppk/p6p/1p6/5n2/2N5/PP3PPP/6K1 b - - 0 26"
    board = Board("2Q5/5ppk/p6p/1p6/5n2/2N5/PP3PbP/6K1 w - - 0 28")
    assert board.to_fen() == "2Q5/5ppk/p6p/1p6/5n2/2N5/PP3PbP/6K1 w - - 0 28"
    board = Board("8/5ppk/7p/1Q6/8/2N2b1n/PP3P1P/6K1 w - - 1 30")
    assert board.to_fen() == "8/5ppk/7p/1Q6/8/2N2b1n/PP3P1P/6K1 w - - 1 30"
    board = Board("rnbqkbnr/pp2pppp/2p5/8/2pP4/4P3/PP3PPP/RNBQKBNR w KQkq - 0 4")
    assert board.to_fen() == "rnbqkbnr/pp2pppp/2p5/8/2pP4/4P3/PP3PPP/RNBQKBNR w KQkq - 0 4"
    board = Board("r5nr/pp1b2k1/2pPp2p/4P1bQ/2P5/3B4/PP3PPP/R3K2R w KQ - 1 18")
    assert board.to_fen() == "r5nr/pp1b2k1/2pPp2p/4P1bQ/2P5/3B4/PP3PPP/R3K2R w KQ - 1 18"