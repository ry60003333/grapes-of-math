#!/usr/bin/python
import pygame
import sys
from gi.repository import Gtk
from entity import Entity
from bucket import Bucket
from grape import Grape
from background import Background
import random


class grapes:
    TOTAL_LEVELS = 4

    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()

        # Setup game variables
        self.background = Background(0, 0)
        self.bucket = Bucket(-100, 100)
        self.grapes = []
        self.spawnCount = 0
        self.paused = False

        # Load the font
        self.font = pygame.font.SysFont("monospace", 30)

        # Setup current level variables
        self.level = 0
        self.score = 0
        self.totalScore = 0

        # Music setup
        pygame.mixer.init()

        # Start the first level
        self.nextLevel()

    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    def nextLevel(self):
        # Increment total score
        self.totalScore += self.score

        # Increment the level and reset the level score
        self.level += 1
        self.score = 0

        # Determine level index
        index = ((self.level - 1) % Background.TOTAL_LEVELS) + 1

        # Start the music
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/levels/" + str(index) + "/music.ogg")
        pygame.mixer.music.play(-1)  # Loop the music

    def spawnGrape(self, width):
        self.grapes.append(Grape(random.randrange(0, width), random.randrange(0, 100), random.randrange(3, 10)))

    # The main game loop.
    def run(self):
        self.running = True

        screen = pygame.display.get_surface()

        while self.running:
            # Pump GTK messages.
            while Gtk.events_pending():
                Gtk.main_iteration()

            pos = pygame.mouse.get_pos()
            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.VIDEORESIZE:
                    pygame.display.set_mode(event.size, pygame.RESIZABLE)
                elif event.type == pygame.MOUSEMOTION:
                    x, y = pos
                    self.bucket.setPos(x, screen.get_height() * 0.8)

            # Spawn Grapes
            if self.spawnCount > 100:
                self.spawnGrape(screen.get_width())
                self.spawnCount = 0

            self.spawnCount += 1
            # Clear Display
            screen.fill((255, 255, 255))  # 255 for white

            # Draw the background
            self.background.draw(self.level, screen)

            # Draw the bucket
            self.bucket.draw(screen)

            clone = list(self.grapes)
            for i, g in enumerate(clone):
                g.falling = True
                g.update()
                g.draw(screen)
                if self.bucket.catchGrape(g.x, g.y, g.r):
                    self.score += g.value
                    del self.grapes[i]

                    if self.score > 20:
                        self.nextLevel()

            # Text drawing
            textX = 10
            textY = 10

            # Draw the current level text
            label = self.font.render("Level " + str(self.level), 1, (176, 229, 255))
            screen.blit(label, (textX, textY))

            textY += 25

            # Draw the score
            label = self.font.render("Score: " + str(self.score), 1, (176, 229, 255))
            screen.blit(label, (textX, textY))

            # Flip Display
            pygame.display.flip()

            # Try to stay at 30 FPS
            self.clock.tick(30)


# This function is called when the game is run directly from the command line:
# ./TestGame.py
def main():
    pygame.init()

    # This is the resolution of the XO
    xo_screen_width = 1200
    xo_screen_height = 900

    # XO Mode will make the screen a fixed size
    # so the background fills up the screen
    xo_mode = True

    # Check for low resolution mode (good for testing)
    if len(sys.argv) > 1 and sys.argv[1] == "-lowres":
        pygame.display.set_mode((800, 600), pygame.RESIZABLE)
    elif xo_mode:
        pygame.display.set_mode((xo_screen_width, xo_screen_height), pygame.RESIZABLE)
    else:
        pygame.display.set_mode((0, 0), pygame.RESIZABLE)


    # Set the window title
    pygame.display.set_caption("Grapes of Math")

    # Start the game
    game = grapes()
    game.run()


if __name__ == '__main__':
    main()
