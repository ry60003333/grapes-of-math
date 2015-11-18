import pygame
from gi.repository import Gtk

class Entity:
    def __init__(self, x, y, asset):
        self.x = x
        self.y = y
        self.asset = asset

    def draw(self):
        pass

    def update(self):
        pass

    def move(self, x, y):
        self.x += x
        self.y += y
