from graphics import *
class TileBase:

    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.rect = Rectangle(Point(self.col * self.width,self.row * self.width),
                              Point(((self.col * self.width) + self.width),(self.row * self.width) +self.width))
        self.rect.setFill("BLACK")
        self.rect.setOutline("GREEN")

        self.state = -1
        self.stateColors = {0:"BLACK",1:"WHITE",2:"RED",3:"ORANGE",4:"CYAN"}

        self.neighbors = []


    def draw(self,win):
        self.rect.draw(win)
    def updateState(self,newState:int):
        self.state = newState
        self.rect.setFill(self.stateColors[self.state])

    def updateNeighbors(self,grid):
        pass
    def getState(self):
        return self.state