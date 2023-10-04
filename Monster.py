from graphics import *
from math import sqrt
class Monster(object):
    def __init__(self):
        self.__movementSpeed = 2.0

        self.__currentTargetX = 0
        self.__currentTargetY = 0
        self.__img = Image(Point(0, 0), "head.png")
        self.__debugT = Text(Point(200, 25), "Centered Text")
        self.__debugT.setTextColor("white")

    def draw(self, gw: GraphWin):
        self.__img.draw(gw)
        self.__debugT.draw(gw)

    def setTargetPos(self, x, y):
        self.__currentTargetX = x
        self.__currentTargetY = y

    def update(self):
        self.dx = 0
        self.dy = 0

        self.dx = (self.__currentTargetX - self.__img.getAnchor().x)
        self.dy = (self.__currentTargetY - self.__img.getAnchor().y)
        if (abs(self.dx) < 1 and abs(self.dy) < 1):
            return

        self.m = sqrt(abs((self.dx * self.dx) + abs(self.dy * self.dy)))

        self.dx = self.dx / self.m
        self.dy = self.dy / self.m

        self.__debugT.setText("Monster Dir: "+str(self.dx.__round__(2)) + ":" + str(self.dy.__round__(2)))
        if (self.dx > 0.1, self.dy > 0.1):
            self.__img.move(self.dx * self.__movementSpeed, self.dy * self.__movementSpeed)
