class Move:
    def __init__(self, algebraic_notation):
        move_clean = algebraic_notation.replace("x", "")
        self.chess_piece = move_clean[0]
        self.src_square = move_clean[1:3]
        self.target_square = move_clean[-2:]

    def promotion_check(self):
        is_promoted = False
        if self.chess_piece == 'p' and self.target_square[1] in ['1', '8']:
            is_promoted = True
        return is_promoted

    def san_notation(self):
        return self.src_square + self.target_square
