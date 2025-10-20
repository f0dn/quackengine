from board import Board

default_1 = "rnbqkbnr"
default_2 = "pppppppp"

chess_board =[[letter for letter in default_1],
              [letter for letter in default_2]]

for i in range(4):
    chess_board.append([None for _ in range(8)]) 

chess_board.append([letter for letter in default_2.upper()])
chess_board.append([letter for letter in default_1.upper()])

chess_board[5][7]= "p"
chess_board[5][0]= "q"
chess_board[6][1] = None
chess_board[6][4] = None

[print(row) for row in chess_board]
print("")

game_board = Board(fen=None)

# initialize the chess board
game_board.board = chess_board
print(game_board.get_possible_moves())
