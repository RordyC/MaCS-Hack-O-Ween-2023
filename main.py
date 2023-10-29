#Rordy 20/11/23
#Tyler
#Add your names here!!
import random

import graphics
from characters.Monster import *
from characters.Player import Player
from game_systems.ViewShifter import ViewShifter
from Door import Door
from InputHandler import *
from graphics import *
from time import *
from tilebase import *
from queue import PriorityQueue
from Collisions import *
from game_systems.WorldSprite import WorldSprite
import pickle
from Key import Key
#from Doors import Door

width = 705 + 256
height = 705

gw = GraphWin("GAME", width, height,autoflush=False) #This is the window where all the graphics are drawn.
gw.setBackground("black")

inputHandler = InputHandler() #Object that receives input from the window.\

gw.setInputHandler(inputHandler)  # We pass in the input handler to the window, so it can receive input!

player = Player(Point(width/2,height/2),inputHandler) #Player object that is controller by user.
monster = Monster() #Monster object that chases the player around the map.

sightLine = Line(player.getPos(),monster.getPos())
sightLine.setFill("red")

testLine = Line(player.getPos(),monster.getPos())
testLine.setFill("green")
mousePosTxt = Text(Point(100, 75), f"Mouse Pos: {0},{0}")
gridIndexTxt = Text(Point(100, 50), f"Grid Index: {0},{0}")
rayTxt = Text(Point(100, 100),f"Ray Unit Step Size: {0},{0}")
rayTxt.setTextColor("lightgreen")
gridIndexTxt.setTextColor("orange")
mousePosTxt.setTextColor("cyan")

doors = []
redDoor = Door((64 * 5),64, "red",player)
blueDoor = Door((64 * 13),64 *11, "blue",player)
doors.append(redDoor)
doors.append(blueDoor)

runtimeTxt = Text(Point(400, 25), "")
fpsTxt = Text(Point(400, 50), "")
debugView = False
editView = False

deltaT = -1.0
gridSizeX = 64
gridSizeY = 64
gridCellSize = 32
grid = []
endTile: TileBase = None
startTile: TileBase = None
nearTiles = []

sprites = []
selectedSprite = None
lastTileType = (0,0)
viewShifters = [ViewShifter((64 * 5),64,player,gw,(0,0),(0,-200))]


def main():
    menu() #Calling this opens main menu
    game() #Calling this starts the game loop.
def menu():
    # all background info
    white_background = Rectangle(Point(0, 0), Point(961, 705))
    white_background.setFill('black')
    white_background.draw(gw)

    # Title 
    titleLabel = Text(Point(480, 100), 'GHOUL ESCAPE')
    titleLabel.setSize(28)
    titleLabel.setTextColor('orange')
    titleLabel.setStyle('bold italic')

    # Start button
    startLabel = Text(Point(480, 325), 'Start Game')
    startLabel.setSize(20)
    startLabel.setTextColor('white')
    startLabel.setStyle('bold italic')

    startButton = Rectangle(Point(353, 300), Point(607, 350))
    #startButton.setFill('lightgreen')
    startButton.setOutline('orange')

    # Quit button
    quitLabel = Text(Point( 480, 425), 'Exit To Desktop')
    quitLabel.setSize(20)
    quitLabel.setTextColor('white')
    quitLabel.setStyle('bold italic')

    quitButton = Rectangle(Point(353, 400), Point(607, 450))
    #quitButton.setFill('brown')
    quitButton.setOutline('red')
    
    # Draws Menu
    #menuBackground.draw(gw)
    titleLabel.draw(gw)
    startButton.draw(gw)
    startLabel.draw(gw)
    quitButton.draw(gw)
    quitLabel.draw(gw)
    while True:
            click_point = gw.checkMouse()
            if click_point:
                if 353 < click_point.getX() < 607:
                    if 300 < click_point.getY() < 350:
                        break
                    elif 400 < click_point.getY() < 450:
                        gw.close()
    # Undraws menu and pauses for (1) second 
    for item in gw.items[:]:
        item.undraw()
    gw.update()                    
    #sleep(1)
