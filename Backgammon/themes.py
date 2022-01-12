import subprocess


class DarkTheme:
    font_color = '#f5f5f5'
    background_image_path = 'images/Dark.png'
    single_button_path = 'images/Single Player Dark Button.png'
    two_button_path = 'images/Two Players Dark Button.png'


class LightTheme:
    font_color = '#152238'
    background_image_path = 'images/Light.png'
    single_button_path = 'images/Single Player Light Button.png'
    two_button_path = 'images/Two Players Light Button.png'


def dark_theme_selected():
    command = 'defaults read -g AppleInterfaceStyle'
    process = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)

    return bool(process.communicate()[0])
