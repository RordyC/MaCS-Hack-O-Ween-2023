import game_systems.graphics
from game_systems import graphics
from game_systems.graphics import *
from game_systems.tilebase import *



class TileBase:

    def __init__(self, row, col, width, total_rows):
        self.win: graphics.GraphWin = None
        self.row = row
        self.col = col
        self.width = width
        self.total_rows = total_rows
        self.rect = Rectangle(Point(self.col * self.width, self.row * self.width),
                              Point(((self.col * self.width) + self.width), (self.row * self.width) + self.width))
        darkGrey = color_rgb(26, 26, 26)
        self.state = 0
        self.stateColors = {0: darkGrey, 1: "WHITE", 2: darkGrey, 3: "ORANGE", 4: "CYAN", 5: darkGrey, 6: "Purple"}
        self.stateOutlines = {0: "blaCK", 1: "blaCK", 2: "CYAN", 3: "blaCK", 4: "blaCK", 5: "black", 6: "blaCK"}

        self.neighbors = []
        self.edges = [True, True, True, True]  # UP  #DOWN #LEFT #RIGHT

        self.isDrawn = False
        self.showDebug = False
        self.showTile = False

        self.score = Text(Point((self.col * self.width) + 24, (self.row * self.width) + 8), "inf")
        self.score.setSize(8)
        self.score.setTextColor("grey")

        self.gCostTxt = Text(Point((self.col * self.width) + 8, (self.row * self.width) + 8), "inf")
        self.gCostTxt.setTextColor("grey")
        self.gCostTxt.setSize(8)
        self.fCostTxt = Text(Point((self.col * self.width) + 16, (self.row * self.width) + 22), "0")
        self.fCostTxt.setTextColor("white")
        self.fCostTxt.setSize(12)

    def getPos(self):
        return self.row, self.col

    def draw(self, win):
        self.rect.draw(win)
        self.win = win
        self.isDrawn = True
        self.__updateVisuals()

    def updateState(self, newState: int):
        self.state = newState
        if not (self.win == None):
            self.__updateVisuals()

    def __updateVisuals(self):
        if self.showDebug:
            if not self.isDrawn:
                self.isDrawn = True
                self.rect.draw(self.win)
                #self.win.lower(self.rect.id)
            self.rect.setFill(self.stateColors[self.state])
            self.rect.setOutline(self.stateOutlines[self.state])
        elif self.showTile:
            if (self.state == 1):
                if not self.isDrawn:
                    self.isDrawn = True
                    self.rect.draw(self.win)
                    #self.win.lower(self.rect.id)
                self.rect.setFill(DEFAULT_CONFIG['fill'])
                self.rect.setOutline("white")
        else:
                self.rect.undraw()
                self.isDrawn = False

    def updateNeighbors(self, grid):
        self.neighbors = []
        if (self.row < self.total_rows - 1):
            down = grid[self.row + 1][self.col]
            if not down.getState() == 1: self.neighbors.append(down)
            if down.getState() == 1: self.edges[1] = False
            else: self.edges[1] = True

        if (self.row > 0):
            up = grid[self.row - 1][self.col]
            if not up.getState() == 1: self.neighbors.append(up)
            if up.getState() == 1: self.edges[0] = False
            else: self.edges[0] = True
        if (self.col < self.total_rows - 1):
            right = grid[self.row][self.col + 1]
            if not (right.getState() == 1): self.neighbors.append(right)
            if right.getState() == 1: self.edges[3] = False
            else: self.edges[3] = True
        if (self.col > 0):
            left = grid[self.row][self.col - 1]
            if not left.getState() == 1: self.neighbors.append(left)
            if left.getState() == 1: self.edges[2] = False
            else: self.edges[2] = True
        # Upper left
        # Upper Right
        # Lower Left
        # Lower Right

    def toggleDebug(self, show: bool):
        if not (self.showDebug):
            self.showDebug = True
            self.showTile = False
            self.__updateVisuals()
            self.score.draw(self.win)
            self.gCostTxt.draw(self.win)
            self.fCostTxt.draw(self.win)

            #self.win.lower(self.score.id)
            #self.win.lower(self.gCostTxt.id)
            #self.win.lower(self.fCostTxt.id)
            #self.win.lower(self.rect.id)
        else:
            self.showDebug = False
            self.__updateVisuals()
            self.score.undraw()
            self.gCostTxt.undraw()
            self.fCostTxt.undraw()
    def toggleEditMode(self):
        if not self.showTile:
            self.showTile = True
            self.__updateVisuals()
            if (self.showDebug):
                self.toggleDebug()
        else:
            self.showTile = False
            self.__updateVisuals()


    def getState(self) -> int:
        return self.state

    def getEdges(self) -> [bool, bool, bool, bool]:
        return self.edges

    def setHCostText(self, score):
        self.score.setText(str(score))

    def setGCostText(self, score):
        self.gCostTxt.setText(str(score))

    def setFCostText(self, score):
        self.fCostTxt.setText(str(score))
    def getGridPos(self):
        return (self.row,self.col)
