class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __lt__(self, other):
        return self.score < other.score

    def __le__(self, other):
        return self.score <= other.score

    def __gt__(self, other):
        return self.score > other.score

    def __ge__(self, other):
        return self.score >= other.score

    def __eq__(self, other):
        if not isinstance(other, Student):
            return False
        return self.score == other.score and self.name == other.name

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"Student('{self.name}', {self.score})"
