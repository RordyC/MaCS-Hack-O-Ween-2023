import graphics
from graphics import *
from Collisions import pointCircle

paths = {"wall":"sprites/wall.png"}

class WorldSprite():
    def __init__(self,x,y,type:str,win:graphics.GraphWin):
        self.x = x
        self.y = y
        self.__type = type
        self.__win = win
        self.__image = Image(Point(self.x,self.y),paths[self.__type])
        self.__grabPoint = Circle(Point(self.x,self.y),8)
        self.__grabPoint.setFill("Cyan")
        self.__grabPoint.setOutline("White")

    def draw(self):
        self.__image.draw(self.__win)
        self.__grabPoint.draw(self.__win)