class Slot:
    def __init__(self, index=None, position=None, pieces=None):
        """
        An object representing a slot (triangle).
        :param index: the canvas widget index
        :param position: the position on the board
        :param pieces: a list of the pieces residing here
        """
        if pieces is None:
            pieces = []
        self.index = index
        self.position = position
        self.pieces = pieces
