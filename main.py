#Rordy 20/11/23
#Tyler
#Add your names here!!

import graphics
from Monster import *
from Player import Player
from InputHandler import *
from graphics import *
from time import *
from tilebase import *
from queue import PriorityQueue
from Collisions import *

width = 705
height = 705

gw = GraphWin("GAME", width, height,autoflush=False) #This is the window where all the grapics are drawn.

inputHandler = InputHandler() #Object that recieves input from the window.

player = Player(Point(width/2,height/2),inputHandler) #Player object that is controller by user.
monster = Monster() #Monster object that chases the player around the map.

sightLine = Line(player.getPos(),monster.getPos())
sightLine.setFill("red")

testLine = Line(player.getPos(),monster.getPos())
testLine.setFill("green")
testRect = Rectangle(Point(400,400),Point(464,464))
testRect.setFill("white")
testRect.draw(gw)

mousePosTxt = Text(Point(100, 25), f"Mouse Pos: {0},{0}")
gridIndexTxt = Text(Point(100, 50), f"Grid Index: {0},{0}")
rayTxt = Text(Point(100, 100),f"Ray Unit Step Size: {0},{0}")
rayTxt.setTextColor("lightgreen")
gridIndexTxt.setTextColor("orange")
mousePosTxt.setTextColor("cyan")


runtimeTxt = Text(Point(400, 25), "")
fpsTxt = Text(Point(400, 50), "")

deltaT = -1.0
gridSizeX = 22
gridSizeY = 22
gridCellSize = 32
grid = []
endTile: TileBase = None
startTile: TileBase = None

testRect = Rectangle(Point(0,0),Point(50,50))

def main():
    global gw
    global deltaT
    gw.setBackground("black")
    gw.setInputHandler(inputHandler) #We pass in the input handler to the window so it can recieve input!

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            grid[row][col].draw(gw)


    mousePosTxt.draw(gw)
    fpsTxt.setTextColor("yellow")

    runtimeTxt.setTextColor("cyan")
    runtimeTxt.draw(gw)
    fpsTxt.draw(gw)
    gridIndexTxt.draw(gw)
    rayTxt.draw(gw)

    monster.draw(gw)
    player.draw(gw)

    print(len(grid))

    sx = 57
    sy = 57
    sw = 57
    sh = 57

    done = False
    while not done:  # This will run until 'done' is False.
        currentTime = time.time()

        monster.setTargetPos(player.getPos().x,player.getPos().y)
        monster.update(deltaT)
        player.update(deltaT)
        updateEndPos()
        global sightLine
        sightLine.undraw()
        sightLine = Line(player.getPos(),monster.getPos())

        los = True
        """
        for ir, row in enumerate(grid):
            for ic, tile in enumerate(row):
                if (lineRect(monster.getPos().x,
                             monster.getPos().y,
                             player.getPos().x,
                             player.getPos().y,ir * 32,ic*32,32,32, tile.getEdges())):
                    los = False
                    break
        """
        rayIntersection = [0,0]
      #  if (targetTileFound):
            #rayIntersection = rayStart + rayDir * rayDist

        """
        if lineRect(monster.getPos().x,
                             monster.getPos().y,
                             player.getPos().x,
                             player.getPos().y,400,400,64,64, (True,True,True,True)):

            sightLine.setFill("cyan")
        else:
            sightLine.setFill("red")
        sightLine.draw(gw)
        """

        if (dda()):
            sightLine.setFill("red")
        else:
            sightLine.setFill("cyan")
        sightLine.draw(gw)

        if gw.checkKey() == 'v':
            print("Showing grid: ")

            for row in grid:
                for tile in row:
                    tile.toggleDebug(True)


        cx = player.getPos().x
        cy = player.getPos().y

        sx = monster.getPos().x - 57/2
        sy = monster.getPos().y - 57/2

        col = inputHandler.getMousePos()[0] // gridCellSize
        if not (col < gridSizeX):
            col = 0

        row = inputHandler.getMousePos()[1] // gridCellSize
        if not (row < gridSizeY):
            row = 0
        gridIndexTxt.setText(f"Grid Index: [{row}][{col}]")
        selectedTile: TileBase = grid[row][col]
        if (inputHandler.getMousePressed()):
            if (selectedTile.getState() == 0 or selectedTile.getState() == 5):
                selectedTile.updateState(1)
                #Grid updated
                for row in grid:
                    for tile in row:
                        tile.updateNeighbors(grid)
            if (selectedTile.getState() == 1 and gw.checkMouse()):
                print(selectedTile.getEdges())


        monster.hit(circleRect(cx, cy, 25, sx, sy,57,57))

        runTime = (deltaT*1000).__round__(1)
        mousePosTxt.setText(f"Mouse Pos: {inputHandler.getMousePos()}")
        runtimeTxt.setText(f"Run Time: {str(runTime)}ms")
        fpsTxt.setText(f"FPS: {str((1000/runTime).__round__())}")

        time.sleep((0.1/1000))   #Calling this redraws everything on screen.
        gw.update()

        deltaT = time.time() - currentTime
        if (gw.closed): #When the window is closed the gameloop finishes
            done = True
