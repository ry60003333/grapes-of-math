import pygame
from gi.repository import Gtk
from entity import Entity

import entity
# Grape class for grapes
class Grape(Entity):
    def __init__(self, x, y, verts):
        Entity.__init__(self, x, y)
        self.r = 10
        self.falling = False
        self.verts = verts

    def update(self):
        if self.falling == True:
            self.y += 5

    def draw(self, screen):
        # Temp draw function, I'll figure out points soon
        pygame.draw.circle(screen, (255, 0, 255), (self.x, self.y), self.r)

    def beginFall(self):
        self.falling = True
