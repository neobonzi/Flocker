"""A basic flocking bird simulation with one leader.
"""
__version__ = "$Id:$"
__docformat__ = "reStructuredText"

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk as pm
from pymunk import Vec2d
import pymunk.util as u

class FlockDemo:
    def __init__(self):
        self.running = True

        ### Init pygame and create screen
        pygame.init()
        self.w self.h = 600, 600