def drawWorld():
    pass
def game():
    global gw
    global deltaT
    global sprites

    makeGrid()
    loadWorld()
    game_over = False

    offsetX = 0
    offsetY = 0
    gw.setCoords(offsetX,height + offsetY,width + offsetX,offsetY)

    for sprite in sprites:
        if (sprite.getLayer() == 0):
            sprite.draw()

    image_paths = ["small_button.png", "sprites/angry_head.png", "keycard_red.png"]

# Start with the first image
    current_image_index = 0
    current_image = Image(Point(200, 200), image_paths[current_image_index])
    current_image.draw(gw)

# Time delay in seconds between image changes
    image_delay = 100.0  # Change this to your desired delay

    keys = []

    key_blue = Key(505, 636, 'blue',player)
    keys.append(key_blue)
    key_red = Key(435, 435, 'red',player)
    keys.append(key_red)
    key_yellow = Key(550, 636, 'yellow',player)
    keys.append(key_yellow)
    key_green = Key(400, 435, 'green',player)
    keys.append(key_green)
    for key in keys:
        key.draw(gw)  

    for door in doors:
        door.draw(gw)

    for sprite in sprites:
        if (sprite.getLayer() == 1):
            sprite.draw()
    for sprite in sprites:
        if (sprite.getLayer() == 2):
            sprite.draw()

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            grid[row][col].draw(gw)


    fpsTxt.setTextColor("yellow")

    runtimeTxt.setTextColor("cyan")

    monster.draw(gw)
    player.draw(gw)

    redDoor.setTiles([grid[1][10],grid[1][9],grid[2][10],grid[2][9]])
    blueDoor.setTiles([grid[21][25],grid[21][26],grid[22][26],grid[22][25]])
    print(len(grid))
    global selectedSprite
    game_over = False
    while not game_over:  # This will run until 'done' is False.

        currentTime = time.time()

        monster.setTargetPos(player.getPos().x,player.getPos().y)
        monster.update(deltaT)

        player.update(deltaT)
        player.setCollisionTiles(nearTiles)

        for door in doors:
            door.update(deltaT)

        for i in viewShifters:
            i.update()
        updateEndPos()

        for key in keys:
            key.update()

        gridEditing()

        global sightLine
        global debugView
        sightLine.undraw()
        if (debugView):
            sightLine = Line(player.getPos(), monster.getPos())
            sightLine.draw(gw)

        if (checkLineOfSight(monster.getPos().x,monster.getPos().y,monster.getPlayerDir(),monster.getPlayerDist())):
            sightLine.setFill("red")
            monster.updateLineOfSight(False)
        else:
            sightLine.setFill("cyan")
            monster.updateLineOfSight(True)


        if (inputHandler.getMousePressed() and editView and selectedSprite == None):
            print("!")
            closestSprite = None
            closestDist = math.inf

            for sprite in sprites:
                print("b")
                currentDist = (((mouseToWorld()[0] - sprite.getGrabPointPos().x)*(mouseToWorld()[0] - sprite.getGrabPointPos().x)) \
                              + (mouseToWorld()[1] - sprite.getGrabPointPos().y)*(mouseToWorld()[1] - sprite.getGrabPointPos().y))
                if ((abs(currentDist) < closestDist)and currentDist < 256):
                    closestDist = currentDist
                    closestSprite = sprite
            print(closestSprite)
            selectedSprite = closestSprite

        global lastTileType
        if (inputHandler.getMousePressed() == False and selectedSprite != None):
            print(":(")
            lastTileType = selectedSprite.getType()
            selectedSprite = None

        if (selectedSprite != None):
            selectedSprite.setPos((mouseToWorld()[0]//gridCellSize) * gridCellSize,(mouseToWorld()[1]//gridCellSize) * gridCellSize)

        if gw.checkKey() == 'i':
            saveWorld()

        sx = monster.getPos().x - 57/2
        sy = monster.getPos().y - 57/2

        monster.hit(circleRect(player.getPos().x, player.getPos().y, 16, sx, sy,57,57))

        runTime = (deltaT*1000).__round__(1)
        mousePosTxt.setText(f"Mouse Pos: {mouseToWorld()[0].__round__(1),mouseToWorld()[1].__round__(1)}")
        runtimeTxt.setText(f"Run Time: {str(runTime)}ms")
        fpsTxt.setText(f"FPS: {str((1000/runTime).__round__())}")

        time.sleep((0.1/1000))   #Calling this redraws everything on screen.
        gw.update()

        deltaT = time.time() - currentTime

        if (debugView):
            cameraVX = inputHandler.getArrowXAxis() * 1024 * deltaT
            cameraVY = inputHandler.getArrowYAxis() * 1024 * deltaT
            offsetX = offsetX + cameraVX
            offsetY = offsetY + cameraVY
            if (cameraVX != 0 or cameraVY != 0):
                gw.setCoords(offsetX, height + offsetY, width + offsetX, offsetY)

        current_image.undraw()

        current_image_index = (current_image_index + 1) % len(image_paths)
        current_image = Image(Point(200, 200), image_paths[current_image_index])
        current_image.draw(gw)

        #youWinScreen()

        if (gw.closed): #When the window is closed the gameloop finishes
            done = True
            

def makeGrid():
    rows = gridSizeX
    columns = gridSizeY
    count = 0
    with open('save_data/grid_data','rb') as f:
        gridData = pickle.load(f)
    for row in range(rows):
        row_list = []
        for col in range(columns):
            tile = TileBase(row,col,gridCellSize,rows)
            if (row < len(gridData)):
                if col < len(gridData[row]):
                    tile.updateState(gridData[row][col])
            row_list.append(tile)
            count +=1
        grid.append(row_list)

    global endTile
    endTile = grid[1][1]
    print(f'Grid Size: {count}')

def gridEditing():
    col = int(mouseToWorld()[0] // gridCellSize)
    if not (col < gridSizeX):
        col = 0

    row = int(mouseToWorld()[1] // gridCellSize)
    if not (row < gridSizeY):
        row = 0
    gridIndexTxt.setText(f"Grid Index: [{row}][{col}]")
    selectedTile: TileBase = grid[row][col]
    if (inputHandler.getMousePressed() and debugView):
        if (selectedTile.getState() == 0 or selectedTile.getState() == 5):
            selectedTile.updateState(1)
            # Grid updated
            for row in grid:
                for tile in row:
                    tile.updateNeighbors(grid)
    if (inputHandler.getRMB()and debugView):
        if (selectedTile.getState() == 1):
            selectedTile.updateState(0)
            # Grid updated
            for row in grid:
                for tile in row:
                    tile.updateNeighbors(grid)
                    
def updatePlayerCollision(row:int,col:int):
    global nearTiles
    nearTiles = []

    for r in range(0,4):
        for c in range(0,4):
            rt = max(min(row - 2 + r,gridSizeY -1), 0)
            ct = max(min(col - 2 + c,gridSizeX -1), 0)
            tile = grid[rt][ct]
            if (tile.getState() == 1):
                nearTiles.append(tile)
def updateEndPos():
    global startTile
    global endTile
    targetRow = int(player.getPos().y // gridCellSize)
    targetCol = int(player.getPos().x // gridCellSize)


    startRow = int((monster.getPos().y - gridCellSize/2) // gridCellSize)
    startCol = int((monster.getPos().x - gridCellSize/2) // gridCellSize)

    currentStart = grid[startRow][startCol]
    currentTarget = grid[targetRow][targetCol]
    updatePlayerCollision(targetRow, targetCol)
    if (currentTarget.getState() == 1):
        return
    if (currentStart.getState() != 1):
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

def checkLineOfSight(startX,startY,rayDirection:[float],distance):
    rayStart = [startX,startY]
    rayDir = rayDirection

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
    maxRayDist = distance/gridCellSize - 1
    rayDist = 0.0

    '''
    for row in grid:
        for tile in row:
            if not tile.getState() == (1):
                tile.updateState(0)
    '''
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
    if len(path) > 0:
        monster.updatePath(path)
def pathfind(grid,start:TileBase,end:TileBase):
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
            reconstruct_path(came_from, end)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current

                h_score = heuristic(end.getPos(), neighbor.getPos())
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
def saveWorld():
    print("Saving...")
    gridData = []
    for row in grid:
        rowData = []
        for col in row:
            if (col.getState() == 1):
                rowData.append(1)
            else:
                rowData.append(0)
        gridData.append(rowData)
    spriteData = []
    for s in sprites:
        spriteData.append(s.getData())
    print(gridData)

    with open('save_data/grid_data', 'wb') as f:
        pickle.dump(gridData, f)
    with open('save_data/sprite_data','wb') as f:
        pickle.dump(spriteData,f)
def loadWorld():
    print("Loading World Sprites...")
    global sprites

    with open('save_data/sprite_data','rb') as f:
        sprites = [WorldSprite(s[0],s[1],s[2],s[3],s[4],gw) for s in pickle.load(f)]

def toggleDebugView(activate:bool):
    global debugView
    if (debugView == activate):
        return
    debugView = activate

    if not (debugView):

        mousePosTxt.undraw()

        runtimeTxt.undraw()
        fpsTxt.undraw()
        gridIndexTxt.undraw()
        rayTxt.undraw()
        for i in viewShifters:
            i.undraw()
    else:
        mousePosTxt.draw(gw)
        runtimeTxt.draw(gw)
        fpsTxt.draw(gw)
        gridIndexTxt.draw(gw)
        rayTxt.draw(gw)
        for i in viewShifters:
            i.draw()
def toggleWorldEdit(activate:bool):
    global editView
    global selectedSprite
    if (editView == activate):
        return

    editView = activate
    global sprites
    for s in sprites:
         s.editMode(activate)
    if not editView:
        selectedSprite = None
def numberKeyPressed(number:str):
    global selectedSprite
    if (selectedSprite != None):
        if (number == "1"):
            selectedSprite.updateType(1)
        elif (number== "3"):
            selectedSprite.toggleLayer()
        else:
            selectedSprite.updateVariation(1)
def keyPressed(key:str):
    if (key == 'v'):
        toggleWorldEdit(False)
        if (debugView):
            toggleDebugView(False)
        else:
            toggleDebugView(True)
    if (key == 'i'):
        saveWorld()
    if (key == 'b'):
        if (editView):
            toggleWorldEdit(False)
        else:
            toggleWorldEdit(True)
        toggleDebugView(False)
    if (key == 'g'):
        print("Showing grid: ")
        for row in grid:
            for tile in row:
                tile.toggleDebug(True)
def rmbPressed():
    if (selectedSprite == None):
        if (editView):
             newSprite = WorldSprite(mouseToWorld()[0]//gridCellSize * gridCellSize,mouseToWorld()[1]//gridCellSize * gridCellSize,lastTileType[0],lastTileType[1],0,gw)
             newSprite.redraw()
             sprites.append(newSprite)
    else:
        selectedSprite.toggleLayer()
def youWinScreen():
    overlay = Rectangle(Point(0, 0), Point(961, 705))
    overlay.setFill('black')
    overlay.setOutline('black')
    background = Image(Point(961/2, 705/2), "background2.png")
    message = Text(Point(480, 100), 'YOU WIN!\nTHANKS 4 PLAYING!')
    message.setSize(24)
    message.setTextColor('red')
    message.setStyle('bold italic')
    overlay.draw(gw)
    background.draw(gw)
    message.draw(gw)


def mouseToWorld():
    pos = inputHandler.getMousePos()
    return gw.toWorld(pos[0],pos[1])

inputHandler.setNumberKeyFunc(numberKeyPressed)
inputHandler.setKeyPressedFunc(keyPressed)
inputHandler.setRMBPressedFunc(rmbPressed)

main()
