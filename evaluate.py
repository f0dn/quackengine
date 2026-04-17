class Evaluate:
    def __init__(self, score=None, mate=None):
        self.score = score
        self.mate = mate

    @staticmethod
    def normal(score):
        return Evaluate(score=score)

    @staticmethod
    def mate_in(x):
        return Evaluate(mate=x)
    
    def is_mate(self):
        return self.mate is not None

    def increment_mate(self):
        if self.is_mate():
            if self.mate > 0:
                return Evaluate.mate_in(self.mate + 1)
            else:
                return Evaluate.mate_in(self.mate - 1)
        return self

    def __lt__(self, other):
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