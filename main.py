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
from game_systems.CandleSprite import Candle
#from Doors import Door

width = 705 + 256
height = 705

offsetX = 1084
offsetY = 700

gw = GraphWin("GAME", width, height,autoflush=False) #This is the window where all the graphics are drawn.
gw.setBackground("black")

inputHandler = InputHandler() #Object that receives input from the window.\

gw.setInputHandler(inputHandler)  # We pass in the input handler to the window, so it can receive input!

player = Player(Point(1700,1200),inputHandler) #Player object that is controller by user.
monster = Monster(1900,1200) #Monster object that chases the player around the map.

sightLine = Line(player.getPos(),monster.getPos())
sightLine.setFill("red")

testLine = Line(player.getPos(),monster.getPos())
testLine.setFill("green")

monsterCollision = Rectangle(Point(0,0),Point(0,0))
monsterCollision.setOutline("RED")

mousePosTxt = Text(Point(100, 75), f"Mouse Pos: {0},{0}")
gridIndexTxt = Text(Point(100, 50), f"Grid Index: {0},{0}")
gridIndexTxt.setTextColor("orange")
mousePosTxt.setTextColor("cyan")
exitZoneDebug = Rectangle(Point((32 * 8),(32*-2)),Point((32 * 10),(32*0)))
exitZoneDebug.setOutline("pink")

doors = []
exitDoor = Door((32 * 9),(32*0), None,player)
normalDoor = Door((32 * 46),(32*34), None,player)
redDoor = Door((32 * 20),(32*9), "red",player)
blueDoor = Door((32 * 29),(32 *36), "blue",player)
greenDoor = Door((32 * 36),(32*11), "green",player)
yellowDoor = Door((64 * 13),(32 *21), "yellow",player)
pinkDoor = Door((32 * 2),(32 *23), "pink",player)
normalDoor2 = Door((49 * 32),(32*21), None,player)
normalDoor3 = Door((38 * 32),(27*32), None,player)
doors.append(redDoor)
doors.append(blueDoor)
doors.append(normalDoor)
doors.append(greenDoor)
doors.append(yellowDoor)
doors.append(exitDoor)
doors.append(pinkDoor)
doors.append(normalDoor2)
doors.append(normalDoor3)

runtimeTxt = Text(Point(400, 25), "")
fpsTxt = Text(Point(400, 50), "")
debugView = False
editView = False

deltaT = -1.0
gridSizeX = 64
grid = []
endTile: TileBase = None
gridSizeY = 64
gridCellSize = 32
startTile: TileBase = None
nearTiles = []

sprites = []
selectedSprite = None
lastTileType = (0,0)
viewShifters = [
                ViewShifter((32 * 43),27*32,player,gw,(1084,700),(1084,370),True),
                ViewShifter((32 * 49),21*32,player,gw,(1084,370),(1084,0),True),
                ViewShifter((32 * 62),21*32,player,gw,(1084,370),(1084,0),True),
                ViewShifter((32 * 36),(32*11),player,gw,(1084,0),(350,0),True),
                ViewShifter((32 * 26),(32*21),player,gw,(350,640),(350,0),True),
                ViewShifter((32 * 20),(32*9),player,gw,(350,0),(0,-300),True),
                ViewShifter((32 * 2),(32*23),player,gw,(0,700),(0,0),True),
                ViewShifter((32 * 19),(32*40),player,gw,(350,640),(0,700),False) #This is the weird sideways one. <--------
                ]

candles = [Candle(1975,1226,True,gw),
           Candle(1923,1190,False,gw),
           Candle(1923,1275,True,gw),
           Candle(1875,1265,False,gw),
           Candle(1875,1200,True,gw),
           Candle(1850,1250,True,gw)]

