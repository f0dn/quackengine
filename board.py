import numpy as np

class Board:
    board = [[None for _ in range(8)] for _ in range(8)]
    turn = "w"
    castling_avail = "KQkq"
    recent_en_passant_target = "-"
    halfmove_clock = 0
    fullmoves = 1
    fen = ""

    def __init__(self, fen):
        self.fen = fen
        """
        Use FEN to initialize board?
        """

    def to_fen(self):
        fen = ""

        # Getting where the pieces are from the board
        rows = [] 
        for row in self.board:
            empty = 0
            row = ""

            for square in row:
                if square is None:
                    empty += 1
                else:
                    if empty > 0:
                        row += str(empty)
                        empty = 0
                    
                    row += square
            
            if empty > 0:
                row += str(empty)
            
            rows.append(row)

        # First Field: piece placement
        fen = '/'.join(rows)

        # Can be "compressed" to reduce the lines
        # Second Field: active color
        fen += " " + self.turn

        # Third Field: castling availability
        fen += " " + self.castling_avail

        # Fourth Field: en passant target square
        fen += " " + self.recent_en_passant_target

        # Fifth Field: halfmove clock
        fen += " " + self.halfmove_clock

        # Sixth Field: number of fullmove
        fen += " " + self.fullmoves

        self.fen = fen
        return fen

    def get_possible_moves(self):
        """
        Returns a list of possible moves on the board 
        with a move being encoded in long_algebraic form 'e1e4'
        """
        chess_board = self.board

        # Reverse the chess board
        chess_board.reverse()
        possible_moves = []

        for i in range(8):
            for j in range(8):
                # record all possible bishop moves
                if chess_board[i][j] == 'B' or chess_board[i][j] == 'b':
                    # keep track of starting position
                    position = (i, j)

                    directions = [(-1, -1), (-1,1), (1,1), (1,-1)]
                    for direction in directions:
                        new_point = (position[0] + direction[0], position[1] + direction[1])                      
                        while 0 <= new_point[0] <= 7 and 0 <= new_point[1] <= 7:   
                            if self.turn == 'w':                        
                                # Check if an opponent or teammate is on the diagonal path                        
                                if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].islower():
                                    possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                                    break
                                    
                                elif chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].isupper():
                                    break
                            else:
                                # Check if an opponent or teammate is on the diagonal path                        
                                if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].isupper():
                                    possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                                    break
                                    
                                elif chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].islower():
                                    break

                            possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                            new_point = (new_point[0] + direction[0], new_point[1] + direction[1])
        return possible_moves
