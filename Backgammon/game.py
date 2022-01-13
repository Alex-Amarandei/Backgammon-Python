import secrets

from slot import Slot
from piece import Piece
from status import Status
from drag_data import DragData
from PIL import Image, ImageTk
from ui_button import UIButton


class Game:
    def __init__(self, gui):
        self.gui = gui
        self.turn = 'none_1'
        self.status = None
        self.width = None
        self.height = None

        self.turn_index = None
        self.status_index = None

        self.diameter = None
        self.margin = None

        self.x_left = None
        self.y_up = None
        self.x_right = None
        self.y_down = None

        self.slots = 24 * [Slot()]
        self.white_pieces = 15 * [Piece(color='White')]
        self.black_pieces = 15 * [Piece(color='Black')]
        self.drag_data = DragData()

        self.roll_button = UIButton()
        self.dice_1 = UIButton()
        self.dice_2 = UIButton()
        self.player_1 = []
        self.player_2 = []

        self.moves = []
        self.white_jail = []
        self.black_jail = []

    def update_game(self, event):
        self.diameter = 0.81 * self.gui.size / 12
        self.margin = 0.09 * self.gui.size / 24
        self.width = event.widget.winfo_width()
        self.height = event.widget.winfo_height()

        if self.turn == 'none_1':
            self.new_game()
            self.gui.root.resizable(False, False)

    def new_game(self):
        self.status = Status.ROLL
        self.update_player()
        self.update_status()
        self.draw_roll_button()
        self.update_dice(1, 1)

        self.set_new_slots()

    def update_player(self):
        if self.turn == 'none_1':
            turn = 'White'
        elif self.turn == 'none_2':
            turn = 'Black'
        else:
            turn = self.turn
        self.gui.main_canvas.delete(self.turn_index)

        font = 'Century ' + str(int(min(self.width / 32, self.height / 12))) + ' bold'
        self.turn_index = self.gui.main_canvas.create_text(self.width - (self.width - self.gui.size) / 4,
                                                           self.height / 2 - 0.05 * self.height,
                                                           fill=self.gui.theme.font_color,
                                                           font=font,
                                                           text=turn)

    def update_status(self):
        self.gui.main_canvas.delete(self.status_index)
        font = 'Century ' + str(int(min(self.width / 32, self.height / 12))) + ' bold'
        self.status_index = self.gui.main_canvas.create_text(self.width - (self.width - self.gui.size) / 4,
                                                             self.height / 2 + 0.05 * self.height,
                                                             fill=self.gui.theme.font_color,
                                                             font=font,
                                                             text=self.status.value)

    def draw_roll_button(self):
        self.roll_button.image = ImageTk.PhotoImage(
            Image.open(self.gui.theme.roll_path).resize((int((self.width - self.gui.size) / 4), int(self.height * 0.15)), Image.ANTIALIAS))
        self.roll_button.index = self.gui.main_canvas.create_image((self.width - self.gui.size) / 4,
                                                                   self.height / 2 + 0.15 * self.height,
                                                                   image=self.roll_button.image)

        self.gui.main_canvas.tag_bind(self.roll_button.index, '<Button-1>', self.roll)

    def update_dice(self, first, second):
        self.dice_1.image = ImageTk.PhotoImage(
            Image.open(self.choose_dice_image(first)).resize((int(self.height * 0.12), int(self.height * 0.12)), Image.ANTIALIAS))
        self.dice_1.index = self.gui.main_canvas.create_image((self.width - self.gui.size) / 6,
                                                              self.height / 2 - 0.15 * self.height,
                                                              image=self.dice_1.image)

        self.dice_2.image = ImageTk.PhotoImage(
            Image.open(self.choose_dice_image(second)).resize((int(self.height * 0.12), int(self.height * 0.12)), Image.ANTIALIAS))
        self.dice_2.index = self.gui.main_canvas.create_image((self.width - self.gui.size) / 6 + int(self.height * 0.18),
                                                              self.height / 2 - 0.15 * self.height,
                                                              image=self.dice_2.image)

    def choose_dice_image(self, number):
        if number == 1:
            return self.gui.theme.dice_1_path
        elif number == 2:
            return self.gui.theme.dice_2_path
        elif number == 3:
            return self.gui.theme.dice_3_path
        elif number == 4:
            return self.gui.theme.dice_4_path
        elif number == 5:
            return self.gui.theme.dice_5_path
        return self.gui.theme.dice_6_path

    def set_new_slots(self):
        for i in range(2, 7):
            self.black_pieces[i].position = i
            self.place(self.black_pieces[i], self.slots[0])

        for i in range(7, 10):
            self.white_pieces[i].position = i
            self.place(self.white_pieces[i], self.slots[4])

        for i in range(10, 15):
            self.white_pieces[i].position = i
            self.place(self.white_pieces[i], self.slots[6])

        for i in range(0, 2):
            self.black_pieces[i].position = i
            self.place(self.black_pieces[i], self.slots[11])

        for i in range(0, 2):
            self.white_pieces[i].position = i
            self.place(self.white_pieces[i], self.slots[12])

        for i in range(10, 15):
            self.black_pieces[i].position = i
            self.place(self.black_pieces[i], self.slots[17])

        for i in range(7, 10):
            self.black_pieces[i].position = i
            self.place(self.black_pieces[i], self.slots[19])

        for i in range(2, 7):
            self.white_pieces[i].position = i
            self.place(self.white_pieces[i], self.slots[23])

    def update_pieces(self):
        for slot in self.slots:
            for piece in slot.pieces:
                self.place(piece, slot)

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

        if color == 'White':
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

    def drag_start(self, event, item):
        if self.slots[item.slot].pieces[-1].position == item.position \
                and self.status == Status.MOVE\
                and self.turn == item.color:
            self.drag_data = DragData(item.slot, item.position, item.index, item.color, event.x, event.y)
            self.slots[item.slot].pieces.remove(item)

    def drag_stop(self, event):
        if self.drag_data.from_position is not None:
            to_slot = self.position_is_valid(event)
            self.gui.main_canvas.delete(self.drag_data.index)

            if self.drag_data.color == 'White':
                if to_slot == -1:
                    self.place(self.white_pieces[self.drag_data.from_position], self.slots[self.drag_data.from_slot])
                else:
                    self.place(self.white_pieces[self.drag_data.from_position], self.slots[to_slot])
            else:
                if to_slot == -1:
                    self.place(self.black_pieces[self.drag_data.from_position], self.slots[self.drag_data.from_slot])
                else:
                    self.place(self.black_pieces[self.drag_data.from_position], self.slots[to_slot])

        if len(self.moves) == 0:
            self.turn = change_turn(self.turn)
            self.update_player()

            self.status = Status.ROLL
            self.update_status()

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
                if self.move_is_valid(self.slots[i]):
                    return i
                else:
                    return -1

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

    def roll(self, event):
        if self.turn == 'none_1':
            self.choice_roll(1)
        elif self.turn == 'none_2':
            self.choice_roll(2)
        else:
            if self.status == Status.ROLL:
                first = secrets.choice(range(1, 7))
                second = secrets.choice(range(1, 7))
                print(first, second)

                if first == second:
                    self.moves = 4 * [first]
                else:
                    self.moves = [first, second]

                print(self.moves)

                self.status = Status.MOVE
                self.update_status()
                self.update_dice(first, second)

    def choice_roll(self, player):
        if player == 1:
            self.player_1 = [secrets.choice(range(1, 7)), secrets.choice(range(1, 7))]
            print(self.player_1[0], self.player_1[1])
            self.turn = 'none_2'
            self.update_player()
            self.update_dice(self.player_1[0], self.player_1[1])
        else:
            self.player_2 = [secrets.choice(range(1, 7)), secrets.choice(range(1, 7))]
            print('before')
            print(self.player_1[0], self.player_1[1])
            print(self.player_2[0], self.player_2[1])
            self.update_dice(self.player_2[0], self.player_2[1])

            if self.player_1[0] == self.player_1[1]:
                if self.player_2[0] == self.player_2[1]:
                    if self.player_1[0] >= self.player_2[0]:
                        self.turn = 'White'
                    else:
                        self.turn = 'Black'
                else:
                    self.turn = 'White'
            else:
                if self.player_2[0] == self.player_2[1]:
                    self.turn = 'Black'
                elif self.player_1[0] + self.player_1[1] >= self.player_2[0] + self.player_2[1]:
                    self.turn = 'White'
                else:
                    self.turn = 'Black'

            print(self.player_1[0], self.player_1[1])
            print(self.player_2[0], self.player_2[1])
            self.update_player()

    def move_is_valid(self, to_slot):
        difference = to_slot.position - self.drag_data.from_slot

        q_from = get_quadrant(self.drag_data.from_slot)
        q_to = get_quadrant(to_slot.position)

        if self.turn == 'White':
            if q_from == 1:
                if 1 <= q_to <= 2:
                    if difference > 0 and difference in self.moves:
                        return self.stack_is_valid(to_slot, difference)
                    return False
                return False
            elif q_from == 2:
                if q_to == 2 and difference > 0 and difference in self.moves:
                    return self.stack_is_valid(to_slot, difference)
                return False
            elif q_from == 3:
                if 3 <= q_to <= 4:
                    if difference > 0 and difference in self.moves:
                        return self.stack_is_valid(to_slot, difference)
                return False
            elif q_from == 4:
                if q_to == 4:
                    if difference > 0 and difference in self.moves:
                        return self.stack_is_valid(to_slot, difference)
                    return False
                elif q_to == 1:
                    difference = to_slot.position + 24 - self.drag_data.from_slot
                    if difference > 0 and difference in self.moves:
                        return self.stack_is_valid(to_slot, difference)
                    return False
                return False
        else:
            if q_from == 1:
                if q_to == 1:
                    if difference < 0 and abs(difference) in self.moves:
                        return self.stack_is_valid(to_slot, abs(difference))
                    return False
                elif q_to == 4:
                    difference = self.drag_data.from_slot + 24 - to_slot.position
                    if difference > 0 and difference in self.moves:
                        return self.stack_is_valid(to_slot, difference)
                return False
            elif q_from == 2:
                if 1 <= q_to <= 2:
                    if difference < 0:
                        if abs(difference) in self.moves:
                            return self.stack_is_valid(to_slot, abs(difference))
                        return False
                    return False
                return False
            elif q_from == 3:
                if q_to == 3:
                    if difference < 0:
                        if abs(difference) in self.moves:
                            return self.stack_is_valid(to_slot, abs(difference))
                        return False
                    return False
                return False
            elif q_from == 4:
                if 3 <= q_to <= 4:
                    if difference < 0 and abs(difference) in self.moves:
                        return self.stack_is_valid(to_slot, abs(difference))
                    return False
                return False

        return False

    def stack_is_valid(self, to_slot, difference):
        if len(to_slot.pieces) == 0:
            self.moves.remove(difference)
            return True
        elif to_slot.pieces[-1].color == self.turn:
            self.moves.remove(difference)
            return True
        elif len(to_slot.pieces) == 1:
            self.moves.remove(difference)
            self.capture(to_slot)
            return True
        return False

    def capture(self, to_slot):
        piece_position = to_slot.pieces[-1].position

        if self.turn == 'White':
            self.gui.main_canvas.delete(self.black_pieces[piece_position].index)

            self.black_pieces[piece_position] = Piece(
                    index=self.gui.main_canvas.create_oval(
                        self.width / 2 - 0.025 * self.gui.size - 2 * self.margin,
                        self.y_up + len(self.black_jail) * self.diameter,
                        self.width / 2 - 0.025 * self.gui.size + self.diameter - 2 * self.margin,
                        self.y_up + (len(self.black_jail) + 1) * self.diameter,
                        fill=self.gui.theme.black_fill),
                    position=piece_position, slot=-1, color='Black')

            self.gui.main_canvas.tag_bind(self.black_pieces[piece_position].index, '<ButtonPress-1>',
                                          lambda event, item=self.black_pieces[piece_position]: self.drag_start(event, item))
            self.gui.main_canvas.tag_bind(self.black_pieces[piece_position].index, '<ButtonRelease-1>', self.drag_stop)
            self.gui.main_canvas.tag_bind(self.black_pieces[piece_position].index, '<B1-Motion>', self.drag)
            self.black_jail.append(self.black_pieces[piece_position])
        else:
            self.gui.main_canvas.delete(self.white_pieces[piece_position].index)

            self.white_pieces[piece_position] = Piece(
                    index=self.gui.main_canvas.create_oval(
                        self.width / 2 - 0.025 * self.gui.size - 2 * self.margin,
                        self.y_down - (len(self.black_jail) + 1) * self.diameter,
                        self.width / 2 - 0.025 * self.gui.size + self.diameter - 2 * self.margin,
                        self.y_down - len(self.black_jail) * self.diameter,
                        fill=self.gui.theme.white_fill),
                    position=piece_position, slot=-1, color='White')

            self.gui.main_canvas.tag_bind(self.white_pieces[piece_position].index, '<ButtonPress-1>',
                                          lambda event, item=self.black_pieces[piece_position]: self.drag_start(event, item))
            self.gui.main_canvas.tag_bind(self.white_pieces[piece_position].index, '<ButtonRelease-1>', self.drag_stop)
            self.gui.main_canvas.tag_bind(self.white_pieces[piece_position].index, '<B1-Motion>', self.drag)
            self.black_jail.append(self.white_pieces[piece_position])

        to_slot.pieces.pop(-1)


def get_quadrant(number):
    if 0 <= number <= 5:
        return 1
    elif 6 <= number <= 11:
        return 2
    elif 12 <= number <= 17:
        return 3
    elif 18 <= number <= 23:
        return 4


def change_turn(current):
    if current == 'White':
        return 'Black'
    return 'White'
