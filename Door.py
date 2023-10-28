from graphics import *
from Collisions import pointCircle
from Key import Key

class Door():
    def __init__(self,x,y):
        self.__posX = x
        self.__posY = y
        
      
        self.__panelRight = Image(Point(self.__posX, self.__posY), "sprites/door/door_right.png")
        self.__panelLeft = Image(Point(self.__posX, self.__posY), "sprites/door/door_left.png")
        self.__frameRight = Image(Point(self.__posX, self.__posY), "sprites/door/door_frame_right.png")
        self.__frameLeft = Image(Point(self.__posX, self.__posY), "sprites/door/door_frame_left.png")
        self.__anchorRight = 0
        print(self.__anchorRight)
        print(self.__panelRight.getAnchor().x)
        self.__anchorLeft = self.__panelLeft.getAnchor().x

        self.__doorSpeed = 64
        
        self.__is_open = False
        self.__playerX = 0
        self.__playerY = 0

        self.__tiles = []
        self.red_key_collected= False
    def draw(self, gw: GraphWin):
        self.__panelRight.draw(gw)
        self.__panelLeft.draw(gw)
        self.__frameRight.draw(gw)
        self.__frameLeft.draw(gw)
        self.__anchorRight = self.__panelRight.getAnchor().x
    
    def canOpen(self):
        return self.red_key_collected
    def setRedkeyCollected(self):
        self.red_key_collected = True
    def update(self, deltaT, has_key):
        if has_key:
            if self.canOpen():
                self.openDoor()
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
        if not self.__is_open and self.canOpen():
            self.__is_open = True
        if (self.__is_open == False):
            self.__is_open = not self.__is_open
            for tile in self.__tiles:
                tile.updateState(0)
    def checkPlayer(self):
        if (pointCircle(self.__playerX,self.__playerY,self.__posX + 32,self.__posY+32,69)):
            self.openDoor()
    def setPlayerCoords(self,playerX,playerY):
        self.__playerX = playerX
        self.__playerY = playerY
    def setTiles(self, tiles):
        self.__tiles = tiles