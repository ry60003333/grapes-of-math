import pygame, os
from gi.repository import Gtk
from entity import Entity
import math
from math import cos, sin

import entity
# Grape class for grapes
class Grape(Entity):

    # The minimum amount of vertices for a grape
    MIN_VERTS = 3

    # The maximum amount of vertices for a grape
    MAX_VERTS = 6

    # The default radius of a grape
    DEFAULT_RADIUS = 30

    # Array of generated textures
    TEXTURES = []

    def __init__(self, x, y, numVerts, velocity):
        Entity.__init__(self, x, y)
        self.r = Grape.DEFAULT_RADIUS
        self.falling = False
        self.numVerts = numVerts
        self.verts = self.createVerts(numVerts)
        self.value = self.numVerts * 2
        self.color = (227, 18, 213)
        self.velocity = velocity

        # Make sure our textures are generated
        if len(Grape.TEXTURES) == 0:
            self.generateTextures()

    # Generate required textures
    def generateTextures(self):

        # Load the main texture
        MAIN_TEXTURE = pygame.image.load(os.path.join("assets/grape_texture.png")).convert()

        # Generate an image for each number of vertices
        for numVerts in range(Grape.MIN_VERTS, Grape.MAX_VERTS + 1):

            # Help from https://stackoverflow.com/questions/3580500/active-texturing-with-pygame-possible-what-concepts-to-look-into

            # Create a surface to hold the mask
            mask = pygame.Surface((Grape.DEFAULT_RADIUS * 2, Grape.DEFAULT_RADIUS * 2), pygame.SRCALPHA)

            # Mask debugging
            # mask.fill((128, 128, 128), pygame.Rect(0, 0, 100, 100))

            # Calculate vertices
            theta = 2*math.pi/numVerts
            verts = []
            count = 0
            while count < numVerts:
                x = Grape.DEFAULT_RADIUS * cos(theta * count) + Grape.DEFAULT_RADIUS
                y = Grape.DEFAULT_RADIUS * sin(theta * count) + Grape.DEFAULT_RADIUS
                verts.append((x, y))
                count += 1

            # Draw the mask onto the surface
            pygame.draw.polygon(mask, (0, 0, 0), verts)

            # Copy the mask and get it's rectangle
            texturedMask = mask.copy()
            texturedRect = texturedMask.get_rect()

            # Mask the loaded texture with the polygon
            texturedMask.blit(MAIN_TEXTURE,(0,0),None,pygame.BLEND_ADD)

            # Save the final texture in memory
            Grape.TEXTURES.append(texturedMask)

    def update(self):
        #self.verts = self.createVerts(self.numVerts)
        if self.falling == True:
            self.y += self.velocity

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
        #pygame.draw.polygon(screen, self.color, self.verts)

        screen.blit(Grape.TEXTURES[self.numVerts - Grape.MIN_VERTS], (self.x - Grape.DEFAULT_RADIUS, self.y - Grape.DEFAULT_RADIUS));


    def beginFall(self):
        self.falling = True
