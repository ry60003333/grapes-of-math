import pygame
from gi.repository import Gtk
from entity import Entity
import math
from math import cos, sin

import entity
# Grape class for grapes
class Grape(Entity):
    def __init__(self, x, y, numVerts):
        Entity.__init__(self, x, y)
        self.r = 20
        self.falling = False
        self.numVerts = numVerts
        self.verts = self.createVerts(numVerts)

    def update(self):
        self.verts = self.createVerts(self.numVerts)
        if self.falling == True:
            self.y += 5

    def createVerts(self, numVerts):
        theta = 2*math.pi/numVerts
        verts = []
        count = 0
        while count < numVerts:
            x = self.r * cos(theta * count) + self.x
            y = self.r * sin(theta * count) + self.y
            verts.append((x, y))
            count += 1
        return verts

    def draw(self, screen):
        # Temp draw function, I'll figure out points soon
        pygame.draw.polygon(screen, (255, 0, 255), self.verts)

    def beginFall(self):
        self.falling = True
