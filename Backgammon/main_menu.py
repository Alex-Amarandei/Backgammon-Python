import tkinter as tk
from PIL import Image, ImageTk
from difficulty_menu import DifficultyMenu


class MainMenu:
    def __init__(self, root, theme):
        self.root = root
        self.theme = theme

        self.background_image = ImageTk.PhotoImage(file=self.theme.background_image_path)
        self.screen = {'width': self.root.winfo_screenwidth(),
                       'height': self.root.winfo_screenheight()}
        self.main_canvas = tk.Canvas(self.root,
                                     width=self.screen['width'],
                                     height=self.screen['height'],
                                     cursor='circle')
        self.main_canvas.create_image(0, 0, image=self.background_image, anchor='nw')

        self.game_title = None

        self.single_player_button = None
        self.single_player_button_image = None

        self.two_players_button = None
        self.two_players_button_image = None

        self.update_title(self.screen['width'], self.screen['height'])
        self.update_buttons(self.screen['width'], self.screen['height'])

        self.main_canvas.pack(fill='both', expand=True)
        self.root.bind('<Configure>', self.update)

    def update_title(self, width, height):
        font = 'Century ' + str(int(min(width / 16, height / 6))) + ' bold'

        self.game_title = self.main_canvas.create_text(width / 2,
                                                       height / 6,
                                                       fill=self.theme.font_color,
                                                       font=font,
                                                       text='Backgammon')

    def update_buttons(self, width, height):
        self.single_player_button_image = ImageTk.PhotoImage(
            Image.open(self.theme.single_button_path).resize((int(width / 2), int(height / 7)), Image.ANTIALIAS))
        self.two_players_button_image = ImageTk.PhotoImage(
            Image.open(self.theme.two_button_path).resize((int(width / 2), int(height / 7)), Image.ANTIALIAS))

        self.single_player_button = self.main_canvas.create_image(width / 2,
                                                                  3 * height / 7,
                                                                  image=self.single_player_button_image)
        self.two_players_button = self.main_canvas.create_image(width / 2,
                                                                5 * height / 7,
                                                                image=self.two_players_button_image)

        self.main_canvas.tag_bind(self.single_player_button, '<Button-1>', self.play_single)
        self.main_canvas.tag_bind(self.two_players_button, '<Button-1>', self.play_two)

    def update(self, event):
        self.main_canvas.delete(self.game_title)
        self.update_title(event.width, event.height)

        self.update_buttons(event.width, event.height)

    def play_single(self, event):
        self.main_canvas.destroy()

        DifficultyMenu(self.root, self.theme)

    def play_two(self, event):
        pass
