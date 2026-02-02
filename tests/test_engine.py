from engine import Engine
from board import Board
import random
from piece import Piece, Color


fen = "6k1/5p2/6p1/8/7p/8/6PP/6K1 b - - 0 0"  # Starting with an empty board
endgame = Board(fen)

def test_best_move_is_valid():
    board = endgame
    engine = Engine(board)
    
    best_endgame_move = engine.best_endgame_move()
    
    possible_moves = board.get_possible_moves()
    assert best_endgame_move in possible_moves


def test_best_move_not_none():
    board = endgame
    engine = Engine(board)
    best_endgame_move = engine.best_endgame_move()
    assert best_endgame_move is not None


def test_best_move_multiple_times():
    for i in range(5):
        board = endgame
        engine = Engine(board)
        best_endgame_move = engine.best_endgame_move()
        possible_moves = board.get_possible_moves()
        
        assert best_endgame_move in possible_moves


def test_best_move_same_position_same_result():
    board = endgame
    engine = Engine(board)
    
    move1 = engine.best_endgame_move()
    move2 = engine.best_endgame_move()
    
    assert move1 == move2


def test_best_move_different_positions():
    board1 = endgame
    engine1 = Engine(board1)
    move1 = engine1.best_endgame_move()
    
    board2 = Board("3k4/2n2B2/1KP5/2B2p2/5b1p/7P/8/8 b - - 0 0")
    engine2 = Engine(board2)
    move2 = engine2.best_endgame_move()
    
    assert move1 is not None
    assert move2 is not None