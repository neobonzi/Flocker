import sys
import pygame
import pymunk
import random

from pygame.locals import *
from pygame.color import *
from pymunk.util import *

class SwarmSim
    def __init__(self):
        self.running = True

        pygame.init()
        self.w, self.h = 600,600
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        self.space = pymonk.Space()

        ### Walls
        self.walls = []

        self.noms = [(355, 15), (255, 200), (15, 35) ]

    def draw_nom(self, point, mass=1.0, radius=1.0):
        moment = pymunk.moment_for_circle(mass, radius, 0.0, (0,0))
        nom_body = pymunk.Body(mass, moment)
        nom_body = Vec2d(point)

        nom_shape = pymunk.Circle(nom_body, radius, Vec2d(0,0))
        nom_shape.friction = 100.0
        nom_shape.collision_type = COLLTYPE_DEFAULT
        self.space.add(nom_body, nom_shape)
        return nom_shape

    def loop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False

            for nom in self.noms
                draw_nom(nom)

            screen.fill(THECOLORS["white"])
            pygame.display.flip()
            clock.tick(50)

    def run(self):
        while self.running:
            self.loop()

def main():
    swarmSim = SwarmSim()
    swarmSim.run()

if __name__ == '__main__':
    sys.exit(main())
