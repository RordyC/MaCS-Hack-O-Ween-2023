from graphics import *
from InputHandler import *
class Player():
    def __init__(self, playerStart:Point,inputHandler:InputHandler):
        self.__inputHandler = inputHandler #Using this we can get direction the player wants to move!
        self.__circle = Circle(playerStart, 16)
        self.__circle.setFill("orange")
        self.__circle.setOutline("brown")

        self.__speed = 200.0   #How fast the player can run around.
        self.__vx = 0.0 #Player velocity on the X axis.
        self.__vy = 0.0#Player velocity on the Y axis.

    def draw(self, gw: GraphWin):
            self.__circle.draw(gw)

    def update(self,deltaTime:float):
        self.__vx= self.__inputHandler.getXAxis() * self.__speed * deltaTime
        self.__vy = self.__inputHandler.getYAxis() * self.__speed * deltaTime
        self.__circle.move(self.__vx,self.__vy)
        pass
    def getPos(self):
        return self.__circle.getCenter()