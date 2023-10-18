
from graphics import *

def create_button(win, x1, y1, x2, y2, color):
    button = Rectangle(Point(x1, y1), Point(x2, y2))
    button.setFill(color)
    button.draw(win)
    return button

def create_label(win, x, y, text, size):
    label = Text(Point(x, y), text)
    label.setSize(size)
    label.draw(win)
    return label


win = GraphWin("Start Menu", 705, 705)

title = create_label(win, 352, 100, "Welcome to My Game", 20)

play_button = create_button(win, 252, 300, 452, 350, "lightblue")
play_label = create_label(win, 352, 325, "Play", 14)

quit_button = create_button(win, 252, 400, 452, 450, "lightgreen")
quit_label = create_label(win, 352, 425, "Quit", 14)

