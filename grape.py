import pygame
from gi.repository import Gtk
from entity import Entity
from math import cos, sin

import entity
# Grape class for grapes
class Grape(Entity):
    def __init__(self, x, y, numVerts):
        Entity.__init__(self, x, y)
        self.r = 20
        self.falling = False
        self.verts = self.createVerts(numVerts)
        print self.verts

    def update(self):
        if self.falling == True:
            self.y += 5

    def createVerts(self, numVerts):
        theta = 360/numVerts
        verts = []
        while numVerts > 0:
            x = self.r * cos(theta * numVerts)
            y = self.r * sin(theta * numVerts)
            verts.append((x, y))
            numVerts -= 1

        return verts

    def draw(self, screen):
        # Temp draw function, I'll figure out points soon
        pygame.draw.circle(screen, (255, 0, 255), (self.x, self.y), self.r)

    def beginFall(self):
        self.falling = True
