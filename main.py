#Rordy
#Tyler
#Add your names here!!
import math
import random
import time

#import winsound #winsound.PlaySound("ui_menu_button_beep_13", winsound.SND_FILENAME | winsound.SND_ASYNC)
import graphics
from Monster import *
from Player import Player
from InputHandler import *
from graphics import *
from time import *
from tilebase import *
from queue import PriorityQueue

width = 512
height = 512

gw = GraphWin("GAME", width, height,autoflush=True) #This is the window where all the grapics are drawn.

inputHandler = InputHandler() #Object that recieves input from the window.

player = Player(Point(width/2,height/2),inputHandler) #Player object that is controller by user.
monster = Monster() #Monster object that chases the player around the map.

mousePosTxt = Text(Point(100, 25), f"Mouse Pos: {0},{0}")
gridIndexTxt = Text(Point(100, 50), f"Grid Index: {0},{0}")
gridIndexTxt.setTextColor("orange")
mousePosTxt.setTextColor("cyan")


runtimeTxt = Text(Point(400, 25), "")
fpsTxt = Text(Point(400, 50), "")

deltaT = -1.0
gridSize = 32
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

    monster.draw(gw)
    player.draw(gw)
    print(len(grid))

    cx = 0
    cy = 0

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

        cx = player.getPos().x
        cy =player.getPos().y

        sx = monster.getPos().x - 57/2
        sy = monster.getPos().y - 57/2

        col = inputHandler.getMousePos()[0] // gridSize
        row = inputHandler.getMousePos()[1] // gridSize
        gridIndexTxt.setText(f"Grid Index: [{row}][{col}]")
        if (gw.checkMouse()):
            grid[row][col].updateState(1)
            grid[row][col].updateNeighbors(grid)
            grid[row][col].printNeighbors()


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

def circleRect(cx,cy,r,rx,ry,rw,rh):
    testX = cx
    testY = cy

    if (cx < rx): testX = rx
    elif (cx > (rx +rw)): testX = rx+rw

    if (cy < ry): testY = ry
    elif (cy>(ry+rh)): testY = ry + rh

    distX = cx-testX
    distY = cy-testY
    distance = sqrt((distX*distX) + (distY*distY))

    return (distance <= r)

def makeGrid():
    rows = int(height/gridSize)
    columns = int(width/gridSize)
    count = 0
    for row in range(rows):
        row_list = []
        for col in range(columns):
            tile = TileBase(row,col,gridSize,rows)
            row_list.append(tile)
            count +=1
        grid.append(row_list)

    global endTile
    endTile = grid[1][1]
    print(f'Grid Size: {count}')

def updateEndPos():
    global startTile
    global endTile
    row = int(player.getPos().x // gridSize)
    col = int(player.getPos().y // gridSize)

    startRow = int((monster.getPos().y - 16) // gridSize)
    startCol = int((monster.getPos().x )// gridSize)

    currentStart = grid[startRow][startCol]
    if (startTile != None and startTile != currentStart):
        startTile.updateState(0)
        startTile = currentStart
        startTile.updateState(3)

    else: startTile = currentStart


    currentTile = grid[col][row]
    if (endTile == None or startTile == None):
        return

    if not (endTile == currentTile):
        endTile.updateState(0)
        endTile = currentTile
        endTile.updateState(4)
        pathfind(grid, startTile, endTile)


def heuristic(start:Point,end:Point):
    return (abs(end[0] - start[0]) + abs(end[1]-start[1]))

def reconstruct_path(cameFrom,current):
    count = 0
    while current in cameFrom:
        count += 1
        current = cameFrom[current]
        current.updateState(6)
    print(count)
def pathfind(grid,start:TileBase,end:TileBase):
    print('Calling A*')

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
            temp_g_score = g_score[current] + 0

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