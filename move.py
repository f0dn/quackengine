from piece import Piece

class Move:
    from piece import Piece

class Move:
    def __init__(self, from_r, from_c, to_r, to_c, promoted_to=None):
        self.src_coords = (from_r, from_c)
        self.target_coords = (to_r, to_c)
        self.promoted_to = promoted_to

    @staticmethod
    def from_long_algebraic(move: str):
        promoted_to = None

        if len(move) > 4 and move[-1].isalpha() and move[-1].islower():
            promoted_to = Piece(move[-1].upper())
            move = move[:-1]

        #(file, rank)
        src_coords = (ord(move[0]) - ord('a'), int(move[1]) - 1)
        target_coords = (ord(move[2]) - ord('a'), int(move[3]) - 1)

        return Move(src_coords[0], src_coords[1], target_coords[0], target_coords[1], promoted_to)
    
    def to_long_algebraic(self):
        src = chr(self.src_coords[0] + ord('a')) + str(self.src_coords[1] + 1)
        target = chr(self.target_coords[0] + ord('a')) + str(self.target_coords[1] + 1)
        result = src + target
        if self.promoted_to:
            result += self.promoted_to.value.lower()
        return result

