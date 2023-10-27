import graphics
from graphics import *
from Collisions import pointCircle

paths = [
    ["sprites/walls/wall_front.png","sprites/walls/wall_front_right.png","sprites/walls/wall_front_left.png"],
    ["sprites/floors/floor_top.png","sprites/floors/floor_top_door.png"],
    ["sprites/floors/floor_base.png","sprites/floors/floor_vent_left.png","sprites/floors/floor_vent_right.png"],
    ["sprites/walls/wall_back.png","sprites/walls/wall_back_right.png","sprites/walls/wall_back_left.png","sprites/walls/wall_corner_left.png","sprites/walls/wall_corner_right.png"],
        ]

class WorldSprite():
    def __init__(self,x,y,typeID:int,typeVariationID:int,layer:int,win:graphics.GraphWin):
        self.x = x
        self.y = y
        self.__typeInd = typeID
        self.__typeVar = typeVariationID
        self.__win = win
        self.__image = Image(Point(self.x,self.y),paths[self.__typeInd][self.__typeVar])
        self.__grabPoint = Circle(Point(self.x,self.y),8)
        self.__grabPoint.setFill("Cyan")
        self.__grabPoint.setOutline("White")
        self.__layer = layer


    def __str__(self):
        return f"{self.__typeInd},{self.__typeVar}"

    def draw(self):
        self.__image.draw(self.__win)
    def setPos(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.__image.move(dx,dy)
        self.__grabPoint.move(dx,dy)

        self.x = x
        self.y = y
    def getGrabPointPos(self):
        return self.__grabPoint.getCenter()
    def redraw(self):
        self.__image.undraw()
        self.__grabPoint.undraw()
        self.__image = Image(Point(self.x, self.y), paths[self.__typeInd][self.__typeVar])
        self.__image.draw(self.__win)
        self.__grabPoint.draw(self.__win)
        self.__win.lower(self.__grabPoint.id)
        self.__win.lower(self.__image.id)
    def updateType(self, type:int):
        self.__typeInd = self.__typeInd + 1
        self.__typeVar = 0
        if (self.__typeInd > len(paths)-1):
            self.__typeInd = 0
        self.redraw()

        print(self.__typeInd)
    def updateVariation(self, type:int):
        self.__typeVar = self.__typeVar + 1
        if (self.__typeVar > len(paths[self.__typeInd]) - 1):
            self.__typeVar = 0
        self.redraw()
    def editMode(self,isInEditMode:bool):
        if not (isInEditMode):
            self.__grabPoint.undraw()
        else:
            self.__grabPoint.draw(self.__win)
    def getData(self):
        return (self.x,self.y,self.__typeInd,self.__typeVar,self.__layer)
