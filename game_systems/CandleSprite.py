import random
from graphics import *
class Candle():
    def __init__(self,x,y,lit:bool,gw):
        self.x = x
        self.y = y
        self.lit = lit
        self.__imgs = [Image(Point(self.x,self.y),"sprites/candles/candle1.png"),Image(Point(self.x,self.y),("sprites/candles/candle2.png")),Image(Point(self.x,self.y),("sprites/candles/candle_unlit.png"))]
        self.__gw = gw
        self.frameTime = 0.25
        self.__currentFrameTime = random.uniform(0.0,self.frameTime)
        self.__currentFrame = 0

    def draw(self):
        if not self.lit:
            self.__imgs[2].draw(self.__gw)
        else:
            self.__imgs[0].draw(self.__gw)
    def update(self,deltaT):
        if (self.lit):
            self.__currentFrameTime = self.__currentFrameTime + deltaT
            if (self.__currentFrameTime > self.frameTime):
               self.__currentFrameTime = 0
               self.__imgs[self.__currentFrame].undraw()
               self.__currentFrame = (self.__currentFrame + 1) % 2
               self.__imgs[self.__currentFrame].draw(self.__gw)
