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
from time import sleep
from tilebase import *

width = 1024
height = 1024

gw = GraphWin("GAME", width, height,autoflush=True) #This is the window where all the grapics are drawn.

inputHandler = InputHandler() #Object that recieves input from the window.

player = Player(Point(width/2,height/2),inputHandler) #Player object that is controller by user.
monster = Monster() #Monster object that chases the player around the map.

mousePosTxt = Text(Point(600, 25), f"Mouse Pos: {0},{0}")
mousePosTxt.setTextColor("cyan")


runtimeTxt = Text(Point(400, 25), "")
fpsTxt = Text(Point(400, 50), "")

deltaT = -1.0

grid = []

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

        cx = player.getPos().x
        cy =player.getPos().y

        sx = monster.getPos().x - 57/2
        sy = monster.getPos().y - 57/2

        if (gw.checkMouse()):
            row = inputHandler.getMousePos()[0]//32
            col = inputHandler.getMousePos()[1]//32
            updateState(col,row)

        monster.hit(circleRect(cx, cy, 25, sx, sy,57,57))



        runTime = (deltaT*1000).__round__(1)
        mousePosTxt.setText(f"Mouse Pos: {inputHandler.getMousePos()}")
        runtimeTxt.setText(f"Run Time: {str(runTime)}ms")
        fpsTxt.setText(f"FPS: {str((1000/runTime).__round__())}")

      #  sleep((0.00001/1000))   #Calling this redraws everything on screen.
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
    rows = int(1024/32)
    columns = int(1024/32)
    for row in range(rows):
        row_list = []
        for col in range(columns):
            print(row,col)
            tile = TileBase(row,col,32,32)
            row_list.append(tile)
        grid.append(row_list)

def updateState(row:int,col:int):
    grid[row][col].updateState(1)

makeGrid()
main() #Calling this starts the game loop.