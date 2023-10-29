from graphics import *
from InputHandler import *
from Collisions import circleRectMove


class Animation:
    def __init__(self, images, delay, player):
        self.images = images
        self.delay = delay
        self.frame_index = 0
        self.last_update_time = time.time()
        self.player = player
        
        

    def draw(self, gw):
        player_pos = self.player.getPos()  # Get the player's position
        self.images[self.frame_index].move(player_pos.x, player_pos.y)  # Update the animation's position
        self.images[self.frame_index].draw(gw)


    def update(self, deltaT):
        current_time = time.time()
        if current_time - self.last_update_time >= self.delay:
            self.last_update_time = current_time
            self.frame_index = (self.frame_index + 1 ) % len(self.images)
            