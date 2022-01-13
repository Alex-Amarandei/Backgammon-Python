class Piece:
    def __init__(self, index=None, position=None, slot=None, color=None):
        """
        An object representing a backgammon piece.
        :param index: the canvas widget index
        :param position: the position in the initial board configuration
        :param slot: the slot on which the piece resides
        :param color: White or Black
        """
        self.index = index
        self.position = position
        self.slot = slot
        self.color = color
