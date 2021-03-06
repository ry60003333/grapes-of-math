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
    def __init__(self, debug):
        # Set up a clock for managing the frame rate.
        self.clock = pygame.time.Clock()
        self.state = 'START'

        # Setup game variables
        # self.background = Background(0, 0)
        # self.bucket = Bucket(-100, 100)
        self.grapes = []
        self.spawnCount = 0
        self.changeGoalCount = 0
        self.paused = False
        self.debug = debug

        # Begin button variables
        self.startButtonX = 0
        self.startButtonY = 0
        self.startButtonSurface = None
        self.startButtonWidth = 0
        self.startButtonHeight = 0

        # Setup current level variables
        self.level = 0
        self.score = 0
        self.totalScore = 0
        self.goalScore = 0
        self.spawnTime = 0
        self.goalResetTime = 0
        self.grapeVelocity = 0
        self.maxGrapesPerTick = 0

        # Setup goal variables
        self.currentVerts = -1
        self.currentDisplayGrape = None


    def set_paused(self, paused):
        self.paused = paused

    # Called to save the state of the game to the Journal.
    def write_file(self, file_path):
        pass

    # Called to load the state of the game from the Journal.
    def read_file(self, file_path):
        pass

    # Takes the player to the next level
    def nextLevel(self):
        # Increment total score
        self.totalScore += self.score

        # Increment the level and reset the level score
        self.level += 1
        self.score = 0

        # Calculate the goal score
        self.goalScore = self.level * self.level * 40

        # Determine level index
        index = ((self.level - 1) % Background.TOTAL_LEVELS) + 1

        # Calculate spawn rate, goal change rate, and fall speed
        maxCalcLevel = 15
        calcLevel = self.level - 1
        if calcLevel > maxCalcLevel:
            calcLevel = maxCalcLevel

        self.spawnTime = 45 - int((calcLevel * 3.5))
        self.goalResetTime = 270 - int((calcLevel * 2))
        self.grapeVelocity = 5 + int((calcLevel * 1.5))
        self.maxGrapesPerTick = 1 + int((calcLevel / 1.5))

        if self.spawnTime < 10:
            self.spawnTime = 10

        if self.goalResetTime < 30:
            self.goalResetTime = 30

        if self.grapeVelocity > 17:
            self.grapeVelocity = 17

        if self.maxGrapesPerTick > 5:
            self.maxGrapesPerTick = 5

        # Start the music
        pygame.mixer.music.stop()
        pygame.mixer.music.load("assets/levels/" + str(index) + "/music.ogg")
        pygame.mixer.music.play(-1)  # Loop the music

        # Generate first goal
        self.generateNewGoal()

    # Generate a new goal for the player
    def generateNewGoal(self):
        self.currentVerts = random.randint(Grape.MIN_VERTS, Grape.MAX_VERTS)
        self.currentDisplayGrape = Grape(40, 10 + 26 + 80, self.currentVerts, 0)
        self.currentDisplayGrape.color = (25, 252, 0)
        self.randMod = random.randint(1, 5)

    # Spawns a grape
    def spawnGrape(self, width, offsetIndex):
        # Don't spawn grapes off the edge of the screen
        self.grapes.append(Grape(random.randrange(Grape.DEFAULT_RADIUS, width - Grape.DEFAULT_RADIUS), -Grape.DEFAULT_RADIUS * (offsetIndex + 1), random.randint(Grape.MIN_VERTS, Grape.MAX_VERTS), self.grapeVelocity))

    # The main game loop.
    def run(self):
        self.running = True

        screen = pygame.display.get_surface()

        # These needed to be moved for the activity to work
        self.background = Background(0, 0)
        self.bucket = Bucket(-100, 100)

        # Load the font
        self.font = pygame.font.SysFont("monospace", 33)
        self.juiceFont = pygame.font.SysFont("monospace", 30)
        self.titleFont = pygame.font.SysFont("monospace", 120)

        # Mixer setup
        pygame.mixer.init()

        # Sound setup
        self.squishEffect = pygame.mixer.Sound('assets/squish.wav')
        self.incorrectEffect = pygame.mixer.Sound('assets/incorrect.wav')

        # Start the first level
        self.nextLevel()

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
                elif event.type == pygame.MOUSEMOTION and self.state == 'GAME':
                    x, y = pos
                    # Center the bucket
                    x -= self.bucket.sprite.get_width() / 2
                    self.bucket.setPos(x, screen.get_height() * 0.8)
                elif event.type == pygame.KEYDOWN: # Shortcut to next level
                    if self.debug and event.key == pygame.K_n:
                        self.nextLevel()
                    elif event.key == pygame.K_p: # Toggle pause status
                        self.set_paused(not self.paused)
                elif event.type == pygame.MOUSEBUTTONDOWN and self.state == 'START':
                    x, y = pos
                    width, height = self.titleFont.size("Begin")
                    if x > self.startButtonX and x < self.startButtonX + self.startButtonWidth and y > self.startButtonY and y < self.startButtonY + self.startButtonHeight:
                        self.state = 'GAME'
            if self.state == 'START':
                self.background.draw(1, screen, False);
                titleText = "Grapes of Math"
                (titleWidth, titleHeight) = self.titleFont.size(titleText)
                title = self.titleFont.render(titleText, 1, (200, 200, 200))
                screen.blit(title, (screen.get_width() / 2 - (titleWidth / 2), 50))

                startText = "Begin"
                (self.startButtonWidth, self.startButtonHeight) = self.titleFont.size(startText)

                # Only generate this the first draw
                if self.startButtonX == 0:
                    overlayColor = (0, 0, 0, 127)
                    overlayRect = pygame.Rect(0, 0, self.startButtonWidth, self.startButtonHeight)
                    overlaySurface = pygame.Surface((300, 160), pygame.SRCALPHA)
                    overlaySurface.fill(overlayColor, overlayRect)

                    self.startButtonX = (screen.get_width() / 2 - (self.startButtonWidth / 2))
                    self.startButtonY = 200

                screen.blit(overlaySurface, (self.startButtonX, self.startButtonY))

                startButton = self.titleFont.render(startText, 1, (200, 200, 200))
                screen.blit(startButton, (self.startButtonX, self.startButtonY))



            elif self.state == 'GAME':

                if not self.paused:
                    # Spawn Grapes
                    if self.spawnCount > random.randrange(self.spawnTime - 5, self.spawnTime):
                        for i in range(0, random.randint(1, self.maxGrapesPerTick)):
                            self.spawnGrape(screen.get_width(), i)
                        self.spawnCount = 0

                    self.spawnCount += 1

                    # Change goal
                    if self.changeGoalCount > random.randrange(self.goalResetTime - 7, self.goalResetTime):
                        self.generateNewGoal()
                        self.changeGoalCount = 0

                    self.changeGoalCount += 1

                # Clear Display
                screen.fill((255, 255, 255))  # 255 for white

                # Draw the background
                self.background.draw(self.level, screen, True)

                # Draw paused text if paused
                if self.paused:
                    pauseText = "Paused"
                    (pauseWidth, pauseHeight) = self.titleFont.size(pauseText)
                    pauseLabel = self.titleFont.render(pauseText, 1, (255, 255, 255))
                    pauseX = (screen.get_width() / 2) - (pauseWidth / 2)
                    pauseY = (screen.get_height() / 2) - (pauseHeight / 2)
                    screen.blit(pauseLabel, (pauseX, pauseY))

                # Draw the bucket
                self.bucket.draw(screen)

                clone = list(self.grapes)
                for i, g in enumerate(clone):
                    if not self.paused:
                        g.falling = True
                        g.update()
                        g.draw(screen)
                        if self.bucket.catchGrape(g.x, g.y, g.r):

                            # Delete the grape
                            del self.grapes[i]

                            # Check if the grape is correct
                            if g.numVerts == self.currentVerts:
                                self.score += int(g.value * 1.5)
                                self.squishEffect.play()

                                if self.score >= self.goalScore:
                                    self.nextLevel()
                            else:
                                self.score -= g.value / 3
                                if self.score < 0:
                                    self.score = 0

                                self.incorrectEffect.play()
                    else:
                        g.draw(screen)

                # Text drawing
                textX = 16
                textY = 16

                # Draw the current level text
                label = self.font.render("Level " + str(self.level), 1, (176, 229, 255))
                screen.blit(label, (textX, textY))

                textY += 26

                # Draw the score
                label = self.juiceFont.render("Grape Juice: " + str(self.score) + " / " + str(self.goalScore), 1, (219, 140, 213))
                screen.blit(label, (textX, textY))

                textY += 26;

                # Draw the current goal
                levelText = "Collect grapes with " + str(self.currentVerts) + " sides"
                if self.level == 4:
                    levelText = "Collect grapes with " + str(self.currentVerts + self.randMod) + ' - ' + str(self.randMod) + " sides"
                label = self.juiceFont.render(levelText, 1, (162, 252, 151))
                screen.blit(label, (textX, textY))

                # Only draw on level one
                if self.level == 1:
                    # Draw the current goal
                    self.currentDisplayGrape.draw(screen)

            # Flip Display
            pygame.display.flip()

            # Try to stay at 30 FPS
            self.clock.tick(30)


# This function is called when the game is run directly from the command line:
# ./TestGame.py
def main():

    # Initalize pygame
    pygame.init()

    # This is the resolution of the XO
    xo_screen_width = 1200
    xo_screen_height = 900

    # XO Mode will make the screen a fixed size
    # so the background fills up the screen
    xo_mode = True

    # Is debugging enabled
    debug = False

    # Check for low resolution mode (good for testing)
    if len(sys.argv) > 1 and sys.argv[1] == "-lowres":
        pygame.display.set_mode((800, 600), pygame.RESIZABLE)
        debug = True
    elif xo_mode:
        pygame.display.set_mode((xo_screen_width, xo_screen_height), pygame.RESIZABLE)
    else:
        pygame.display.set_mode((0, 0), pygame.RESIZABLE)


    # Set the window title
    pygame.display.set_caption("Grapes of Math")

    # Create an instance of the game
    game = grapes(debug)

    # Start the game
    game.run()


if __name__ == '__main__':
    main()
