from graphics import Image
from Collisions import *
class Key:
    def __init__(self, center, image_path):
        self.image = Image(center, image_path)
        self.collected = False

    def draw(self, gw):
        self.image.draw(gw)

    def is_collected(self):
        return self.collected

    def collect(self):
        if not self.collected:
            self.image.undraw()
            self.collected = True

