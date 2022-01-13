class DragData:
    def __init__(self, from_slot=None, from_position=None, index=None, color=None, x=0, y=0):
        """
        DragData is meant to hold all the necessary information for handling the dragging of widgets on the tkinter canvas's surface.
        :param from_slot: integer representing the slot from which the piece was taken
        :param from_position: integer representing the position of the piece in the initial configuration (used as an id)
        :param index: integer representing the widget index with regards to the main canvas
        :param color: string representing the color of the piece, can be Black or White
        :param x: the x coordinate of the event
        :param y: the y coordinate of the event
        """
        self.from_slot = from_slot
        self.from_position = from_position
        self.index = index
        self.color = color
        self.x = x
        self.y = y
