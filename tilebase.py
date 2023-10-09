
from graphics import *

class TileBase:

    def __init__(self,row,col,width,total_rows):

        self.drawPaths = False

        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.rect = Rectangle(Point(self.col * self.width,self.row * self.width),
                              Point(((self.col * self.width) + self.width),(self.row * self.width) +self.width))

        self.rect.setFill("BLACK")
        self.rect.setOutline("GREEN")

        self.state = 0
        self.stateColors = {0:"BLACK",1:"WHITE",2:"BLACK",3:"ORANGE",4:"CYAN",5:"BLACK",6:"Purple"}
        self.stateOutlines = {0: "GREEN", 1: "GREEN", 2: "YELLOW", 3: "GREEN", 4: "GREEN",5:"GREEN",6:"GREEN"}
        self.neighbors = []
        self.score = Text(Point((self.col * self.width) + 24, (self.row * self.width) + 8), "inf")
        self.score.setSize(8)
        self.score.setTextColor("WHITE")
        self.score.setTextColor("brown")

        self.gCostTxt = Text(Point((self.col * self.width) + 8, (self.row * self.width) + 8), "inf")
        self.gCostTxt.setTextColor("white")
        self.gCostTxt.setSize(8)
        self.fCostTxt = Text(Point((self.col * self.width) + 16, (self.row * self.width) + 22), "0")
        self.fCostTxt.setTextColor("white")
        self.fCostTxt.setSize(12)
    def getPos(self):
        return self.row, self.col
    def draw(self,win):
        if (True):
            self.rect.draw(win)

            if (self.drawPaths):
                self.score.draw(win)
                self.gCostTxt.draw(win)
                self.fCostTxt.draw(win)
    def updateState(self,newState:int):
        self.state = newState

        if not self.drawPaths and newState != 1:
            return
        self.rect.setFill(self.stateColors[self.state])
        self.rect.setOutline(self.stateOutlines[self.state])

    def updateNeighbors(self,grid):
        self.neighbors = []

        if (self.row < self.total_rows - 1):
            down = grid[self.row + 1][self.col]
            if not down.getState() == 1: self.neighbors.append(down)
        if (self.row > 0):
            up = grid[self.row - 1][self.col]
            if not up.getState() == 1: self.neighbors.append(up)
        if (self.col < self.total_rows - 1):
            right = grid[self.row][self.col+1]
            if not (right.getState() == 1): self.neighbors.append(right)
        if (self.col > 0):
            left = grid[self.row][self.col - 1]
            if not left.getState() == 1: self.neighbors.append(left)

        #Upper left
        #Upper Right
        #Lower Left
        #Lower Right
    def getState(self) -> int:
        return self.state
    def printNeighbors(self):
        print("_______")
        for n in self.neighbors:

            print(n.getPos())
    def setHCostText(self,score):
        self.score.setText(str(score))

    def setGCostText(self, score):
        self.gCostTxt.setText(str(score))

    def setFCostText(self, score):
        self.fCostTxt.setText(str(score))