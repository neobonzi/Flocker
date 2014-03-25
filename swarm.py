import sys
import pygame
import pymunk
import random

from pygame.locals import *
from pygame.color import *
from pymunk.util import *
from pymunk.vec2d import *

COLLTYPE_DEFAULT = 0
COLLTYPE_MOUSE = 1

class SwarmSim:

    '''
    Translates a point from pymunk to pygame
    '''
    def flipyv(self, v):
        return int(v.x), int(-v.y + self.h)

    def __init__(self):
        self.running = True

        pygame.init()
        self.w, self.h = 600,600
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        self.space = pymunk.Space()

        ### Walls
        self.walls = []

        ## Create Chows
        self.chows = []
        chowPos = [(300,300)]

        for chow in chowPos:
            self.chows.append(self.create_chow(chow))

        ### Create Noms
        self.noms = []
        nomPos = [(355.0, 15.0), (255.0, 200.0), (15.0, 35.0), (450, 450)]

        for nom in nomPos:
            self.noms.append(self.create_nom(nom))

    def draw_chow(self, chow):


    def draw_nom(self, nom):
        body = nom.body
        color = THECOLORS["yellow"]
        pos = self.flipyv(body.position)
        rad = nom.radius
        pygame.draw.circle(self.screen, color, pos, int(rad), 0)

    def create_chow(self, point, mass=1.0):
        triangle = ((0.0, 0.0), (1.0, 3.0), (2.0, 0.0))
        moment = pymunk.moment_for_poly(mass, triangle, (0,0))
        chow_body = pymunk.Body(mass, moment)
        chow_body.position = Vec2d(point)

        chow_shape = pymunk.Poly(chow_body, triangle)
        chow_shape.friction = .2
        self.space.add(chow_body, chow_shape)
        return chow_shape

    def create_nom(self, point, mass=1.0, radius=4.0):
        moment = pymunk.moment_for_circle(mass, radius, 0.0, (0,0))
        nom_body = pymunk.Body(mass, moment)
        nom_body.position = Vec2d(point)

        nom_shape = pymunk.Circle(nom_body, radius, Vec2d(0,0))
        nom_shape.friction = .95
        nom_shape.collision_type = COLLTYPE_DEFAULT
        self.space.add(nom_body, nom_shape)
        return nom_shape

    def draw(self):
        self.screen.fill(THECOLORS["black"])

        ### Draw noms
        for nom in self.noms:
            self.draw_nom(nom)

        ### Draw chows
        for chow in self.chows:
            self.draw_chow(chow)

        pygame.display.flip()

    def loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.running = False

        self.draw()

        pygame.display.flip()
        self.clock.tick(50)

    def run(self):
        while self.running:
            self.loop()

def main():
    swarmSim = SwarmSim()
    swarmSim.run()

if __name__ == '__main__':
    sys.exit(main())
