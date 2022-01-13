import tkinter as tk

from game import *
from menus import Menu
from PIL import Image, ImageTk
from ui_button import UIButton
from game_modes import GameMode


class GUI:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme
        self.scale = 0.8
        self.size = None

        self.game = None
        self.game_mode = GameMode.VS
        self.current_menu = Menu.MAIN_MENU

        self.background_image = ImageTk.PhotoImage(file=self.theme.background_image_path)
        self.screen = {'width': self.root.winfo_screenwidth(), 'height': self.root.winfo_screenheight()}
        self.main_canvas = tk.Canvas(self.root, width=self.screen['width'], height=self.screen['height'], cursor='circle')
        self.main_canvas.create_image(0, 0, image=self.background_image, anchor='nw')

        self.game_title = None
        self.player_buttons = [UIButton(), UIButton()]
        self.difficulty_buttons = [UIButton(), UIButton(), UIButton()]

        self.border = None
        self.board = None
        self.separator = None
        self.triangles = 24 * [None]
        self.triangle_width = None

        self.main_canvas.pack(fill='both', expand=True)
        self.main_canvas.bind('<Configure>', self.update)

    def update(self, event):
        self.clean()

        if self.current_menu == Menu.MAIN_MENU:
            self.update_main_menu(event)
        elif self.current_menu == Menu.DIFFICULTY_MENU:
            self.update_difficulty_menu(event)
        elif self.current_menu == Menu.GAME_MENU:
            self.update_game_menu(event)

    def clean(self):
        self.main_canvas.delete('all')
        self.main_canvas.create_image(0, 0, image=self.background_image, anchor='nw')

    def update_main_menu(self, event):
        self.update_title(event.widget.winfo_width(), event.widget.winfo_height())
        self.update_player_buttons(event.widget.winfo_width(), event.widget.winfo_height())

    def update_difficulty_menu(self, event):
        self.update_title(event.widget.winfo_width(), event.widget.winfo_height())
        self.update_difficulty_buttons(event.widget.winfo_width(), event.widget.winfo_height())

    def update_game_menu(self, event):
        self.game = Game(self)
        self.update_board(event.widget.winfo_width(), event.widget.winfo_height())
        self.game.update_game(event)

    def update_title(self, width, height):
        font = 'Century ' + str(int(min(width / 16, height / 6))) + ' bold'
        self.game_title = self.main_canvas.create_text(width / 2,
                                                       height / 6,
                                                       fill=self.theme.font_color,
                                                       font=font,
                                                       text='Backgammon')

    def update_player_buttons(self, width, height):
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

    def play_single(self, event):
        self.current_menu = Menu.DIFFICULTY_MENU
        self.update(event)

    def play_two(self, event):
        self.current_menu = Menu.GAME_MENU
        self.game_mode = GameMode.VS
        self.update(event)

    def easy(self, event):
        self.current_menu = Menu.GAME_MENU
        self.game_mode = GameMode.EASY
        self.update(event)

    def medium(self, event):
        self.current_menu = Menu.GAME_MENU
        self.game_mode = GameMode.MEDIUM
        self.update(event)

    def hard(self, event):
        self.current_menu = Menu.GAME_MENU
        self.game_mode = GameMode.HARD
        self.update(event)