def makeGrid():
    rows = gridSizeX
    columns = gridSizeY
    count = 0
    for row in range(rows):
        row_list = []
        for col in range(columns):
            tile = TileBase(row,col,gridCellSize,rows)
            row_list.append(tile)
            count +=1
        grid.append(row_list)

    global endTile
    endTile = grid[1][1]
    print(f'Grid Size: {count}')

def updateEndPos():
    global startTile
    global endTile
    targetRow = int(player.getPos().x // gridCellSize)
    targetCol = int(player.getPos().y // gridCellSize)

    startRow = int((monster.getPos().y - 16) // gridCellSize)
    startCol = int((monster.getPos().x - 16 )// gridCellSize)

    currentStart = grid[startRow][startCol]
    currentTarget = grid[targetCol][targetRow]

    if (currentStart.getState() == 1 or currentTarget.getState() == 1):
        return

    if (startTile != None and startTile != currentStart):
        startTile.updateState(0)
        startTile = currentStart
        startTile.updateState(3)
    else: startTile = currentStart

    if (endTile == None or startTile == None):
        return

    if not (endTile == currentTarget):
        endTile.updateState(0)
        endTile = currentTarget
        endTile.updateState(4)
        pathfind(grid, startTile, endTile)


def heuristic(start:Point,end:Point):
    return (abs(end[0] - start[0]) + abs(end[1]-start[1]))

def dda():
    rayStart = [monster.getPos().x, monster.getPos().y]
    rayDir = monster.getPlayerDir()

    rayUnitStepSize = [ sqrt(1 + (rayDir[1]/rayDir[0]) * (rayDir[1]/rayDir[0])),
                        sqrt(1 + (rayDir[0]/rayDir[1]) * (rayDir[0]/rayDir[1])) ]
    rayTxt.setText(f"Ray Unit Step Size: {rayUnitStepSize[0].__round__(2)},{rayUnitStepSize[1].__round__(2)}")

    mapCheck = [int(monster.getPos().x // gridCellSize), int(monster.getPos().y // gridCellSize)]
    rayLength1D = [0.0, 0.0]
    step = [1, 1]

    if rayDir[0] < 0:
        step[0] = -1
        rayLength1D[0] = (rayStart[0] - (float(mapCheck[0] * gridCellSize))) / gridCellSize * rayUnitStepSize[0]
    else:
        step[0] = 1
        rayLength1D[0] = ((float(mapCheck[0] + 1) * gridCellSize) - rayStart[0]) / gridCellSize * rayUnitStepSize[0]

    if rayDir[1] < 0:
        rayLength1D[1] = (rayStart[1] - (float(mapCheck[1] * gridCellSize))) / gridCellSize * rayUnitStepSize[1]
        step[1] = -1
    else:
        rayLength1D[1] = (float((mapCheck[1] + 1) * gridCellSize) - rayStart[1]) / gridCellSize * rayUnitStepSize[1]
        step[1] = 1

    targetTileFound = False
    maxRayDist = 100.0
    rayDist = 0.0

    global testLine
    testLine.undraw()
    testLine = Line(Point(0,1), Point(monster.getPos().x + rayDir[0], monster.getPos().y +rayDir[1]))
    testLine.setFill("green")
    testLine.draw(gw)

    for row in grid:
        for tile in row:
            if not tile.getState() == (1):
                tile.updateState(0)

    while (not targetTileFound) and rayDist < maxRayDist:
        if (rayLength1D[0] < rayLength1D[1]):
            mapCheck[0] += step[0]
            rayDist = rayLength1D[0]
            rayLength1D[0] += rayUnitStepSize[0]
        else:
            mapCheck[1] += step[1]
            rayDist = rayLength1D[1]
            rayLength1D[1] += rayUnitStepSize[1]



        if (mapCheck[0] >= 0 and mapCheck[0] < gridSizeX) and (mapCheck[1] >= 0 and mapCheck[1] < gridSizeY):
            if not (grid[mapCheck[1]][mapCheck[0]].getState() == 1):
                grid[mapCheck[1]][mapCheck[0]].updateState(2)

            if (grid[mapCheck[1]][mapCheck[0]].getState() == 1):
                targetTileFound = True


    return targetTileFound

def reconstruct_path(cameFrom,current):
    count = 0
    path = []
    while current in cameFrom:
        count += 1
        path.insert(0,current.getPos())
        current = cameFrom[current]
        current.updateState(6)
    monster.updatePath(path)
def pathfind(grid,start:TileBase,end:TileBase):
    return
    for row in grid:
        for tile in row:
            if (tile.getState() == (2 or 3)):
                tile.updateState(0)
            if (tile.getState() == (6)):
                tile.updateState(0)
            tile.updateNeighbors(grid)
    count = 0
    open_set = PriorityQueue()

    open_set.put((0, count, start))
    open_set_hash = {start}

    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.getPos(), end.getPos())
    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            current.updateState(4)
            reconstruct_path(came_from,end)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current

                h_score = heuristic(end.getPos(),neighbor.getPos())
                neighbor.setHCostText(h_score)

                g_score[neighbor] = temp_g_score
                neighbor.setGCostText(temp_g_score)

                f_score[neighbor] = h_score + temp_g_score
                neighbor.setFCostText(f_score[neighbor])

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.updateState(5)

        if current != start:
            current.updateState(2)
    return False

makeGrid()
main() #Calling this starts the game loop.