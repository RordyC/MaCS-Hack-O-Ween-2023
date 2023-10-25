from graphics import *

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
title = create_label(gw, 350, 100, "THE GAME", 36, 'black', 'bold italic')

play_button = create_button(gw, 252, 300, 452, 350, 'lightgreen')
play_label = create_label(gw, 352, 325, 'Start', 14, 'white', 'bold italic')

quit_button = create_button(gw, 252, 400, 452, 450, 'brown')
quit_label = create_label(gw, 352, 425, "Exit", 14, 'white', 'bold italic')

def menu_loop(gw):
    while True:
        click_point = gw.checkMouse()
        if click_point:
            if 252 < click_point.getX() < 452:
                if 300 < click_point.getY() < 350:
                    break
                elif 400 < click_point.getY() < 450:
                    gw.close()