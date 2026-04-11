from engine import Engine

def test_evaluation():
    print("Evaluation Testing:")
    engine = Engine("6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0")
    print(engine.evaluate_position())
    engine = Engine("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    print(engine.evaluate_position())
    engine = Engine("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    print(engine.evaluate_position())
    engine = Engine("r1bqk1nr/1ppp1ppp/p1n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQkq - 0 5")
    print(engine.evaluate_position())
    engine = Engine("r1bqk1nr/1pppbppp/p1n5/8/2BPP3/5N2/PP3PPP/RNBQK2R w KQkq - 1 7")
    print(engine.evaluate_position())
    engine = Engine("R7/1bP2ppk/p6p/1p6/5n2/2N5/PP3PPP/6K1 b - - 0 26")
    print(engine.evaluate_position())
    engine = Engine("2Q5/5ppk/p6p/1p6/5n2/2N5/PP3PbP/6K1 w - - 0 28")
    print(engine.evaluate_position())
    engine = Engine("8/5ppk/7p/1Q6/8/2N2b1n/PP3P1P/6K1 w - - 1 30")
    print(engine.evaluate_position())
    engine = Engine("rnbqkbnr/pp2pppp/2p5/8/2pP4/4P3/PP3PPP/RNBQKBNR w KQkq - 0 4")
    print(engine.evaluate_position())
    engine = Engine("r5nr/pp1b2k1/2pPp2p/4P1bQ/2P5/3B4/PP3PPP/R3K2R w KQ - 1 18")
    print(engine.evaluate_position())
    #assert engine.evaluate_position() is None

def test_capture_threat():
    print("King Evaluation Testing:")
    engine = Engine("6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0")
    print(engine.evaluate_capture_threats())
    engine = Engine("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    print(engine.evaluate_capture_threats())
    engine = Engine("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    print(engine.evaluate_capture_threats())
    engine = Engine("r1bqk1nr/1ppp1ppp/p1n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQkq - 0 5")
    print(engine.evaluate_capture_threats())
    engine = Engine("r1bqk1nr/1pppbppp/p1n5/8/2BPP3/5N2/PP3PPP/RNBQK2R w KQkq - 1 7")
    print(engine.evaluate_capture_threats())
    engine = Engine("R7/1bP2ppk/p6p/1p6/5n2/2N5/PP3PPP/6K1 b - - 0 26")
    print(engine.evaluate_capture_threats())
    engine = Engine("2Q5/5ppk/p6p/1p6/5n2/2N5/PP3PbP/6K1 w - - 0 28")
    print(engine.evaluate_capture_threats())
    engine = Engine("8/5ppk/7p/1Q6/8/2N2b1n/PP3P1P/6K1 w - - 1 30")
    print(engine.evaluate_capture_threats())
    engine = Engine("rnbqkbnr/pp2pppp/2p5/8/2pP4/4P3/PP3PPP/RNBQKBNR w KQkq - 0 4")
    print(engine.evaluate_capture_threats())
    engine = Engine("r5nr/pp1b2k1/2pPp2p/4P1bQ/2P5/3B4/PP3PPP/R3K2R w KQ - 1 18")
    print(engine.evaluate_capture_threats())
    #assert engine.evaluate_capture_threats() is None

def test_king_safety():
    print("King Evaluation Testing:")
    engine = Engine("6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0")
    print(engine.evaluate_king_safety())
    engine = Engine("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    print(engine.evaluate_king_safety())
    engine = Engine("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    print(engine.evaluate_king_safety())
    engine = Engine("r1bqk1nr/1ppp1ppp/p1n5/2b1p3/2B1P3/2P2N2/PP1P1PPP/RNBQK2R w KQkq - 0 5")
    print(engine.evaluate_king_safety())
    engine = Engine("r1bqk1nr/1pppbppp/p1n5/8/2BPP3/5N2/PP3PPP/RNBQK2R w KQkq - 1 7")
    print(engine.evaluate_king_safety())
    engine = Engine("R7/1bP2ppk/p6p/1p6/5n2/2N5/PP3PPP/6K1 b - - 0 26")
    print(engine.evaluate_king_safety())
    engine = Engine("2Q5/5ppk/p6p/1p6/5n2/2N5/PP3PbP/6K1 w - - 0 28")
    print(engine.evaluate_king_safety())
    engine = Engine("8/5ppk/7p/1Q6/8/2N2b1n/PP3P1P/6K1 w - - 1 30")
    print(engine.evaluate_king_safety())
    engine = Engine("rnbqkbnr/pp2pppp/2p5/8/2pP4/4P3/PP3PPP/RNBQKBNR w KQkq - 0 4")
    print(engine.evaluate_king_safety())
    engine = Engine("r5nr/pp1b2k1/2pPp2p/4P1bQ/2P5/3B4/PP3PPP/R3K2R w KQ - 1 18")
    print(engine.evaluate_king_safety())
    #assert engine.evaluate_king_safety() is None
    
def test_evaluate_pawn_formation():
    engine = Engine("rnb1r3/pppk4/3p1p1p/3Pp3/2P5/2P3P1/PP3PBP/R4RK1 w KQkq - 0 1")
    assert engine.evaluate_pawn_formation() == 0
    engine = Engine("3k4/5p2/8/4p3/P6P/1P5P/8/4K3 w - - 0 1")
    assert engine.evaluate_pawn_formation() == 200
    engine = Engine("6k1/B5pp/3bpp2/8/Pp6/1P2PKP1/2r2P1P/R7 b KQkq - 0 1")
    assert engine.evaluate_pawn_formation() == 110
    engine = Engine("6k1/B5pp/8/8/8/5K2/8/R7 b KQkq - 0 1")
    assert engine.evaluate_pawn_formation() == -220
    engine = Engine("6k1/B5pp/8/8/8/5K2/2P5/R7 b KQkq - 0 1")
    assert engine.evaluate_pawn_formation() == -110
    
def test_evaluate_bishops():
    engine = Engine("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    assert engine.evaluate_bishops() == 0
    engine = Engine("rnbqk2r/ppp3pp/3p1p1n/4p3/1bB1P3/3P1P2/PPP3PP/RN1QK1NR b KQkq - 0 1")
    assert engine.evaluate_bishops() == -45
    engine = Engine("rn1qk1nr/pp2p2p/7b/2ppNpp1/4PP2/8/PPPP2PP/RNBQKB1R w KQkq - 0 1")
    assert engine.evaluate_bishops() == 45
    engine = Engine("rnbqkbnr/p3pppp/2p5/1p6/P1pP4/4P3/1P3PPP/RNBQKBNR b KQkq - 0 1")
    assert engine.evaluate_bishops() == 0
    engine = Engine("1r1r2k1/p4pb1/2Bp1np1/q3p1Bp/4P3/2N2Q2/PP3PPP/1R1R2K1 b KQkq - 0 1")
    assert engine.evaluate_bishops() == 45