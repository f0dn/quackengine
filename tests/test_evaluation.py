from board import Board

def test_evaluation():
    print("Evaluation Testing:")
    board = Board("6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0")
    print(board.evaluate_position())
    board = Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    print(board.evaluate_position())
    board = Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    print(board.evaluate_position())
    board = Board("r1bqk1nr/1ppp1ppp/p1n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQkq - 0 5")
    print(board.evaluate_position())
    board = Board("r1bqk1nr/1pppbppp/p1n5/8/2BPP3/5N2/PP3PPP/RNBQK2R w KQkq - 1 7")
    print(board.evaluate_position())
    board = Board("R7/1bP2ppk/p6p/1p6/5n2/2N5/PP3PPP/6K1 b - - 0 26")
    print(board.evaluate_position())
    board = Board("2Q5/5ppk/p6p/1p6/5n2/2N5/PP3PbP/6K1 w - - 0 28")
    print(board.evaluate_position())
    board = Board("1Q6/5ppk/p6p/1p6/5n2/2N5/PP3PbP/6K1 b - - 1 28")
    print(board.evaluate_position())
    board = Board("8/5ppk/p6p/1p3Q2/5n2/2N5/PP3PbP/6K1 b - - 1 28")
    print(board.evaluate_position())
    board = Board("8/5ppk/7p/1Q6/8/2N2b1n/PP3P1P/6K1 w - - 1 30")
    print(board.evaluate_position())
    board = Board("rnbqkbnr/pp2pppp/2p5/8/2pP4/4P3/PP3PPP/RNBQKBNR w KQkq - 0 4")
    print(board.evaluate_position())
    board = Board("r5nr/pp1b2k1/2pPp2p/4P1bQ/2P5/3B4/PP3PPP/R3K2R w KQ - 1 18")
    print(board.evaluate_position())
    #assert board.evaluate_position() is None

def test_capture_threat():
    print("King Evaluation Testing:")
    board = Board("6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0")
    print(board.evaluate_capture_threats())
    board = Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    print(board.evaluate_capture_threats())
    board = Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    print(board.evaluate_capture_threats())
    board = Board("r1bqk1nr/1ppp1ppp/p1n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQkq - 0 5")
    print(board.evaluate_capture_threats())
    board = Board("r1bqk1nr/1pppbppp/p1n5/8/2BPP3/5N2/PP3PPP/RNBQK2R w KQkq - 1 7")
    print(board.evaluate_capture_threats())
    board = Board("R7/1bP2ppk/p6p/1p6/5n2/2N5/PP3PPP/6K1 b - - 0 26")
    print(board.evaluate_capture_threats())
    board = Board("2Q5/5ppk/p6p/1p6/5n2/2N5/PP3PbP/6K1 w - - 0 28")
    print(board.evaluate_capture_threats())
    board = Board("8/5ppk/7p/1Q6/8/2N2b1n/PP3P1P/6K1 w - - 1 30")
    print(board.evaluate_capture_threats())
    board = Board("rnbqkbnr/pp2pppp/2p5/8/2pP4/4P3/PP3PPP/RNBQKBNR w KQkq - 0 4")
    print(board.evaluate_capture_threats())
    board = Board("r5nr/pp1b2k1/2pPp2p/4P1bQ/2P5/3B4/PP3PPP/R3K2R w KQ - 1 18")
    print(board.evaluate_capture_threats())
    #assert board.evaluate_capture_threats() is None

def test_king_safety():
    print("King Evaluation Testing:")
    board = Board("6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0")
    print(board.evaluate_king_safety())
    board = Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    print(board.evaluate_king_safety())
    board = Board("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    print(board.evaluate_king_safety())
    board = Board("r1bqk1nr/1ppp1ppp/p1n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQkq - 0 5")
    print(board.evaluate_king_safety())
    board = Board("r1bqk1nr/1pppbppp/p1n5/8/2BPP3/5N2/PP3PPP/RNBQK2R w KQkq - 1 7")
    print(board.evaluate_king_safety())
    board = Board("R7/1bP2ppk/p6p/1p6/5n2/2N5/PP3PPP/6K1 b - - 0 26")
    print(board.evaluate_king_safety())
    board = Board("2Q5/5ppk/p6p/1p6/5n2/2N5/PP3PbP/6K1 w - - 0 28")
    print(board.evaluate_king_safety())
    board = Board("8/5ppk/7p/1Q6/8/2N2b1n/PP3P1P/6K1 w - - 1 30")
    print(board.evaluate_king_safety())
    board = Board("rnbqkbnr/pp2pppp/2p5/8/2pP4/4P3/PP3PPP/RNBQKBNR w KQkq - 0 4")
    print(board.evaluate_king_safety())
    board = Board("r5nr/pp1b2k1/2pPp2p/4P1bQ/2P5/3B4/PP3PPP/R3K2R w KQ - 1 18")
    print(board.evaluate_king_safety())
    #assert board.evaluate_king_safety() is None
    
def test_evaluate_pawn_formation():
    board = Board("rnb1r3/pppk4/3p1p1p/3Pp3/2P5/2P3P1/PP3PBP/R4RK1 w KQkq - 0 1")
    assert board.evaluate_pawn_formation() == 0
    board = Board("3k4/5p2/8/4p3/P6P/1P5P/8/4K3 w - - 0 1")
    assert board.evaluate_pawn_formation() == 200
    board = Board("6k1/B5pp/3bpp2/8/Pp6/1P2PKP1/2r2P1P/R7 b KQkq - 0 1")
    assert board.evaluate_pawn_formation() == 110
    board = Board("6k1/B5pp/8/8/8/5K2/8/R7 b KQkq - 0 1")
    assert board.evaluate_pawn_formation() == -220
    board = Board("6k1/B5pp/8/8/8/5K2/2P5/R7 b KQkq - 0 1")
    assert board.evaluate_pawn_formation() == -110
    
def test_evaluate_bishops():
    board = Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert board.evaluate_bishops() == 0
    board = Board("rnbqk2r/ppp3pp/3p1p1n/4p3/1bB1P3/3P1P2/PPP3PP/RN1QK1NR b KQkq - 0 1")
    assert board.evaluate_bishops() == -45
    board = Board("rn1qk1nr/pp2p2p/7b/2ppNpp1/4PP2/8/PPPP2PP/RNBQKB1R w KQkq - 0 1")
    assert board.evaluate_bishops() == 45
    board = Board("rnbqkbnr/p3pppp/2p5/1p6/P1pP4/4P3/1P3PPP/RNBQKBNR b KQkq - 0 1")
    assert board.evaluate_bishops() == 0
    board = Board("1r1r2k1/p4pb1/2Bp1np1/q3p1Bp/4P3/2N2Q2/PP3PPP/1R1R2K1 b KQkq - 0 1")
    assert board.evaluate_bishops() == 45
