from graphics import *
from Collisions import pointCircle
class Door():
    def __init__(self,x,y,key):
        self.__posX = x
        self.__posY = y
        self.__key = key
        self.__panelRight = Image(Point(self.__posX, self.__posY), "sprites/door/door_right.png")
        self.__panelLeft = Image(Point(self.__posX, self.__posY), "sprites/door/door_left.png")
        self.__frameRight = Image(Point(self.__posX, self.__posY), "sprites/door/door_frame_right.png")
        self.__frameLeft = Image(Point(self.__posX, self.__posY), "sprites/door/door_frame_left.png")
        self.__anchorRight = 0
        print(self.__anchorRight)
        print(self.__panelRight.getAnchor().x)
        self.__anchorLeft = self.__panelLeft.getAnchor().x

        self.__doorSpeed = 64
        self.__isOpen = False
        self.__playerX = 0
        self.__playerY = 0
    def draw(self, gw: GraphWin):
        self.__panelRight.draw(gw)
        self.__panelLeft.draw(gw)
        self.__frameRight.draw(gw)
        self.__frameLeft.draw(gw)
        self.__anchorRight = self.__panelRight.getAnchor().x
    def update(self, deltaT):
        self.checkPlayer()
        if self.__isOpen:
            if self.__panelRight.getAnchor().x < self.__anchorRight + 32:
                self.__panelRight.move(deltaT * self.__doorSpeed, 0)
            if self.__panelLeft.getAnchor().x > self.__anchorLeft - 32:
                self.__panelLeft.move(deltaT * -self.__doorSpeed, 0)
        else:
            if self.__panelRight.getAnchor().x > self.__anchorRight:
                self.__panelRight.move(deltaT * -self.__doorSpeed, 0)
            if self.__panelLeft.getAnchor().x < self.__anchorLeft:
                self.__panelLeft.move(deltaT * self.__doorSpeed, 0)
    def open(self):
        self.__isOpen = not self.__isOpen
    def checkPlayer(self):
        if (pointCircle(self.__playerX,self.__playerY,self.__posX + 32,self.__posY+32,69)):
            self.__isOpen = True
    def setPlayerCoords(self,playerX,playerY):
        self.__playerX =playerX
        self.__playerY = playerY