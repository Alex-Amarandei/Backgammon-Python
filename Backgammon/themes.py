import subprocess


class DarkTheme:
    font_color = '#f5f5f5'
    background_image_path = 'images/Dark.png'
    single_button_path = 'images/Single Player Dark Button.png'
    two_button_path = 'images/Two Players Dark Button.png'
    easy_button_path = 'images/Easy Button.png'
    medium_button_path = 'images/Medium Button.png'
    hard_button_path = 'images/Hard Button.png'
    border_fill = '#000000'
    board_fill = '#56342A'
    triangle_fill = '#505050'
    white_fill = '#FFFFFF'
    black_fill = '#900000'


class LightTheme:
    font_color = '#152238'
    background_image_path = 'images/Light.png'
    single_button_path = 'images/Single Player Light Button.png'
    two_button_path = 'images/Two Players Light Button.png'
    easy_button_path = 'images/Easy Button.png'
    medium_button_path = 'images/Medium Button.png'
    hard_button_path = 'images/Hard Button.png'
    border_fill = '#C19A6C'
    board_fill = '#FFF8DC'
    triangle_fill = '#D8D8D8'
    white_fill = '#FFFFFF'
    black_fill = '#900000'


def dark_theme_selected():
    command = 'defaults read -g AppleInterfaceStyle'
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)

    return bool(process.communicate()[0])
