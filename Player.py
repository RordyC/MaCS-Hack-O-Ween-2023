from graphics import *
from InputHandler import *
from Collisions import circleRectMove
from Animation import Animation

class Player():
    def __init__(self, playerStart:Point,inputHandler:InputHandler):
        self.__inputHandler = inputHandler #Using this we can get direction the player wants to move!
        self.__circle = Circle(playerStart, 16)
        self.__circle.setFill("orange")
        self.__circle.setOutline("brown")

        self.__speed = 125.0   #How fast the player can run around.
        self.__vx = 0.0 #Player velocity on the X axis.
        self.__vy = 0.0 #Player velocity on the Y axis.
        self.keys = {'red': False, 'green':False, 'blue':False}
        self.collected_keys = []
        self.__ct = [] #The tiles that the player will check for collision with.

    
    def collect_keys(self, key_color):
        if key_color in self.keys and not self.keys[key_color]:
            self.keys[key_color] = True
            self.collected_keys.append(key_color)

    def has_key(self, key_color):
        if key_color in self.keys:
            return self.keys[key_color]
        else:
            return False

    def calculateTileCollisions(potPos):
        newPos = circleRectMove(25, potPos, 10 * 32, 4 * 32)
        return newPos

    def update(self,deltaTime:float):
        currentX = self.__circle.getCenter().x
        currentY = self.__circle.getCenter().y
        self.__vx = self.__inputHandler.getXAxis() * self.__speed * deltaTime
        self.__vy = self.__inputHandler.getYAxis() * self.__speed * deltaTime
        potentialPosition = [currentX + self.__vx, currentY + self.__vy]

        if (len(self.__ct) > 0):
         for t in self.__ct:
            potentialPosition = circleRectMove(16,potentialPosition,t.getGridPos()[1] *32,t.getGridPos()[0]*32)

        step = [potentialPosition[0] - currentX, potentialPosition[1] - currentY]
        self.__circle.move(step[0],step[1])
        
        pass
    def getPos(self):
        return self.__circle.getCenter()

    def setCollisionTiles(self, tiles):
        self.__ct = tiles
    
    def draw(self, gw: GraphWin):
            self.__circle.draw(gw)
          


