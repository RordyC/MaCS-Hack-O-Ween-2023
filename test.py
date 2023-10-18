from graphics import *

#original_image = Image.open("halloween.jpg")
#original_image.save('halloween.gif')

win = GraphWin("Start Menu", 705, 705)
background = Image(Point(352, 352), 'blood.png')
background.draw(win)

def create_button(win, x1, y1, x2, y2, color):
    button = Rectangle(Point(x1, y1), Point(x2,y2))
    button.setFill(color)
    button.draw(win)
    return button

def create_label(win, x, y, text, size, color, style,):
    label = Text(Point(x, y), text)
    label.setSize(size)
    label.setTextColor(color)
    label.setStyle(style)
    label.draw(win)
    return label

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



title = create_label(win, 350, 100, "THE GAME", 36, 'black', 'bold italic')

play_button = create_button(win, 252, 300, 452, 350, 'lightgreen')
play_label = create_label(win, 352, 325, 'Start', 14, 'white', 'bold italic')

quit_button = create_button(win, 252, 400, 452, 450, 'brown')
quit_label = create_label(win, 352, 425, "Exit", 14, 'white', 'bold italic')

while True:
    click_point = win.checkMouse()
    if click_point:
        if 252 < click_point.getX() < 452:
            if 300 < click_point.getY() < 350:
                start_game(win)
            elif 400 < click_point.getY() < 450:
                win.close()