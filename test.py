from graphics import *

#original_image = Image.open("halloween.jpg")
#original_image.save('halloween.gif')

win = GraphWin("Start Menu", 705, 705)



def start_game(win): 
    for item in win.items[:]:
        item.undraw()
    game_win = GraphWin("game", 705, 705)
    
    while True:
        click_point = game_win.checkMouse()
        if click_point:
            pass
        if win.checkMouse(): 
            game_win.close()
            return



