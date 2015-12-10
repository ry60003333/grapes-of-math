import pygame
from gi.repository import Gtk
from entity import Entity
import math
from math import cos, sin

import entity
# Grape class for grapes
class Grape(Entity):

    MIN_VERTS = 3
    MAX_VERTS = 6
    DEFAULT_RADIUS = 30

    def __init__(self, x, y, numVerts):
        Entity.__init__(self, x, y)
        self.r = Grape.DEFAULT_RADIUS
        self.falling = False
        self.numVerts = numVerts
        self.verts = self.createVerts(numVerts)
        self.value = self.numVerts * 2
        self.color = (227, 18, 213)

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
        pygame.draw.polygon(screen, self.color, self.verts)

    def beginFall(self):
        self.falling = True
