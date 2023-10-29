from graphics import *
class Button:
    def __init__(self, position, image_path):
        self.image = Image(position, image_path)
        
    def draw(self, gw):
        self.image.draw(gw)