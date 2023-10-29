#Rordy 20/11/23
#Tyler
#Add your names here!!
import random

import graphics
from Monster import *
from Player import Player
from Door import Door
from InputHandler import *
from graphics import *
from time import *
from tilebase import *
from queue import PriorityQueue
from Collisions import *
from WorldSprite import WorldSprite
import pickle
from Key import Key
#from Doors import Door

width = 705 + 256
height = 705

gw = GraphWin("GAME", width, height,autoflush=False) #This is the window where all the graphics are drawn.
gw.setBackground("black")

inputHandler = InputHandler() #Object that receives input from the window.
gw.setInputHandler(inputHandler)  # We pass in the input handler to the window, so it can receive input!

player = Player(Point(width/2,height/2),inputHandler) #Player object that is controller by user.
monster = Monster() #Monster object that chases the player around the map.

sightLine = Line(player.getPos(),monster.getPos())
sightLine.setFill("red")

testLine = Line(player.getPos(),monster.getPos())
testLine.setFill("green")

mousePosTxt = Text(Point(100, 25), f"Mouse Pos: {0},{0}")
gridIndexTxt = Text(Point(100, 50), f"Grid Index: {0},{0}")
rayTxt = Text(Point(100, 100),f"Ray Unit Step Size: {0},{0}")
rayTxt.setTextColor("lightgreen")
gridIndexTxt.setTextColor("orange")
mousePosTxt.setTextColor("cyan")

testDoor = Door((64 * 5) + 2,64, )


runtimeTxt = Text(Point(400, 25), "")
fpsTxt = Text(Point(400, 50), "")
debugView = False
editView = False

deltaT = -1.0
gridSizeX = 32
gridSizeY = 32
gridCellSize = 32
grid = []
endTile: TileBase = None
startTile: TileBase = None
nearTiles = []



def main():
    menu() #Calling this opens main menu
    game() #Calling this starts the game loop.
def menu():
    # all background info
    white_background = Rectangle(Point(0, 0), Point(961, 705))
    white_background.setFill('white')
    white_background.draw(gw)
    menuBackground = Image(Point(480, 352), 'blood.png')

    # Title 
    titleLabel = Text(Point(480, 100), 'THE GAME')
    titleLabel.setSize(28)
    titleLabel.setTextColor('black')
    titleLabel.setStyle('bold italic')

    # Start button
    startLabel = Text(Point(480, 325), 'Start Game')
    startLabel.setSize(20)
    startLabel.setTextColor('white')
    startLabel.setStyle('bold italic')

    startButton = Rectangle(Point(353, 300), Point(607, 350))
    startButton.setFill('lightgreen')

    # Quit button
    quitLabel = Text(Point( 480, 425), 'Exit To Desktop')
    quitLabel.setSize(20)
    quitLabel.setTextColor('white')
    quitLabel.setStyle('bold italic')

    quitButton = Rectangle(Point(353, 400), Point(607, 450))
    quitButton.setFill('brown')
    
    # Draws Menu
    menuBackground.draw(gw)
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
    sleep(1)               



def game():
    global gw
    global deltaT
   
    makeGrid()
    game_over = False

    #gw.setCoords(0+ 500,705,705 + 500,0)
    walls = []
    floors = []
    image_paths = ["small_button.png", "angry_head.png", "keycard_red.png"]

# Start with the first image
    current_image_index = 0
    current_image = Image(Point(200, 200), image_paths[current_image_index])
    current_image.draw(gw)

# Time delay in seconds between image changes
    image_delay = 1.0  # Change this to your desired delay
    
    # current_image = player_images[current_image_index]
    # key drawingsdda
    keys = []
    
    #key1 = Key(Point(690, 85), 'keycard_red.png')
    #key2 = Circle(Point(200, 200), 10)
    #key2.setFill('green')
    key3 = Key(Point(505, 636), 'keycard_blue.png')
    keys.extend([key3])
    keys_data = [
                {'color':'blue','image':key3, 'collected':False}]
    for key in keys:
        key.draw(gw)  

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            grid[row][col].draw(gw)
    for i in range(5):
        wall = Image(Point(64 * i, 64), "sprites/wall.png")
        wall.draw(gw)
        walls.append(wall)
    for i in range(5):
        wall = Image(Point(64 * i, 128), "sprites/floor.png")
        wall.draw(gw)
        walls.append(wall)
    
    testDoor.draw(gw)
    mousePosTxt.draw(gw)
    fpsTxt.setTextColor("yellow")

    runtimeTxt.setTextColor("cyan")
    runtimeTxt.draw(gw)
    fpsTxt.draw(gw)
    gridIndexTxt.draw(gw)
    rayTxt.draw(gw)

    monster.draw(gw)
    player.draw(gw)
    sprite = WorldSprite(500,500,"wall",gw)
    sprite.draw()
    testDoor.setTiles([grid[1][10],grid[1][9],grid[2][10],grid[2][9]])

    print(len(grid))

    game_over = False
    while not game_over:  # This will run until 'done' is False.

        currentTime = time.time()

        monster.setTargetPos(player.getPos().x,player.getPos().y)
        monster.update(deltaT)
        player.update(deltaT)
        player.setCollisionTiles(nearTiles)
        #testDoor.update(deltaT, key_data['collected'])
        testDoor.setPlayerCoords(player.getPos().x,player.getPos().y)
        updateEndPos()

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


        if gw.checkKey() == 'v':
            toggleDebugView()
            print("Showing grid: ")
            for row in grid:
                for tile in row:
                    tile.toggleDebug(True)

        if pointCircle(player.getPos().x, player.getPos().y, testDoor._Door__posX + 32, testDoor._Door__posY + 32, 69):
            testDoor.openDoor()

        if gw.checkKey() == 'i':
            saveWorld()

        sx = monster.getPos().x - 57/2
        sy = monster.getPos().y - 57/2

        monster.hit(circleRect(player.getPos().x, player.getPos().y, 25, sx, sy,57,57))

        runTime = (deltaT*1000).__round__(1)
        mousePosTxt.setText(f"Mouse Pos: {inputHandler.getMousePos()}")
        runtimeTxt.setText(f"Run Time: {str(runTime)}ms")
        fpsTxt.setText(f"FPS: {str((1000/runTime).__round__())}")

        time.sleep((0.1/1000))   #Calling this redraws everything on screen.
        gw.update()
        
        deltaT = time.time() - currentTime
        
        for key_data in keys_data:
            if not key_data['collected']:
                key_color = key_data['color']
            if key_color == 'blue':
                if not key3.is_collected() and circleRect(player.getPos().x, player.getPos().y, 16, key.image.getAnchor().x, key.image.getAnchor().y, 10, 10):
                    key3.collect()
                    key_data['collected'] = True
                    player.collect_keys('blue')
                
            
            if key_data['collected'] and pointCircle(player.getPos().x, player.getPos().y, testDoor.getPosX() + 32, testDoor._Door__posY + 32, 69):
                    testDoor.update(deltaT, key_data['collected'])

        #time.sleep(image_delay)

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
    with open('grid_data','rb') as f:
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
    col = inputHandler.getMousePos()[0] // gridCellSize
    if not (col < gridSizeX):
        col = 0

    row = inputHandler.getMousePos()[1] // gridCellSize
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
    print(gridData)

    with open('grid_data', 'wb') as f:
        pickle.dump(gridData, f)
def toggleDebugView():
    global debugView
    if (debugView):
        debugView = False
    else:
        debugView = True
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
    
main()
