from themes import *
from main_menu import *


def create_root():
    global root
    global theme

    root.title('Backgammon')
    root.iconphoto(True, ImageTk.PhotoImage(file='images/AppIcon.png'))

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(str(screen_width) + 'x' + str(screen_height))


if __name__ == '__main__':
    root = tk.Tk()
    theme = DarkTheme if dark_theme_selected() else LightTheme

    create_root()
    MainMenu(root, theme)
    root.mainloop()
