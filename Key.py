from graphics import Image
from graphics import Point
from Collisions import *
from characters.Player import Player
class Key:
    def __init__(self, x,y, type,player):
        self.x = x
        self.y = y
        self.type = type
        self.image = Image(Point(self.x,self.y), "sprites/keycards/keycard_"+type+".png")
        self.collected = False
        self.player = player

    def draw(self, gw):
        self.image.draw(gw)
    def update(self):
        if (pointCircle(self.player.getPos().x,self.player.getPos().y,self.x,self.y,30)):
            if not self.collected:
                self.collect()

    def collect(self):
        if not self.collected:
            self.image.undraw()
            self.collected = True
            self.player.collectKey(self.type)

