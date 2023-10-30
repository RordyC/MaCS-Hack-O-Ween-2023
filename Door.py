from graphics import *
from Collisions import pointCircle
from characters.Player import Player
from Key import Key

class Door():
    def __init__(self,x,y,keycard:str,player):
        self.__posX = x
        self.__posY = y
      
        self.__panelRight = Image(Point(self.__posX, self.__posY), "sprites/door/door_right.png")
        self.__panelLeft = Image(Point(self.__posX, self.__posY), "sprites/door/door_left.png")
        self.__frameRight = Image(Point(self.__posX, self.__posY), "sprites/door/door_frame_right.png")
        self.__frameLeft = Image(Point(self.__posX, self.__posY), "sprites/door/door_frame_left.png")
        self.__anchorRight = 0
        self.__anchorLeft = self.__panelLeft.getAnchor().x

        self.__doorSpeed = 64
        
        self.__is_open = False

        self.__tiles = []
        self.__keycard = keycard
        self.__player = player
    def draw(self, gw: GraphWin):
        self.__panelRight.draw(gw)
        self.__panelLeft.draw(gw)
        self.__frameRight.draw(gw)
        self.__frameLeft.draw(gw)
        self.__anchorRight = self.__panelRight.getAnchor().x
    def update(self, deltaT):
            self.checkPlayer()
            if self.__is_open:
                if self.__panelRight.getAnchor().x < self.__anchorRight + 32:
                    self.__panelRight.move(deltaT * self.__doorSpeed, 0)
                if self.__panelLeft.getAnchor().x > self.__anchorLeft - 32:
                    self.__panelLeft.move(deltaT * -self.__doorSpeed, 0)
            else:
                if self.__panelRight.getAnchor().x > self.__anchorRight:
                    self.__panelRight.move(deltaT * -self.__doorSpeed, 0)
                if self.__panelLeft.getAnchor().x < self.__anchorLeft:
                    self.__panelLeft.move(deltaT * self.__doorSpeed, 0)
    def getPosX(self):
        return self.__posX
    def openDoor(self):
        self.__is_open = True
        for tile in self.__tiles:
            tile.updateState(0)
    def checkPlayer(self):
        if (pointCircle(self.__player.getPos().x,self.__player.getPos().y,self.__posX,self.__posY,75) and self.__is_open == False):
            if (self.__keycard == None):
                self.openDoor()
            elif self.__player.has_key(self.__keycard):
                self.openDoor()

    def setTiles(self, tiles):
        self.__tiles = tiles
        for tile in self.__tiles:
            tile.updateState(1)