import tkinter as tk

from game import *
from menus import Menu
from copy import deepcopy
from player import Player
from PIL import Image, ImageTk
from ui_button import UIButton
from game_modes import GameMode


class GUI:
    def __init__(self, root, theme):
        """
        Initialises the main object holding all the information regarding the GUI and UI/UX up until the Game menu, which is separate.
        :param root: the root of tkinter
        :param theme: the theme of the user's OS
        """
        self.root = root
        self.theme = theme
        self.scale = 0.8
        self.size = None

        self.game = Game(self)
        self.game_mode = GameMode.VS
        self.current_menu = Menu.MAIN_MENU

        self.background_image = ImageTk.PhotoImage(file=self.theme.background_image_path)
        self.screen = {'width': self.root.winfo_screenwidth(), 'height': self.root.winfo_screenheight()}
        self.main_canvas = tk.Canvas(self.root, width=self.screen['width'], height=self.screen['height'], cursor='circle')
        self.main_canvas.create_image(0, 0, image=self.background_image, anchor='nw')

        self.game_title = None
        self.player_buttons = [UIButton(), UIButton()]
        self.difficulty_buttons = [UIButton(), UIButton(), UIButton()]

        self.player1 = Player()
        self.player2 = Player()

        self.player1_input = None
        self.player2_input = None
        self.player1_field = None
        self.player2_field = None
        self.confirm_button = UIButton()

        self.border = None
        self.board = None
        self.separator = None
        self.triangles = 24 * [None]
        self.triangle_width = None

        self.main_canvas.pack(fill='both', expand=True)
        self.main_canvas.bind('<Configure>', self.update)

    def update(self, event):
        """
        A centralised function for updating the UI depending on the actions occurring on the screen.
        :param event: the event triggering the update, used for getting the x and y coordinates
        """
        self.clean()

        if self.current_menu == Menu.MAIN_MENU:
            self.update_main_menu(event)
        elif self.current_menu == Menu.DIFFICULTY_MENU:
            self.update_difficulty_menu(event)
        elif self.current_menu == Menu.GAME_MENU:
            self.update_game_menu(event)
        elif self.current_menu == Menu.NAME_MENU:
            self.update_name_menu(event)

    def clean(self):
        """
        Cleans the entire UI, but redraws the background gradient..
        """
        self.main_canvas.delete('all')
        self.main_canvas.create_image(0, 0, image=self.background_image, anchor='nw')

    def update_main_menu(self, event):
        """
        Updates the Title and Player buttons to be resized according to the window.
        :param event: widget used for getting the current width and height of the screen
        """
        self.update_title(event.widget.winfo_width(), event.widget.winfo_height())
        self.update_player_buttons(event.widget.winfo_width(), event.widget.winfo_height())

    def update_difficulty_menu(self, event):
        """
        Updates the difficulty menu with its corresponding title and buttons in order to fit the new sizes.
        :param event: widget used for getting the current width and height of the screen
        """
        self.update_title(event.widget.winfo_width(), event.widget.winfo_height())
        self.update_difficulty_buttons(event.widget.winfo_width(), event.widget.winfo_height())

    def update_game_menu(self, event):
        """
        Creates the board and calls the corresponding function in the Game menu.
        :param event: widget used for getting the current width and height of the screen
        """
        self.update_board(event.widget.winfo_width(), event.widget.winfo_height())
        self.game.update_game(event)

    def update_name_menu(self, event):
        """
        Updates the newly added name menu for users to type their names.
        :param event: widget used for getting the width and height of the current window
        """
        self.update_title(event.widget.winfo_width(), event.widget.winfo_height(),
                          'Let\'s get to know each other!')
        self.update_player_fields(event.widget.winfo_width(), event.widget.winfo_height())
        self.update_confirm_button(event.widget.winfo_width(), event.widget.winfo_height())

    def update_player_fields(self, width, height):
        """
            Updates the newly added fields for users to type their names in order to have them displayed whilst playing.
            :param width: the width of the current window
            :param height: the height of the current window
        """
        scale = int(0.04 * width)
        self.player1_input = tk.Entry(self.root, font=('Helvetica', scale),
                                      width=int(width/scale),
                                      fg='#336d92', bd=0)
        self.player1_input.insert(2, 'Player 1 Name')

        self.player2_input = tk.Entry(self.root, font=('Helvetica', scale),
                                      width=int(width/scale),
                                      fg='#336d92', bd=0)
        self.player2_input.insert(2, 'Player 2 Name')

        self.player1_field = self.main_canvas.create_window(width / 2,
                                                            2 * height / 5,
                                                            anchor='center',
                                                            window=self.player1_input)
        self.player2_field = self.main_canvas.create_window(width / 2,
                                                            3 * height / 5,
                                                            anchor='center',
                                                            window=self.player2_input)

    def update_confirm_button(self, width, height):
        """
        Resizes the aspect of the confirm button that adds the names of the players to stored data.
        :param width:  the width of the current window
        :param height: the height of the current window
        """
        self.confirm_button.image = ImageTk.PhotoImage(
            Image.open(self.theme.confirm_button_path).resize((int(width / 2), int(height / 7)), Image.ANTIALIAS))

        self.confirm_button.index = self.main_canvas.create_image(width / 2,
                                                                  6 * height / 7,
                                                                  image=self.confirm_button.image)

        self.main_canvas.tag_bind(self.confirm_button.index, '<Button-1>', self.confirm)

    def confirm(self, event):
        """
        Adds the collected data from the input fields into storage for later use.
        :param event: widget used for getting the width and height of the current window
        """
        self.player1 = Player(self.player1_input.get(), 'White')
        self.player2 = Player(self.player2_input.get(), 'Black')
        self.current_menu = Menu.GAME_MENU
        self.update(event)

    def update_title(self, width, height, text='Backgammon'):
        """
        Updates the title to fit the new sizes.
        :param text: the text to be shown on the upper part of the screen
        :param width: the width of the window
        :param height: the height of the window
        """
        font = 'Century ' + str(int(min(width / 16, height / 6))) + ' bold'
        self.game_title = self.main_canvas.create_text(width / 2,
                                                       height / 6,
                                                       fill=self.theme.font_color,
                                                       font=font,
                                                       text=text)

    def update_player_buttons(self, width, height):
        """
        Resizes the player buttons to fit the window size.
        :param width: the width of the window
        :param height: the height of the window
        """
        self.player_buttons[0].image = ImageTk.PhotoImage(
            Image.open(self.theme.single_button_path).resize((int(width / 2), int(height / 7)), Image.ANTIALIAS))
        self.player_buttons[1].image = ImageTk.PhotoImage(
            Image.open(self.theme.two_button_path).resize((int(width / 2), int(height / 7)), Image.ANTIALIAS))

        self.player_buttons[0].index = self.main_canvas.create_image(width / 2,
                                                                     3 * height / 7,
                                                                     image=self.player_buttons[0].image)
        self.player_buttons[1].index = self.main_canvas.create_image(width / 2,
                                                                     5 * height / 7,
                                                                     image=self.player_buttons[1].image)

        self.main_canvas.tag_bind(self.player_buttons[0].index, '<Button-1>', self.play_single)
        self.main_canvas.tag_bind(self.player_buttons[1].index, '<Button-1>', self.play_two)

    def update_difficulty_buttons(self, width, height):
        """
        Resizes the difficulty buttons to fit the window size.
        :param width: the width of the window
        :param height: the height of the window
        """
        self.difficulty_buttons[0].image = ImageTk.PhotoImage(
            Image.open(self.theme.easy_button_path).resize((int(width / 6), int(2 * height / 7)), Image.ANTIALIAS))
        self.difficulty_buttons[1].image = ImageTk.PhotoImage(
            Image.open(self.theme.medium_button_path).resize((int(width / 6), int(2 * height / 7)), Image.ANTIALIAS))
        self.difficulty_buttons[2].image = ImageTk.PhotoImage(
            Image.open(self.theme.hard_button_path).resize((int(width / 6), int(2 * height / 7)), Image.ANTIALIAS))

        self.difficulty_buttons[0].index = self.main_canvas.create_image(1 * width / 6,
                                                                         height / 2,
                                                                         image=self.difficulty_buttons[0].image)
        self.difficulty_buttons[1].index = self.main_canvas.create_image(3 * width / 6,
                                                                         height / 2,
                                                                         image=self.difficulty_buttons[1].image)
        self.difficulty_buttons[2].index = self.main_canvas.create_image(5 * width / 6,
                                                                         height / 2,
                                                                         image=self.difficulty_buttons[2].image)

        self.main_canvas.tag_bind(self.difficulty_buttons[0].index, '<Button-1>', self.easy)
        self.main_canvas.tag_bind(self.difficulty_buttons[1].index, '<Button-1>', self.medium)
        self.main_canvas.tag_bind(self.difficulty_buttons[2].index, '<Button-1>', self.hard)

    def update_board(self, width, height):
        """
        Resizes the board to fit the window size.
        :param width: the width of the window
        :param height: the height of the window
        """
        self.size = self.scale * min(width, height)
        self.game.x_left = (width - self.size) / 2 + 0.025 * self.size
        self.game.y_up = (height - self.size) / 2 + 0.025 * self.size
        self.game.x_right = (width + self.size) / 2 - 0.025 * self.size
        self.game.y_down = (height + self.size) / 2 - 0.025 * self.size

        self.border = self.main_canvas.create_rectangle((width - self.size) / 2,
                                                        (height - self.size) / 2,
                                                        (width + self.size) / 2,
                                                        (height + self.size) / 2,
                                                        fill=self.theme.border_fill,
                                                        width=0)
        self.board = self.main_canvas.create_rectangle(self.game.x_left,
                                                       self.game.y_up,
                                                       self.game.x_right,
                                                       self.game.y_down,
                                                       fill=self.theme.board_fill,
                                                       width=0)
        self.separator = self.main_canvas.create_rectangle(width / 2 - 0.025 * self.size,
                                                           (height - self.size) / 2,
                                                           width / 2 + 0.025 * self.size,
                                                           (height + self.size) / 2,
                                                           fill=self.theme.border_fill,
                                                           width=0)

        self.update_triangles(width, height)

    def update_triangles(self, width, height):
        """
        Resizes the slots (triangles) to fit the window size.
        :param width: the width of the window
        :param height: the height of the window
        """
        backup = deepcopy(self.game.slots)

        self.size = self.scale * min(width, height)
        offsets = [self.game.x_left, width / 2 + 0.025 * self.size]
        bases = [self.game.y_down, self.game.y_up]
        tops = [bases[0] - 0.95 * self.size / 3, bases[1] + 0.95 * self.size / 3]
        self.triangle_width = 0.9 * self.size / 12

        for i in range(0, 4):
            for j in range(0, 6):
                self.triangles[i * 6 + j] = self.main_canvas.create_polygon(offsets[i % 2] + j * self.triangle_width,
                                                                            bases[int(bool(i > 1))],
                                                                            offsets[i % 2] + (2 * j + 1) * self.triangle_width / 2,
                                                                            tops[int(bool(i > 1))],
                                                                            offsets[i % 2] + (j + 1) * self.triangle_width,
                                                                            bases[int(bool(i > 1))],
                                                                            fill=self.theme.triangle_fill)
                self.game.slots[i * 6 + j] = Slot(index=self.triangles[i * 6 + j], position=i * 6 + j)

        for i in range(0, len(backup)):
            self.game.slots[i].pieces = deepcopy(backup[i].pieces)

    def play_single(self, event):
        """
        For choosing to play with the computer.
        :param event: widget used for getting the current width and height of the screen
        """
        self.current_menu = Menu.DIFFICULTY_MENU
        self.update(event)

    def play_two(self, event):
        """
        For choosing to play with another player locally.
        :param event: widget used for getting the current width and height of the screen
        """
        self.current_menu = Menu.NAME_MENU
        self.game_mode = GameMode.VS
        self.update(event)

    def easy(self, event):
        """
        For choosing to play with the computer on an easy difficulty.
        :param event: widget used for getting the current width and height of the screen
        """
        self.current_menu = Menu.GAME_MENU
        self.game_mode = GameMode.EASY
        self.update(event)

    def medium(self, event):
        """
        For choosing to play with the computer on a medium difficulty.
        :param event: widget used for getting the current width and height of the screen
        """
        self.current_menu = Menu.GAME_MENU
        self.game_mode = GameMode.MEDIUM
        self.update(event)

    def hard(self, event):
        """
        For choosing to play with the computer on a hard difficulty.
        :param event: widget used for getting the current width and height of the screen
        """
        self.current_menu = Menu.GAME_MENU
        self.game_mode = GameMode.HARD
        self.update(event)
