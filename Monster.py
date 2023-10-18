import math

from graphics import *
from math import sqrt
class Monster():
    def __init__(self):
        self.__movementSpeed = 50
        self.__hasLineOfSight = True
        self.__currentTargetX = 0
        self.__currentTargetY = 0
        self.__playerDir = [0.0, 0.0]
        self.playerDistance = 0.0

        self.__path = []
        self.__currentPathTarget = [100, 100]

        self.__img = Image(Point(25, 25), "head.png")
        self.__gw = None
        self.__angry = False
        self.__altImg = Image(Point(25, 25), "angry_head.png")
        self.__width = self.__img.getWidth()
        self.__dir = [0,0]
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
        self.calculatePlayerDir()
        self.dx = 0
        self.dy = 0

        if (self.__hasLineOfSight):
            self.dx = (self.__currentTargetX - self.__img.getAnchor().x)
            self.dy = (self.__currentTargetY - self.__img.getAnchor().y)
        else:
            self.dx = (self.__currentPathTarget[0] - self.__img.getAnchor().x)
            self.dy = (self.__currentPathTarget[1] - self.__img.getAnchor().y)

        if (abs(self.dx) < 35 and abs(self.dy) < 35):
            if (self.__hasLineOfSight == False and len(self.__path) > 0):
                target = self.__path.pop(0)

                self.__currentPathTarget[0] = (target[1] * 32) + 16
                self.__currentPathTarget[1] = (target[0] * 32) + 16
                print(target[0] * 32,target[1])

        self.m = sqrt(abs((self.dx * self.dx) + abs(self.dy * self.dy)))

        self.dx = self.dx / self.m
        self.dy = self.dy / self.m

        self.__dir[0] = self.dx
        self.__dir[1] = self.dy

        if (self.m > 10):
            self.__img.move(self.dx * self.__movementSpeed * deltaT, self.dy * self.__movementSpeed * deltaT)
            self.__altImg.move(self.dx * self.__movementSpeed * deltaT, self.dy * self.__movementSpeed * deltaT)
    def getPos(self):
        return self.__img.getAnchor()

    def calculatePlayerDir(self):
        dx = (self.__currentTargetX - self.__img.getAnchor().x)
        dy = (self.__currentTargetY - self.__img.getAnchor().y)

        m = sqrt(abs((dx*dx) + abs(dy*dy)))
        self.playerDistance = m
        dx = dx / m
        dy = dy / m

        self.__playerDir[0] = dx
        self.__playerDir[1] = dy

        self.__debugT.setText("Monster Dir: " + str(self.__playerDir[0].__round__(2)) + ":" + str(self.__playerDir[1].__round__(2)))
    def getPlayerDir(self):
        return self.__playerDir
    def getPlayerDist(self):
        return self.playerDistance
    def updatePath(self, path):
        self.__path = path

        closestDistance = math.inf
        closestInd = 0

        for i, p in enumerate(path):
            currentDist = (p[0] * p[0]) + (p[1] * p[1])
            if (currentDist < closestDistance):
                closestDistance = currentDist
                print(closestDistance)
                closestInd = i
                break

        for i in range(0, closestInd):
            self.__path.pop(i)

        target = self.__path.pop(0)
        self.__currentPathTarget[0] = (target[1] * 32) + 16
        self.__currentPathTarget[1] = (target[0] * 32) + 16
    def updateLineOfSight(self, los:bool):
        self.__hasLineOfSight = los