import secrets

from slot import Slot
from piece import Piece
from status import Status
from drag_data import DragData
from PIL import Image, ImageTk
from ui_button import UIButton
from game_modes import GameMode


class Game:
    def __init__(self, gui):
        """
        Is meant to hold all necessary information for game and UI logic and is also used for fetching different data and values from other files that it is linked to.
        :param gui: a reference to the GUI instance containing the root and main canvas of tkinter
        """
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

        self.slots = 26 * [Slot()]
        self.white_pieces = 15 * [Piece(color='White')]
        self.black_pieces = 15 * [Piece(color='Black')]
        self.drag_data = DragData()

        self.roll_button = UIButton()
        self.dice_1 = UIButton()
        self.dice_2 = UIButton()
        self.player_1 = []
        self.player_2 = []

        self.moves = []
        self.jail = {'White': [], 'Black': []}

    def update_game(self, event):
        """
        Initialises the game with its default values.
        :param event: widget representing the event which triggered this function's call (mainly used for getting the window's size)
        """
        self.diameter = 0.81 * self.gui.size / 12
        self.margin = 0.09 * self.gui.size / 24
        self.width = event.widget.winfo_width()
        self.height = event.widget.winfo_height()

        if self.turn == 'none_1':
            self.new_game()
            self.gui.root.resizable(False, False)

    def new_game(self):
        """
        Initialises the game data with their respective default values.
        """
        self.status = Status.ROLL
        self.update_player()
        self.update_status()
        self.draw_roll_button()
        self.update_dice(1, 1)

        self.set_new_slots()

    def update_player(self):
        """
        Updates the player text on the right of the screen according to which of the two's turn it is.
        """
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
        """
        Updates the status below the player with values such as Move and Roll in order to suggest to the human player what kind of action he is required to take now.
        """
        self.gui.main_canvas.delete(self.status_index)
        font = 'Century ' + str(int(min(self.width / 32, self.height / 12))) + ' bold'
        self.status_index = self.gui.main_canvas.create_text(self.width - (self.width - self.gui.size) / 4,
                                                             self.height / 2 + 0.05 * self.height,
                                                             fill=self.gui.theme.font_color,
                                                             font=font,
                                                             text=self.status.value)

    def draw_roll_button(self):
        """
        This function is only called once and its role is to display the Roll button underneath the dices on the left of the screen.
        """
        self.roll_button.image = ImageTk.PhotoImage(
            Image.open(self.gui.theme.roll_path).resize(
                (int((self.width - self.gui.size) / 4), int(self.height * 0.15)), Image.ANTIALIAS))
        self.roll_button.index = self.gui.main_canvas.create_image((self.width - self.gui.size) / 4,
                                                                   self.height / 2 + 0.15 * self.height,
                                                                   image=self.roll_button.image)

        self.gui.main_canvas.tag_bind(self.roll_button.index, '<Button-1>', lambda event: self.roll())

    def update_dice(self, first, second):
        """
        Updates the images representing the dices according to the values which where randomly picked during the rolling phase.
        :param first: integer representing the value of the first die
        :param second: integer representing the value of the second die
        """
        self.dice_1.image = ImageTk.PhotoImage(
            Image.open(self.choose_dice_image(first)).resize((int(self.height * 0.12), int(self.height * 0.12)),
                                                             Image.ANTIALIAS))
        self.dice_1.index = self.gui.main_canvas.create_image((self.width - self.gui.size) / 6,
                                                              self.height / 2 - 0.15 * self.height,
                                                              image=self.dice_1.image)

        self.dice_2.image = ImageTk.PhotoImage(
            Image.open(self.choose_dice_image(second)).resize((int(self.height * 0.12), int(self.height * 0.12)),
                                                              Image.ANTIALIAS))
        self.dice_2.index = self.gui.main_canvas.create_image(
            (self.width - self.gui.size) / 6 + int(self.height * 0.18),
            self.height / 2 - 0.15 * self.height,
            image=self.dice_2.image)

        if self.status == Status.MOVE and self.turn == 'Black':
            self.computer_move()

    def choose_dice_image(self, number):
        """
        A utility function which helps pick the right path to the image corresponding to each of the values on the die.
        :param number: integer representing the value on the die
        :return: string representing the path to the image requested
        """
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
        """
        Sets the initial layout of the board, with the slots (triangles) and pieces.
        """
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

    def drag_start(self, event, item):
        """
        A function called at the start of the dragging action of a piece.
        :param event: event which triggered the function, used for getting the x and y coordinates of the cursor
        :param item: the piece to be dragged around
        """
        if self.slots[item.slot].pieces[-1].position == item.position \
                and self.status == Status.MOVE \
                and self.turn == item.color:
            if (len(self.jail[self.turn]) > 0 and self.jail[self.turn][-1].position == item.position) \
                    or len(self.jail[self.turn]) == 0:
                self.drag_data = DragData(item.slot, item.position, item.index, item.color, event.x, event.y)
                self.slots[item.slot].pieces.remove(item)

    def drag_stop(self, event):
        """
        A function called at the end of the dragging action of a piece which validates if the current position is suitable or the action will be reverted.
        :param event: event which triggered the function, used for getting the x and y coordinates of the cursor
        """
        if self.drag_data.from_position is not None:
            to_slot = self.position_is_valid(event)

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
        """
        A function called during the dragging action of a piece which moves it around according to the data in the DragData object.
        :param event: the event of dragging, necessary for getting the x and y coordinates of the cursor
        """
        if self.drag_data.index is not None:
            delta_x = event.x - self.drag_data.x
            delta_y = event.y - self.drag_data.y
            self.gui.main_canvas.move(self.drag_data.index, delta_x, delta_y)
            self.drag_data.x = event.x
            self.drag_data.y = event.y

    def is_inside(self, slot, event):
        """
        Utility function to check if a piece is inside the domain or territory of a certain slot so that it can be snapped-in-place.
        :param slot: slot to be checked for the aforementioned reasons
        :param event: widget necessary for getting the x and y coordinates of the cursor
        :return: True is the piece has its center in the boundaries of the slot and False, otherwise
        """
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

    def choice_roll(self, player):
        """
        The first roll of the game for deciding which player moves first.
        :param player: integer representing the player which is at turn
        """
        if player == 1:
            self.player_1 = [secrets.choice(range(1, 7)), secrets.choice(range(1, 7))]
            self.turn = 'none_2'
            self.update_player()
            self.update_dice(self.player_1[0], self.player_1[1])
        else:
            self.player_2 = [secrets.choice(range(1, 7)), secrets.choice(range(1, 7))]
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

            self.update_player()

    def roll(self):
        """
        Function used by all players to access the dice-rolling logic.
        """
        if self.turn == 'none_1':
            self.choice_roll(1)
        elif self.turn == 'none_2':
            self.choice_roll(2)
        else:
            if self.status == Status.ROLL:
                first = secrets.choice(range(1, 7))
                second = secrets.choice(range(1, 7))

                if first == second:
                    self.moves = 4 * [first]
                else:
                    self.moves = [first, second]
                # self.eliminate_impossible_moves()

                self.status = Status.MOVE
                self.update_status()
                self.update_dice(first, second)

    def position_is_valid(self, event):
        """
        utility function to check if the position in which a piece was left is legal.
        :param event: widget used for getting the x and y coordinates of the cursor
        :return: the slot's position on the board if the position is valid and -1 otherwise
        """
        if self.turn == 'White' and len(self.jail['White']) > 0:
            for i in range(12, 18):
                if self.is_inside(self.slots[i], event):
                    if self.bail_is_valid(self.slots[i]):
                        return i
                    else:
                        return -1
        elif self.turn == 'Black' and len(self.jail['Black']) > 0:
            for i in range(6, 12):
                if self.is_inside(self.slots[i], event):
                    if self.bail_is_valid(self.slots[i]):
                        return i
                    else:
                        return -1
        else:
            for i in range(0, len(self.slots)):
                if self.is_inside(self.slots[i], event):
                    if self.move_is_valid(self.slots[i]):
                        return i
                    else:
                        return -1

        return -1

    def move_is_valid(self, to_slot):
        """
        Utility function used to check if the rules of the game are respected with the currently on-going move.
        :param to_slot: the slot to which the piece is intended to be moved
        :return: true is it is a valid move and False otherwise
        """
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

    def bail_is_valid(self, slot):
        """
        Utility function to check if a bail out of the jail has been done in a legal way.
        :param slot: the slot intended for the piece
        :return: True if the move was valid and False otherwise
        """
        if self.turn == 'White':
            if 12 <= slot.position <= 17:
                for i in range(12, 18):
                    if slot.position == i and (i - 11) in self.moves:
                        if self.stack_is_valid(slot, i - 11):
                            self.jail['White'].remove(self.white_pieces[self.drag_data.from_position])
                            return True
                        return False
                return False
            return False
        else:
            if 6 <= slot.position <= 11:
                for i in range(6, 12):
                    if slot.position == i and (12 - i) in self.moves:
                        if self.stack_is_valid(slot, 12 - i):
                            self.jail['Black'].remove(self.black_pieces[self.drag_data.from_position])
                            return True
                        return False
                return False
            return False

    def stack_is_valid(self, to_slot, difference, test=False):
        """
        Utility function to check if the stack on which a piece is meant to be positioned would allow for a legal move.
        :param to_slot: the slot intended for the piece
        :param difference: the difference between the initial and final positions of the piece, a move, essentially
        :param test: if the move is to actually committed or just verified
        :return: True if the move was valid and False otherwise
        """
        if len(to_slot.pieces) == 0:
            if not test:
                if difference in self.moves:
                    self.moves.remove(difference)
            return True
        elif to_slot.pieces[-1].color == self.turn:
            if not test:
                if difference in self.moves:
                    self.moves.remove(difference)
            return True
        elif len(to_slot.pieces) == 1:
            if not test:
                if difference in self.moves:
                    self.moves.remove(difference)
                    self.capture(to_slot)
            return True
        return False

    def place(self, piece, slot):
        """
        Places the piece on the selected position.
        :param piece: The piece to be moved.
        :param slot: The slot to which the piece is intended to be moved.
        """
        if 24 <= slot.position <= 25:
            self.capture(slot, False)

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

    def capture(self, to_slot, popping=True):
        """
        Logic for capturing an enemy piece.
        :param to_slot: The slot on which the enemy piece resides.
        :param popping: If the piece taken is to be eliminated from the corresponding slot or it is just a verification.
        """
        test_1 = 'White'

        if not popping:
            test_1 = 'Black'

        piece_position = to_slot.pieces[-1].position

        if self.turn == test_1:
            self.gui.main_canvas.delete(self.black_pieces[piece_position].index)

            self.black_pieces[piece_position] = Piece(
                index=self.gui.main_canvas.create_oval(
                    self.width / 2 - 0.025 * self.gui.size - 2 * self.margin,
                    self.y_up + len(self.jail['Black']) * self.diameter,
                    self.width / 2 - 0.025 * self.gui.size + self.diameter - 2 * self.margin,
                    self.y_up + (len(self.jail['Black']) + 1) * self.diameter,
                    fill=self.gui.theme.black_fill),
                position=piece_position, slot=24, color='Black')

            self.gui.main_canvas.tag_bind(self.black_pieces[piece_position].index, '<ButtonPress-1>',
                                          lambda event, item=self.black_pieces[piece_position]: self.drag_start(event,
                                                                                                                item))
            self.gui.main_canvas.tag_bind(self.black_pieces[piece_position].index, '<ButtonRelease-1>', self.drag_stop)
            self.gui.main_canvas.tag_bind(self.black_pieces[piece_position].index, '<B1-Motion>', self.drag)
            self.jail['Black'].append(self.black_pieces[piece_position])
            self.slots[24].pieces.append(self.black_pieces[piece_position])
        else:
            self.gui.main_canvas.delete(self.white_pieces[piece_position].index)

            self.white_pieces[piece_position] = Piece(
                index=self.gui.main_canvas.create_oval(
                    self.width / 2 - 0.025 * self.gui.size - 2 * self.margin,
                    self.y_down - (len(self.jail['White']) + 1) * self.diameter,
                    self.width / 2 - 0.025 * self.gui.size + self.diameter - 2 * self.margin,
                    self.y_down - len(self.jail['White']) * self.diameter,
                    fill=self.gui.theme.white_fill),
                position=piece_position, slot=25, color='White')

            self.gui.main_canvas.tag_bind(self.white_pieces[piece_position].index, '<ButtonPress-1>',
                                          lambda event, item=self.white_pieces[piece_position]: self.drag_start(event,
                                                                                                                item))
            self.gui.main_canvas.tag_bind(self.white_pieces[piece_position].index, '<ButtonRelease-1>', self.drag_stop)
            self.gui.main_canvas.tag_bind(self.white_pieces[piece_position].index, '<B1-Motion>', self.drag)
            self.jail['White'].append(self.white_pieces[piece_position])
            self.slots[25].pieces.append(self.white_pieces[piece_position])

        if popping:
            to_slot.pieces.pop(-1)

    def eliminate_impossible_moves(self):
        """
        Eliminates moves that cannot be done due to illegality.
        """
        if self.turn == 'White':
            for j in range(0, len(self.moves)):
                is_possible = False
                for i in range(0, len(self.white_pieces)):
                    if self.check_move(self.white_pieces[i], self.moves[j]) != -1:
                        is_possible = True
                if not is_possible:
                    self.moves.pop(j)
        else:
            for j in range(0, len(self.moves)):
                is_possible = False
                for i in range(0, len(self.black_pieces)):
                    if self.check_move(self.black_pieces[i], self.moves[j]) != -1:
                        is_possible = True
                if not is_possible:
                    self.moves.pop(j)

    def check_move(self, piece, distance, test=False):
        """
        Verifies if a move would be valid.
        :param piece: The piece to be moved.
        :param distance: The distance to be crossed.
        :param test: If the move is to be committed or just verified.
        :return: -1 if not valid or the distance to be crossed if yes
        """
        q_from = get_quadrant(piece.slot)

        if self.turn == 'White':
            if q_from == 1 or q_from == 3:
                if self.stack_is_valid(self.slots[piece.slot + distance], distance, test):
                    return piece.slot + distance
            elif q_from == 2:
                if piece.slot + distance < 12 and \
                        self.stack_is_valid(self.slots[piece.slot + distance], distance, test):
                    return piece.slot + distance
            elif q_from == 4:
                if self.stack_is_valid(self.slots[(piece.slot + distance) % 24], distance, test):
                    return (piece.slot + distance) % 24
            return -1
        else:
            if q_from == 1:
                if self.stack_is_valid(self.slots[piece.slot - distance + 24], distance, test):
                    return piece.slot - distance + 24
            elif q_from == 2 or q_from == 4:
                if self.stack_is_valid(self.slots[piece.slot - distance], distance, test):
                    return piece.slot - distance
            elif q_from == 3:
                if piece.slot - distance > 11 and \
                        self.stack_is_valid(self.slots[piece.slot - distance], distance, test):
                    return piece.slot - distance
            return -1

    def computer_move(self):
        """
        Function to simulate the computer's movements, depending on its selected level of difficulty.
        """
        if self.gui.game_mode == GameMode.EASY:
            while len(self.moves) > 0:
                move = secrets.choice(self.moves)
                ascending = secrets.choice(range(0, 2))

                if ascending == 1:
                    for i in range(0, len(self.black_pieces)):
                        answer = self.check_move(self.black_pieces[i], move)
                        if answer != -1 and self.slots[self.black_pieces[i].slot].pieces[-1] == self.black_pieces[i]:
                            self.place(self.black_pieces[i], self.slots[answer])
                            break
                else:
                    for i in range(len(self.black_pieces) - 1, -1, -1):
                        answer = self.check_move(self.black_pieces[i], move)
                        if answer != -1 and self.slots[self.black_pieces[i].slot].pieces[-1] == self.black_pieces[i]:
                            self.place(self.black_pieces[i], self.slots[answer])
                            break
        elif self.gui.game_mode == GameMode.MEDIUM:
            answers = []
            for j in range(0, len(self.moves)):
                for i in range(0, len(self.black_pieces)):
                    answer = self.check_move(self.black_pieces[i], self.moves[j], True)
                    if answer != -1 and self.slots[self.black_pieces[i].slot].pieces[-1] == self.black_pieces[i]:
                        answers.append([i, j])

            answers.sort(reverse=True)

            for i in range(0, len(self.moves)):
                answer = self.check_move(self.black_pieces[answers[i][0]], self.moves[answers[i][1]])
                self.place(self.black_pieces[answers[i][0]], self.slots[answer])
        elif self.gui.game_mode == GameMode.HARD:
            pass

        self.turn = change_turn(self.turn)
        self.update_player()

        self.status = Status.ROLL
        self.update_status()


def get_quadrant(number):
    """
    Gets the quadrant of the board in which a slot resides.
    :param number: the slot's position on the board
    :return: the quadrant number, 1 for bottom-left, 2 for bottom-right, 3 for upper-right, 4 for upper-left
    """
    if 0 <= number <= 5:
        return 1
    elif 6 <= number <= 11:
        return 2
    elif 12 <= number <= 17:
        return 3
    elif 18 <= number <= 23:
        return 4


def change_turn(current):
    """
    Changes the player currently at turn
    :param current: The player that is now at turn
    :return: The other player's color
    """
    if current == 'White':
        return 'Black'
    return 'White'
