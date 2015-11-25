import pygame
from gi.repository import Gtk

import entity

class Bucket(entity.Entity):
    def __init__(self):

    def setPos(self, x, y):
        self.x = x
        self.y = y
        self.r = 30

    def catchGrape(self, x, y, r):
        return ( (self.x - x) * (self.x - x) + (self.y - y) * (self.y - y) ) < (self.r + r) * (self.r + r)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)
