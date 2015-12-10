import pygame, os
from gi.repository import Gtk

from entity import Entity

class Background(Entity):

    # The total amount of defined levels in the game
    TOTAL_LEVELS = 4

    def __init__(self, x, y):
        Entity.__init__(self, x, y)
        self.sprites = []
        for index in range(1, Background.TOTAL_LEVELS + 1):
            self.sprites.append(pygame.image.load(os.path.join("assets/levels/" + str(index) + "/background.jpg")).convert())

        # Overlay constants
        overlayColor = (0, 0, 0, 127)
        overlayRect = pygame.Rect(3, 3, 300, 160)
        self.overlaySurface = pygame.Surface((300, 160), pygame.SRCALPHA)
        self.overlaySurface.fill(overlayColor, overlayRect)

    def draw(self, level, screen, drawOverlay):

        # Determine the index of the background to draw
        index = (level - 1) % len(self.sprites)

        # Draw the background
        screen.blit(self.sprites[index], (self.x, self.y))

        # Draw the overlay surface
        if drawOverlay:
            screen.blit(self.overlaySurface, (3, 3))
