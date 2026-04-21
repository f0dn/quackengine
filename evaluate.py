from board import Color

class Evaluation:
    def __init__(self, score=None, mate=None):
        self.score = score
        self.mate = mate

    @staticmethod
    def normal(score):
        return Evaluation(score=score)

    @staticmethod
    def mate_in(x, color):
        if color == Color.WHITE:
            return Evaluation(mate=(x + 1))
        else:
            return Evaluation(mate=-(x + 1))
    
    def is_mate(self):
        return self.mate is not None

    def increment_mate(self):
        if self.is_mate():
            if self.mate > 0:
                return Evaluation(mate=self.mate + 1)
            else:
                return Evaluation(mate=self.mate - 1)
        return self

    def __lt__(self, other):
        if not isinstance(other, Evaluation):
            return NotImplemented
        
        if self.is_mate() and other.is_mate():
            return self.mate < other.mate

        if self.is_mate():
            return self.mate < 0

        if other.is_mate():
            return other.mate > 0

        return self.score < other.score

    def __gt__(self, other):
        return other < self

    def __eq__(self, other):
        return self.score == other.score and self.mate == other.mate
    
    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other