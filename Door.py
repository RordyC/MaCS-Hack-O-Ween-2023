from graphics import *
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

        self.speed = 4
        self.open = True
    def draw(self, gw: GraphWin):
        self.__panelRight.draw(gw)
        self.__panelLeft.draw(gw)
        self.__frameRight.draw(gw)
        self.__frameLeft.draw(gw)
        self.__anchorRight = self.__panelRight.getAnchor().x
        self.__panelRight.move(self.speed,0)
        self.__panelLeft.move(-self.speed,0)
    def update(self, deltaT):
        if self.open:
            if self.__panelRight.getAnchor().x < self.__anchorRight + 32:
                self.__panelRight.move(deltaT * self.speed, 0)
            if self.__panelLeft.getAnchor().x > self.__anchorLeft - 32:
                self.__panelLeft.move(deltaT * -self.speed, 0)
        else:
            self.__panelRight.move(deltaT * -self.speed, 0)
            if self.__panelRight.getAnchor().x < 322:
                self.open = True
        pass