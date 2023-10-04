#Rordy
#Tyler
#Add your names here!!

import random
import winsound #winsound.PlaySound("ui_menu_button_beep_13", winsound.SND_FILENAME | winsound.SND_ASYNC)
import graphics
from Monster import *
from Player import Player
from InputHandler import *
from graphics import *
from time import sleep

width = 720
height = 720

gw = GraphWin("GAME", width, height) #This is the window where all the grapics are drawn.

inputHandler = InputHandler() #Object that recieves input from the window.

player = Player(Point(width/2,height/2),inputHandler) #Player object that is controller by user.
monster = Monster() #Monster object that chases the player around the map.

mousePosTxt = Text(Point(600, 25), f"Mouse Pos: {0},{0}")
mousePosTxt.setTextColor("cyan")

runtimeTxt = Text(Point(400, 25), "")

def main():
    global gw
    gw.setBackground("black")
    gw.setInputHandler(inputHandler) #We pass in the input handler to the window so it can recieve input!

    mousePosTxt.draw(gw)
    runtimeTxt.setTextColor("red")
    runtimeTxt.draw(gw)

    monster.draw(gw)
    player.draw(gw)

    done = False
    while not done: #This will run until 'done' is False.
        fps = time.time()

        monster.setTargetPos(player.getPos().x,player.getPos().y)
        monster.update()
        player.update()

        tt = time.time() - fps
        sleep((6/1000))
        runTime = (tt*1000).__round__(2)

        mousePosTxt.setText(f"Mouse Pos: {inputHandler.getMousePos()}")
        runtimeTxt.setText(f"Run Time: {str(runTime)}ms")

        if (gw.closed): #When the window is closed the gameloop finishes
            done = True

main() #Calling this starts the game loop.