class UIButton:
    def __init__(self, index=None, image=None):
        """
        An object for better managing the button-related information such as the image and the canvas widget index.
        :param index: the canvas widget index
        :param image: the image corresponding to each UI element
        """
        self.index = index
        self.image = image
