import pygame
from gi.repository import Gtk

import entity
# Grape class for grapes
class Grape(entity.Entity):
    def __init__(self, numPoints):
        self.r = 10
        self.falling = False
        self.numPoints = numPoints

    def update(self):
        if self.falling == True:
            self.y -= 5

    def draw(self, screen):
        # Temp draw function, I'll figure out points soon
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)

    def beginFall(self):
        self.falling = True
