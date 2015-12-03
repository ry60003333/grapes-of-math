import pygame, os
from gi.repository import Gtk

from entity import Entity

class Background(Entity):
    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.sprite = pygame.image.load(os.path.join("background.jpg")).convert()
        
    def draw(self, screen):
        screen.blit(self.sprite, (self.x, self.y))
