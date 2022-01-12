import tkinter as tk

from PIL import Image, ImageTk
from menus import Menu
from ui_button import UIButton


class GUI:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme
        self.current_menu = Menu.MAIN_MENU

        self.background_image = ImageTk.PhotoImage(file=self.theme.background_image_path)
        self.screen = {'width': self.root.winfo_screenwidth(),
                       'height': self.root.winfo_screenheight()}
        self.main_canvas = tk.Canvas(self.root,
                                     width=self.screen['width'],
                                     height=self.screen['height'],
                                     cursor='circle')
        self.main_canvas.create_image(0, 0, image=self.background_image, anchor='nw')

        self.game_title = None
        self.player_buttons = [UIButton(), UIButton()]
        self.difficulty_buttons = [UIButton(), UIButton(), UIButton()]

        self.main_canvas.pack(fill='both', expand=True)
        self.main_canvas.bind('<Configure>', self.update)

    def update(self, event):
        if self.current_menu == Menu.MAIN_MENU:
            self.update_main_menu(event)
        elif self.current_menu == Menu.DIFFICULTY_MENU:
            self.update_difficulty_menu(event)
        elif self.current_menu == Menu.GAME_MENU:
            self.update_game_menu(event)

    def update_main_menu(self, event):
        self.update_title(event.widget.winfo_width(), event.widget.winfo_height())
        for x in self.difficulty_buttons:
            self.main_canvas.delete(x.index)
        self.update_player_buttons(event.widget.winfo_width(), event.widget.winfo_height())

    def update_difficulty_menu(self, event):
        self.update_title(event.widget.winfo_width(), event.widget.winfo_height())
        for x in self.player_buttons:
            self.main_canvas.delete(x.index)
        self.update_difficulty_buttons(event.widget.winfo_width(), event.widget.winfo_height())

    def update_title(self, width, height):
        self.main_canvas.delete(self.game_title)

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

    def play_single(self, event):
        self.current_menu = Menu.DIFFICULTY_MENU
        self.update(event)

    def play_two(self, event):
        print(self.theme)

    def easy(self, event):
        self.current_menu = Menu.MAIN_MENU
        self.update(event)

    def medium(self, event):
        self.current_menu = Menu.MAIN_MENU
        self.update(event)

    def hard(self, event):
        self.current_menu = Menu.MAIN_MENU
        self.update(event)
