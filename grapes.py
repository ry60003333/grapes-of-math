#!/usr/bin/python
import pygame
from gi.repository import Gtk
import entity

class grapes:
    def __init__(self):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()

        self.bucket = entity.Entity(-100, 100, "fruit")

        self.vx = 10
        self.vy = 0

        self.paused = False
        self.direction = 1

    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

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
                    self.bucket.x, self.bucket.y = pos

            # Move the ball
            #if not self.paused:
            #    self.bucket.x += self.vx * self.direction
            #    if self.direction == 1 and self.bucket.x > screen.get_width() + 100:
            #        self.bucket.x = -100
            #    elif self.direction == -1 and self.x < -100:
            #        self.bucket.x = screen.get_width() + 100

            #    self.bucket.y += self.vy
            #    if self.bucket.y > screen.get_height() - 100:
            #        self.bucket.y = screen.get_height() - 100
            #        self.vy = -self.vy

            #    self.vy += 5

            # Clear Display
            screen.fill((255, 255, 255))  # 255 for white

            # Draw the ball
            pygame.draw.circle(screen, (255, 0, 0), (self.bucket.x, self.bucket.y), 100)

            # Flip Display
            pygame.display.flip()

            # Try to stay at 30 FPS
            self.clock.tick(30)


# This function is called when the game is run directly from the command line:
# ./TestGame.py
def main():
    pygame.init()
    pygame.display.set_mode((0, 0), pygame.RESIZABLE)
    game = grapes()
    game.run()

if __name__ == '__main__':
    main()
