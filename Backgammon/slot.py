class Slot:
    def __init__(self, index=None, position=None, pieces=None):
        if pieces is None:
            pieces = []
        self.index = index
        self.position = position
        self.pieces = pieces