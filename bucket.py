import pygame, os
from gi.repository import Gtk

from entity import Entity

class Bucket(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.r = 80
        self.sprite = pygame.image.load(os.path.join("assets/bucket.png")).convert_alpha()

    def setPos(self, x, y):
        self.x = x
        self.y = y

    def catchGrape(self, x, y, r):
        #return ( (self.x - x) * (self.x - x) + (self.y - y) * (self.y - y) ) < (self.r + r) * (self.r + r)

        upperX = self.x + self.sprite.get_width()
        upperY = self.y + self.sprite.get_height()

        return ( x > self.x and x < upperX and y > self.y and y < upperY )

    def draw(self, screen):
        # pygame.draw.circle(screen, (255, 0, 0), (self.x, self.y), self.r)
        screen.blit(self.sprite, (self.x, self.y))
