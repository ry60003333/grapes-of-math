import pygame, os
from gi.repository import Gtk

from entity import Entity

class Background(Entity):

    TOTAL_LEVELS = 4

    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.sprites = []
        for index in range(1, Background.TOTAL_LEVELS + 1):
            self.sprites.append(pygame.image.load(os.path.join("assets/levels/" + str(index) + "/background.jpg")).convert())
        
    def draw(self, level, screen):
        index = (level - 1) % len(self.sprites)
        screen.blit(self.sprites[index], (self.x, self.y))
