from slot import Slot
from piece import Piece
from drag_data import DragData


class Game:
    def __init__(self, gui):
        self.gui = gui
        self.turn = 'none'

        self.diameter = None
        self.margin = None

        self.x_left = None
        self.y_up = None
        self.x_right = None
        self.y_down = None

        self.slots = 24 * [Slot()]
        self.white_pieces = 15 * [Piece(color='white')]
        self.black_pieces = 15 * [Piece(color='black')]
        self.drag_data = DragData()

    def update_game(self, event):
        if self.turn == 'none':
            self.new_game(event.widget.winfo_width(), event.widget.winfo_height())
        else:
            self.move(event.widget.winfo_width(), event.widget.winfo_height())

    def new_game(self, width, height):
        size = self.gui.scale * min(width, height)
        self.diameter = 0.81 * size / 12
        self.margin = 0.09 * size / 24

        self.set_new_white_pieces()
        self.set_new_black_pieces()

    def place(self, piece, slot):
        position = piece.position
        color = piece.color
        self.gui.main_canvas.delete(piece.index)

        if slot.position < 12:
            y_down = self.y_down - len(slot.pieces) * self.diameter
            y_up = y_down - self.diameter

            if slot.position < 6:
                x_left = self.x_left + (2 * slot.position + 1) * self.margin + slot.position * self.diameter
            else:
                x_left = self.x_right - (2 * (11 - slot.position) + 1) * self.margin - (
                            12 - slot.position) * self.diameter
            x_right = x_left + self.diameter
        else:
            y_up = self.y_up + len(slot.pieces) * self.diameter
            y_down = y_up + self.diameter

            if slot.position < 18:
                x_left = self.x_right - (2 * (slot.position - 12) + 1) * self.margin - (
                            slot.position - 11) * self.diameter
            else:
                x_left = self.x_left + (2 * (23 - slot.position) + 1) * self.margin + (
                            23 - slot.position) * self.diameter
            x_right = x_left + self.diameter

        if color == 'white':
            self.white_pieces[position] = Piece(
                index=self.gui.main_canvas.create_oval(x_left, y_up, x_right, y_down, fill=self.gui.theme.white_fill),
                position=position, slot=slot.position, color=piece.color)
            slot.pieces.append(self.white_pieces[position])
            self.gui.main_canvas.tag_bind(self.white_pieces[position].index, '<ButtonPress-1>',
                                          lambda event, item=self.white_pieces[position]: self.drag_start(event, item))
            self.gui.main_canvas.tag_bind(self.white_pieces[position].index, '<ButtonRelease-1>', self.drag_stop)
            self.gui.main_canvas.tag_bind(self.white_pieces[position].index, '<B1-Motion>', self.drag)
        else:
            self.black_pieces[position] = Piece(
                index=self.gui.main_canvas.create_oval(x_left, y_up, x_right, y_down, fill=self.gui.theme.black_fill),
                position=position, slot=slot.position, color=piece.color)
            slot.pieces.append(self.black_pieces[position])
            self.gui.main_canvas.tag_bind(self.black_pieces[position].index, '<ButtonPress-1>',
                                          lambda event, item=self.black_pieces[position]: self.drag_start(event, item))
            self.gui.main_canvas.tag_bind(self.black_pieces[position].index, '<ButtonRelease-1>', self.drag_stop)
            self.gui.main_canvas.tag_bind(self.black_pieces[position].index, '<B1-Motion>', self.drag)

    def set_new_white_pieces(self):
        for i in range(0, 2):
            self.white_pieces[i].position = i
            self.place(self.white_pieces[i], self.slots[12])

        for i in range(2, 7):
            self.white_pieces[i].position = i
            self.place(self.white_pieces[i], self.slots[23])

        for i in range(7, 10):
            self.white_pieces[i].position = i
            self.place(self.white_pieces[i], self.slots[4])

        for i in range(10, 15):
            self.white_pieces[i].position = i
            self.place(self.white_pieces[i], self.slots[6])

    def set_new_black_pieces(self):
        for i in range(0, 2):
            self.black_pieces[i].position = i
            self.place(self.black_pieces[i], self.slots[11])

        for i in range(2, 7):
            self.black_pieces[i].position = i
            self.place(self.black_pieces[i], self.slots[0])

        for i in range(7, 10):
            self.black_pieces[i].position = i
            self.place(self.black_pieces[i], self.slots[19])

        for i in range(10, 15):
            self.black_pieces[i].position = i
            self.place(self.black_pieces[i], self.slots[17])

    def drag_start(self, event, item):
        if self.slots[item.slot].pieces[-1].position == item.position:
            self.drag_data = DragData(item.slot, item.position, item.index, item.color, event.x, event.y)
            self.slots[item.slot].pieces.remove(item)

    def drag_stop(self, event):
        if self.drag_data.from_position is not None:
            to_slot = self.position_is_valid(event)
            self.gui.main_canvas.delete(self.drag_data.index)

            if self.drag_data.color == 'white':
                if to_slot == -1:
                    self.place(self.white_pieces[self.drag_data.from_position], self.slots[self.drag_data.from_slot])
                else:
                    self.place(self.white_pieces[self.drag_data.from_position], self.slots[to_slot])
            else:
                if to_slot == -1:
                    self.place(self.black_pieces[self.drag_data.from_position], self.slots[self.drag_data.from_slot])
                else:
                    self.place(self.black_pieces[self.drag_data.from_position], self.slots[to_slot])

        self.drag_data = DragData()

    def drag(self, event):
        if self.drag_data.index is not None:
            delta_x = event.x - self.drag_data.x
            delta_y = event.y - self.drag_data.y
            self.gui.main_canvas.move(self.drag_data.index, delta_x, delta_y)
            self.drag_data.x = event.x
            self.drag_data.y = event.y

    def position_is_valid(self, event):
        for i in range(0, len(self.slots)):
            if self.is_inside(self.slots[i], event):
                return i
                # if self.move_is_valid(slot, event):
                #     self.move(slot, event)
                #     return True
                # else:
                #     return False

        return -1

    def is_inside(self, slot, event):
        if slot.position < 12:
            y_down = self.y_down
            y_up = y_down - (self.y_down - self.y_up) / 2

            if slot.position < 6:
                x_left = self.x_left + slot.position * self.gui.triangle_width
            else:
                x_left = self.x_right - (12 - slot.position) * self.gui.triangle_width
            x_right = x_left + self.gui.triangle_width
        else:
            y_up = self.y_up
            y_down = y_up + (self.y_down - self.y_up) / 2

            if slot.position < 18:
                x_left = self.x_right - (slot.position - 11) * self.gui.triangle_width
            else:
                x_left = self.x_left + (23 - slot.position) * self.gui.triangle_width
            x_right = x_left + self.gui.triangle_width

        if x_left <= event.x <= x_right and y_up <= event.y <= y_down:
            return True
        return False

    def move(self, slot, event):
        pass
