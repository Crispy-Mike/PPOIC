
class VisitNotMarkedError(Exception):

    def __init__(self, message="Сначала расставьте посещения!"):
        super().__init__(message)