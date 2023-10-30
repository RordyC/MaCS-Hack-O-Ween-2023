
from game_systems.graphics import *
from game_systems.Collisions import circleRect
class ViewShifter():
    def __init__(self,x,y,player,graphWin,firstOffset,secondOffset, isVertical:bool):
        self.x = x
        self.y = y
        self.__firstOffset = firstOffset
        self.__secondOffSet = secondOffset
        self.__player = player
        self.__win = graphWin
        self.__debugRect = Rectangle(Point(self.x-32,self.y-32),Point(self.x +32,self.y + 32))
        self.__debugRect.setOutline("ORANGE")
        self.__isPlayerInside = False
        self.__isVertical = isVertical

    def draw(self):
        self.__debugRect.draw(self.__win)
        print("!")

    def undraw(self):
        self.__debugRect.undraw()

    def update(self):
        if (circleRect(self.__player.getPos().x, self.__player.getPos().y, 16, self.x-32, self.y-32, 64, 64)):
            if (self.__isPlayerInside == False):
                self.__isPlayerInside = True
                self.__debugRect.setOutline("Light green")
        elif (self.__isPlayerInside == True):
            self.__isPlayerInside = False
            self.__debugRect.setOutline("orange")
            if (self.__isVertical):
                self.setWinCoords(self.isPlayerUp())
            else:
                self.setWinCoords(self.isPlayerRight())
    def isPlayerUp(self) -> bool:
        return (self.__player.getPos().y < self.y + 16)
    def isPlayerRight(self) -> bool:
        return (self.__player.getPos().x < self.x + 16)

    def setWinCoords(self, isUp:bool):
        if (isUp):
            self.__win.setCoords(self.__secondOffSet[0], 705 + self.__secondOffSet[1], 961 + self.__secondOffSet[0], self.__secondOffSet[1])
        else:
            self.__win.setCoords(self.__firstOffset[0], 705 + self.__firstOffset[1], 961 + self.__firstOffset[0], self.__firstOffset[1])

