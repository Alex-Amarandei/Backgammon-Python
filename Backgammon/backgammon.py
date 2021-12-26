import Themes
import subprocess
from tkinter import *


def check_appearance():
    command = 'defaults read -g AppleInterfaceStyle'
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)

    return bool(process.communicate()[0])


def create_root():
    global root
    global theme

    root.title('Backgammon')
    root.iconphoto(True, PhotoImage(file='images/AppIcon.png'))

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(str(screen_width) + 'x' + str(screen_height))


class MainMenu:
    global root
    global theme

    def __init__(self):
        self.background_image = PhotoImage(file=theme.background_image_path.value)

        screen = {'width': root.winfo_screenwidth(),
                  'height': root.winfo_screenheight()}

        self.main_canvas = Canvas(root, width=screen['width'], height=screen['height'])
        self.main_canvas.create_image(0, 0, image=self.background_image, anchor='nw')

        font = 'Century ' + str(int(min(screen['width'] / 20, screen['height'] / 10))) + ' bold'

        self.game_title = self.main_canvas.create_text(screen['width'] / 2,
                                                       screen['height'] / 6,
                                                       fill=theme.font_color.value,
                                                       font=font,
                                                       text='Backgammon')

        self.main_canvas.pack(fill='both', expand=True)

        root.bind('<Configure>', self.update)

    def update(self, event):
        font = 'Century ' + str(int(min(event.width / 15, event.height / 5))) + ' bold'

        self.main_canvas.delete(self.game_title)
        self.game_title = self.main_canvas.create_text(event.width / 2,
                                                       event.height / 6,
                                                       fill=theme.font_color.value,
                                                       font=font,
                                                       text='Backgammon')


if __name__ == '__main__':
    root = Tk()
    theme = Themes.DarkTheme if check_appearance() else Themes.LightTheme

    create_root()
    main_menu = MainMenu()
    root.mainloop()
