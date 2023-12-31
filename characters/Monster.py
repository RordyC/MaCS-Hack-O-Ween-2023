import math

from game_systems.graphics import *
from math import sqrt
from time import *
class Monster():
    def __init__(self,startX,startY):
        self.__startX = startX
        self.__startY = startY
        self.__movementSpeed = 90
        self.__hasLineOfSight = True
        self.__currentTargetX = 0
        self.__currentTargetY = 0
        self.__playerDir = [0.0, 0.0]
        self.playerDistance = 0.0
        self.height = 25
        self.width = 25

        self.__path = []
        self.__currentTarget = [0,0]
        self.__currentPathTargetPos = [100, 100]

        self.__img = Image(Point(self.__startX, self.__startY), "sprites/ghost/ghost1.png")
        self.__imgs = [Image(Point(self.__startX, self.__startY),"sprites/ghost/ghost1.png"),Image(Point(self.__startX, self.__startY),"sprites/ghost/ghost2.png"),Image(Point(self.__startX, self.__startY),"sprites/ghost/ghost3.png")]
        self.__currentFrame = 0
        self.__animSpeed = 0.2
        self.__currentFrameTime = 0.0
        self.__gw = None
        self.__angry = False
        self.__width = self.__img.getWidth()
        self.__dir = [0,0]

    def draw(self, gw: GraphWin):
        self.__gw = gw
        self.__imgs[0].draw(gw)

    def hit(self,isHit):

        if not (isHit == self.__angry):
            self.__angry = isHit
        else:
            return

        if (isHit):
            #self.__img.undraw()
            #self.__altImg.draw(self.__gw)
            # commented out game over screen because it is annoying when looking for coords and stuff xd
            self.game_over_screen()

        else:
            pass
           # self.__altImg.undraw()
           # self.__img.draw(self.__gw)

    def game_over_screen(self):
        self.resetPos()
        return
        '''
        # unfinished death message
        deathMessage = Text(Point(480, 325), 'YOU DIED')
        deathMessage.setSize(20)
        deathMessage.setTextColor('white')
        deathMessage.draw(self.__gw)
        
        deathMessage.undraw()
        '''
        overlay = Rectangle(Point(0, 0), Point(961, 705))
        overlay.setFill('black')
        overlay.setOutline('black')
        overlay.draw(self.__gw)

        restart_button = Rectangle(Point(353, 300), Point(607, 350))
        restart_button.setFill('white')
        restartLabel = Text(Point(480, 325), 'RESTART')
        restartLabel.setSize(20)
        restartLabel.setTextColor('black')
        restartLabel.setStyle('bold italic')
        restart_button.draw(self.__gw)
        restartLabel.draw(self.__gw)

        game_over_text = Text(Point(480, 100), 'Game Over')
        game_over_text.setSize(28)
        game_over_text.setTextColor('red')
        game_over_text.setStyle('bold italic')
        game_over_text.draw(self.__gw)

        self.__gw.getMouse()
        game_over_text.undraw()
        overlay.undraw()

        

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
            self.dx = (self.__currentPathTargetPos[0] - self.__img.getAnchor().x)
            self.dy = (self.__currentPathTargetPos[1] - self.__img.getAnchor().y)

        if (abs(self.dx) < 12 and abs(self.dy) < 12):
            if (self.__hasLineOfSight == False and len(self.__path) > 0):
                target = self.__path.pop(0)
                self.__currentTarget = target

                self.__currentPathTargetPos[0] = (target[1] * 32) + 16
                self.__currentPathTargetPos[1] = (target[0] * 32) + 16
                #print(target[0] * 32,target[1])

        self.m = sqrt(abs((self.dx * self.dx) + abs(self.dy * self.dy)))

        self.dx = self.dx / self.m
        self.dy = self.dy / self.m

        self.__dir[0] = self.dx
        self.__dir[1] = self.dy

        if (self.m > 10):
            self.__img.move(self.dx * self.__movementSpeed * deltaT, self.dy * self.__movementSpeed * deltaT)
            for i in self.__imgs:
                i.move(self.dx * self.__movementSpeed * deltaT, self.dy * self.__movementSpeed * deltaT)

        self.__currentFrameTime = self.__currentFrameTime + deltaT
        if (self.__currentFrameTime > self.__animSpeed):
            self.__currentFrameTime = 0
            self.__imgs[self.__currentFrame].undraw()
            self.__currentFrame = (self.__currentFrame + 1) % 3
            self.__imgs[self.__currentFrame].draw(self.__gw)
    def getPos(self):
        return self.__img.getAnchor()
    def resetPos(self):
        dx = self.__startX - self.__img.getAnchor().x
        dy = self.__startY - self.__img.getAnchor().y
        self.__img.move(dx, dy)
        for i in self.__imgs:
            i.move(dx, dy)
    def calculatePlayerDir(self):
        dx = (self.__currentTargetX - self.__img.getAnchor().x)
        dy = (self.__currentTargetY - self.__img.getAnchor().y)

        m = sqrt(abs((dx*dx) + abs(dy*dy)))
        if (m == 0):
            return
        self.playerDistance = m
        dx = dx / m
        dy = dy / m

        self.__playerDir[0] = dx
        self.__playerDir[1] = dy
    def getPlayerDir(self):
        return self.__playerDir
    def getPlayerDist(self):
        return self.playerDistance
    def updatePath(self, path):
        self.__path = path
        for i, p in enumerate(self.__path):
            if (p == self.__currentTarget):
                for x in range(0,i):
                    self.__path.pop(0)

        target = self.__path.pop(0)
        self.__currentTarget == target
        self.__currentPathTargetPos[0] = (target[1] * 32) + 16
        self.__currentPathTargetPos[1] = (target[0] * 32) + 16
    def updateLineOfSight(self, los:bool):
        self.__hasLineOfSight = los