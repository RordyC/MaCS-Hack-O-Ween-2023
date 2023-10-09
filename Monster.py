from graphics import *
from math import sqrt
class Monster():
    def __init__(self):
        self.__movementSpeed = 25

        self.__currentTargetX = 0
        self.__currentTargetY = 0
        self.__img = Image(Point(25, 25), "head.png")
        self.__gw = None
        self.__angry = False
        self.__altImg = Image(Point(25, 25), "angry_head.png")
        self.__width = self.__img.getWidth()
        self.__debugT = Text(Point(200, 25), "Centered Text")
        self.__debugT.setTextColor("white")
        print(self.__width)

    def draw(self, gw: GraphWin):
        self.__gw = gw
        self.__img.draw(gw)
        self.__debugT.draw(gw)

    def hit(self,isHit):

        if not (isHit == self.__angry):
            self.__angry = isHit
        else:
            return

        if (isHit):
            self.__img.undraw()
            self.__altImg.draw(self.__gw)
        else:
            self.__altImg.undraw()
            self.__img.draw(self.__gw)


    def setTargetPos(self, x, y):
        self.__currentTargetX = x
        self.__currentTargetY = y

    def update(self,deltaT):
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
            self.__img.move(self.dx * self.__movementSpeed * deltaT, self.dy * self.__movementSpeed * deltaT)
            self.__altImg.move(self.dx * self.__movementSpeed * deltaT, self.dy * self.__movementSpeed * deltaT)
    def getPos(self):
        return self.__img.getAnchor()