def main():
    menu() #Calling this opens main menu
    game() #Calling this starts the game loop.
    win()
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
    global offsetY
    global offsetX
    moveCamera(1084,700)
    makeGrid()
    loadWorld()
    game_over = False

    for sprite in sprites:
        if (sprite.getLayer() == 0):
            sprite.draw()

    keys = []

    key_blue = Key(1920, 990, 'blue',player)
    keys.append(key_blue)
    key_red = Key(265, 425, 'red',player)
    keys.append(key_red)
    key_yellow = Key(830, 225, 'yellow',player)
    keys.append(key_yellow)
    key_green = Key(1535, 285, 'green',player)
    keys.append(key_green)
    key_pink = Key(1060, 965, 'pink',player)
    keys.append(key_pink)
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

    for candle in candles:
        candle.draw()

    monster.draw(gw)
    player.draw(gw)

    redDoor.setTiles([grid[9][19],grid[8][19],grid[9][20],grid[8][20]])
    blueDoor.setTiles([grid[35][29],grid[35][28],grid[36][29],grid[36][28]])
    yellowDoor.setTiles([grid[21][25],grid[21][26],grid[20][26],grid[20][25]])
    greenDoor.setTiles([grid[10][36],grid[10][35],grid[11][35],grid[11][36]])
    pinkDoor.setTiles([grid[22][1],grid[23][1],grid[22][2],grid[23][2]])

    exitDoor.setTiles([grid[0][8],grid[0][9]])

    print(len(grid))
    global selectedSprite
    game_over = False
    while not game_over:  # This will run until 'game_over' is False.

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

        for candle in candles:
            candle.update(deltaT)

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


        sx = monster.getPos().x - 16
        sy = monster.getPos().y - 24

        is_hit = circleRect(player.getPos().x, player.getPos().y, 16, sx, sy,30,40)
        if (is_hit):
            player.resetPos()
            offsetX = 1084
            offsetY = 700
            moveCamera(offsetX,offsetY)
        monster.hit(is_hit)

        global monsterCollision
        monsterCollision.undraw()
        if (debugView):
            monsterCollision = Rectangle(Point(sx,sy),Point(sx + 30,sy +40))
            monsterCollision.setOutline("RED")
            monsterCollision.draw(gw)

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
            x = offsetX + cameraVX
            y = offsetY + cameraVY
            if (cameraVX != 0 or cameraVY != 0):
                moveCamera(x,y)

        win_zone = circleRect(player.getPos().x, player.getPos().y, 16, (32*8), (32*-2),64,64)
        if (win_zone):
            game_over = True
        if (gw.closed): #When the window is closed the gameloop finishes
            game_over = True
            

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
    if (rayDir[0] == 0 or rayDir[1] == 0):
        return

    rayUnitStepSize = [ sqrt(1 + (rayDir[1]/rayDir[0]) * (rayDir[1]/rayDir[0])),
                        sqrt(1 + (rayDir[0]/rayDir[1]) * (rayDir[0]/rayDir[1])) ]

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
def moveCamera(xPos,yPos):
    global offsetY
    global offsetX
    offsetX = xPos
    offsetY = yPos
    gw.setCoords(offsetX, height + offsetY, width + offsetX, offsetY)
    gridIndexTxt.move(((width + offsetX)-gridIndexTxt.getAnchor().x) - width +80,((height+ offsetY)-gridIndexTxt.getAnchor().y)-height+100)
    mousePosTxt.move(((width + offsetX)-mousePosTxt.getAnchor().x) - width +110,((height+ offsetY)-mousePosTxt.getAnchor().y)-height+125)
    fpsTxt.move(((width + offsetX)-fpsTxt.getAnchor().x) - width/2,((height+ offsetY)-fpsTxt.getAnchor().y)-height+25)
    runtimeTxt.move(((width + offsetX)-runtimeTxt.getAnchor().x) - width/2,((height+ offsetY)-runtimeTxt.getAnchor().y)-height+50)


def toggleDebugView(activate:bool):
    global debugView
    global grid
    if (debugView == activate):
        return
    debugView = activate

    if not (debugView):

        mousePosTxt.undraw()

        runtimeTxt.undraw()
        fpsTxt.undraw()
        gridIndexTxt.undraw()
        exitZoneDebug.undraw()
        for i in viewShifters:
            i.undraw()
    else:
        mousePosTxt.draw(gw)
        runtimeTxt.draw(gw)
        fpsTxt.draw(gw)
        gridIndexTxt.draw(gw)
        exitZoneDebug.draw(gw)
        for i in viewShifters:
            i.draw()

    for row in grid:
        for tile in row:
            tile.toggleEditMode()
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
def win():
    if (gw.closed):
        return
    moveCamera(0,0)
    overlay = Rectangle(Point(0, 0), Point(961, 705))
    overlay.setFill('black')
    overlay.setOutline('black')
    background = Image(Point(961/2, 705/2), "sprites/ghost/ghost1.png")
    message = Text(Point(480, 200), 'YOU ESCAPED!')
    message2 = Text(Point(480, 250), 'THANKS FOR PLAYING!')
    message.setSize(32)
    message2.setSize(18)
    message.setTextColor('white')
    message.setStyle("bold")
    message2.setTextColor('white')
    message2.setStyle('italic')

    overlay.draw(gw)
    background.draw(gw)
    message.draw(gw)
    message2.draw(gw)
    update()
    time.sleep(5)



def mouseToWorld():
    pos = inputHandler.getMousePos()
    return gw.toWorld(pos[0],pos[1])

inputHandler.setNumberKeyFunc(numberKeyPressed)
inputHandler.setKeyPressedFunc(keyPressed)
inputHandler.setRMBPressedFunc(rmbPressed)

main()
