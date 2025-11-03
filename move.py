from piece import Color, Piece

class Move:
    def __init__(self, move: str):
        self.promoted_to = None

        if len(move) > 4 and move[-1].isalpha() and move[-1].islower():
            self.promoted_to = Piece(move[-1].toupper())
            move = move[:-1]

        #(file, rank)
        self.src_coords = (ord(move[0]) - ord('a'), int(move[1]) - 1)
        self.target_coords = (ord(move[2]) - ord('a'), int(move[3]) - 1)

    def to_long_algebraic(self):
        src = chr(self.src_coords[0] + ord('a')) + str(self.src_coords[1] + 1)
        target = chr(self.target_coords[0] + ord('a')) + str(self.target_coords[1] + 1)
        result = src + target
        if self.promoted_to:
            result += self.promoted_to.value.tolower()
        return result
