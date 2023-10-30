import graphics
from graphics import *

paths = [
    ["sprites/walls/wall_front","sprites/walls/wall_front_right","sprites/walls/wall_front_left"],
    ["sprites/floors/floor_top","sprites/floors/floor_top_door","sprites/floors/floor_right","sprites/floors/floor_left","sprites/floors/floor_left_top_corner","sprites/floors/floor_right_top_corner","sprites/floors/floor_left_bottom_corner","sprites/floors/floor_right_bottom_corner"],
    ["sprites/floors/floor_base","sprites/floors/floor_vent_left","sprites/floors/floor_vent_right"],
    ["sprites/walls/wall_back","sprites/walls/wall_back_right","sprites/walls/wall_back_left","sprites/walls/wall_left","sprites/walls/wall_right"],
    ["sprites/blood/blood_top1","sprites/blood/blood_top2","sprites/blood/blood_top3"],
    ["sprites/key_wall/key_wall_blue", "sprites/key_wall/key_wall_red", "sprites/key_wall/key_wall_yellow","sprites/key_wall/key_wall_green","sprites/key_wall/key_wall_pink",
     "sprites/key_wall/terminal_red", "sprites/walls/wall_right"]
        ]

class WorldSprite():
    def __init__(self,x,y,typeID:int,typeVariationID:int,layer:int,win:graphics.GraphWin):
        self.x = x
        self.y = y
        self.__typeInd = typeID
        self.__typeVar = typeVariationID
        self.__win = win
        self.__image = Image(Point(self.x,self.y),(paths[self.__typeInd][self.__typeVar] + ".png"))
        self.__grabPoint = Circle(Point(self.x,self.y),10)
        self.__grabPoint.setFill("Cyan")
        self.__grabPoint.setOutline("White")
        self.__layer = layer
        self.__layerText = Text(Point(self.x,self.y),str(self.__layer))
        self.__layerText.setTextColor("BLACK")
        self.__layerText.setStyle("bold")

    def __str__(self):
        return f"{self.__typeInd},{self.__typeVar}"

    def draw(self):
        self.__image.draw(self.__win)
    def setPos(self, x, y):
        dx = x - self.x
        dy = y - self.y
        self.__image.move(dx,dy)
        self.__layerText.move(dx,dy)
        self.__grabPoint.move(dx,dy)

        self.x = x
        self.y = y
    def getGrabPointPos(self):
        return self.__grabPoint.getCenter()
    def redraw(self):
        self.__image.undraw()
        self.__grabPoint.undraw()
        self.__layerText.undraw()
        self.__image = Image(Point(self.x, self.y), (paths[self.__typeInd][self.__typeVar] + ".png"))
        self.__image.draw(self.__win)
        self.__grabPoint.draw(self.__win)
        self.__layerText.draw(self.__win)
        #self.__win.lower(self.__layerText.id)
        #self.__win.lower(self.__grabPoint.id)
        #self.__win.lower(self.__image.id)
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
    def toggleLayer(self):
        self.__layer = (self.__layer + 1)%3
        self.__layerText.setText(self.__layer)
    def editMode(self,isInEditMode:bool):
        if not (isInEditMode):
            self.__grabPoint.undraw()
            self.__layerText.undraw()
        else:
            self.__grabPoint.draw(self.__win)
            self.__layerText.draw(self.__win)
    def getData(self):
        return (self.x,self.y,self.__typeInd,self.__typeVar,self.__layer)
    def getType(self):
        return (self.__typeInd,self.__typeVar)
    def getLayer(self):
        return self.__layer
