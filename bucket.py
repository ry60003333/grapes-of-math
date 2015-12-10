import pygame, os
from gi.repository import Gtk

from entity import Entity

class Bucket(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.r = 50
        self.sprite = pygame.image.load(os.path.join("assets/bucket.png")).convert_alpha()

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def catchGrape(self, x, y, r):
        return ( (self.x - x) * (self.x - x) + (self.y - y) * (self.y - y) ) < (self.r + r) * (self.r + r)

    def draw(self, screen):
        # pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)
        screen.blit(self.sprite, (self.x, self.y))
