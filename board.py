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

        pathways = {'N': [(-2, -1), (-2, 1), (-1,-2), (-1,2), (1,2), (1,-2), (2,-1), (2,1)],
                      'B': [(-1, -1), (-1,1), (1,1), (1,-1)],
                      'R': [(-1, 0), (1,0), (0,1), (0,-1)],
                      'Q': [(-1, -1), (-1,1), (1,1), (1,-1), (-1, 0), (1,0), (0,1), (0,-1)],
                      'K': [(-1, -1), (-1,1), (1,1), (1,-1), (-1, 0), (1,0), (0,1), (0,-1)],
                      'P': [(1, -1), (1, 1), (1, 0) if self.turn == 'w' else (-1, 0)]}
    
    
        for i in range(8):
            for j in range(8):
                # keep track of starting position
                position = (i, j)

                # record all possible bishop moves
                if chess_board[i][j] == ('B' if self.turn == 'w' else 'b'):
                    directions = pathways['B']
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

                # record all possible knight moves
                elif chess_board[i][j] == ('N' if self.turn == 'w' else 'n'):
                    directions = pathways['N']

                    for direction in directions:
                        new_point = (position[0] + direction[0], position[1] + direction[1])  
                        if 0 <= new_point[0] <= 7 and 0 <= new_point[1] <= 7:
                            # Ensure that move is not friendly fire
                            if self.turn == 'w':
                                if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].isupper():
                                    continue
                                possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                            else:
                                if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].islower():
                                    continue
                                possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")

                # record all possible rook moves
                elif chess_board[i][j] == ('R' if self.turn == 'w' else 'r'):
                    directions = pathways['R']
                    for direction in directions:
                        new_point = (position[0] + direction[0], position[1] + direction[1])                      
                        while 0 <= new_point[0] <= 7 and 0 <= new_point[1] <= 7:   
                            if self.turn == 'w':                        
                                # Check if an opponent or teammate is on the path                        
                                if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].islower():
                                    possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                                    break
                                    
                                elif chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].isupper():
                                    break
                            else:
                                # Check if an opponent or teammate is on the path                        
                                if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].isupper():
                                    possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                                    break
                                    
                                elif chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].islower():
                                    break
                            possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                            new_point = (new_point[0] + direction[0], new_point[1] + direction[1])

                # record all possible queen moves
                elif chess_board[i][j] == ('Q' if self.turn == 'w' else 'q'):
                    directions = pathways['Q']
                    for direction in directions:
                        new_point = (position[0] + direction[0], position[1] + direction[1])                      
                        while 0 <= new_point[0] <= 7 and 0 <= new_point[1] <= 7:   
                            if self.turn == 'w':                        
                                # Check if an opponent or teammate is on the path                        
                                if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].islower():
                                    possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                                    break
                                    
                                elif chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].isupper():
                                    break
                            else:
                                # Check if an opponent or teammate is on the path                        
                                if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].isupper():
                                    possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                                    break
                                    
                                elif chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].islower():
                                    break
                            possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                            new_point = (new_point[0] + direction[0], new_point[1] + direction[1])
                # record all possible king moves
                elif chess_board[i][j] == ('K' if self.turn == 'w' else 'k'):
                    directions = pathways['K']
                    for direction in directions:
                        new_point = (position[0] + direction[0], position[1] + direction[1])  
                        if 0 <= new_point[0] <= 7 and 0 <= new_point[1] <= 7:
                            # Ensure that move is not friendly fire
                            if self.turn == 'w':
                                if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].isupper():
                                    continue
                                possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                            else:
                                if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].islower():
                                    continue
                                possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                # record all possible pawn moves
                elif chess_board[i][j] == ('P' if self.turn == 'w' else 'p'):
                    directions = pathways['P']

                    for direction in directions:
                        new_point = (position[0] + direction[0], position[1] + direction[1])  
                        if 0 <= new_point[0] <= 7 and 0 <= new_point[1] <= 7:
                            # Ensure that move is not friendly fire
                            if direction == (1, -1) or direction == (1, 1):
                                if self.turn == 'w':
                                    if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].islower():
                                        possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                                else:
                                    if chess_board[new_point[0]][new_point[1]] != None and chess_board[new_point[0]][new_point[1]].isupper():
                                        possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                            else:
                                while chess_board[new_point[0]][new_point[1]] == None:
                                    possible_moves.append(f"{chr(1+j+96)}{i+1}{chr(new_point[1]+1+96)}{new_point[0]+1}")
                                    # Check for initial 2-square move
                                    if (self.turn == 'w' and i == 1) or (self.turn == 'b' and i == 6):
                                        new_point = (new_point[0] + direction[0], new_point[1] + direction[1])
                                    else:
                                        break
        return sorted(set(possible_moves))
