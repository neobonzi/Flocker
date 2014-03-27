import sys
import pygame
import pymunk
import random
import math

from pprint import pprint
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
        return (int(v.x), int(-v.y + self.h))

    def __init__(self):
        self.running = True

        pygame.init()
        pygame.display.init()
        self.w, self.h = 640, 480
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        self.space = pymunk.Space()
        self.constraints = []
        ### Walls
        self.walls = []

        ## Create Chows
        self.chows = []
        chowPos = [(300,300)]

        for chow in chowPos:
            aChow = self.create_chow(chow)
            self.chows.append(aChow)

        ### Create Noms
        self.noms = []
        nomPos = [(355.0, 15.0), (255.0, 200.0), (15.0, 35.0), (450, 450)]

        for nom in nomPos:
            self.noms.append(self.create_nom(nom))

    def draw_chow(self, chow):
        color = THECOLORS["white"]
        v = Vec2d(self.flipyv(chow.body.position))
        orientation = chow.body.rotation_vector

        poly_verts = map(self.flipyv, chow.get_vertices())

        center = int(v.x), int(v.y)
        p2 = Vec2d(orientation.x, -orientation.y) * 10
        pygame.draw.polygon(self.screen, color, poly_verts, 0)
        pygame.draw.line(self.screen, THECOLORS["red"], center, center + p2, 5)

    def draw_nom(self, nom):
        body = nom.body
        color = THECOLORS["yellow"]
        pos = self.flipyv(body.position)
        rad = nom.radius
        pygame.draw.circle(self.screen, color, pos, int(rad), 0)

    def create_chow(self, point, mass=1.0):
        triangle = ((-10.0, 10.0), (10.0, 0.0), (-10.0, -10.0))
        moment = pymunk.moment_for_poly(mass, triangle, (0,0))
        chow_body = pymunk.Body(mass, moment)
        chow_body.position = Vec2d(point)

        # shares collision type with noms
        chow_body.collision_type = 1

        # add motor to reduce turn speed
        motor_body = pymunk.Body()
        motor_constraint = pymunk.constraint.SimpleMotor(chow_body, motor_body, 0.0)
        motor_constraint.max_force = 100.0

        chow_shape = pymunk.Poly(chow_body, triangle)
        chow_shape.friction = .2
        self.space.add(chow_body, chow_shape, motor_constraint)
        return chow_shape

    def create_nom(self, point, mass=1.0, radius=4.0):
        moment = pymunk.moment_for_circle(mass, radius, 0.0, (0,0))
        nom_body = pymunk.Body(mass, moment)
        nom_body.collision_type = 1
        nom_body.position = Vec2d(point)

        nom_shape = pymunk.Circle(nom_body, radius, Vec2d(0,0))
        nom_shape.friction = .95
        nom_shape.collision_type = COLLTYPE_DEFAULT
        self.space.add(nom_body, nom_shape)
        return nom_shape

    def draw_overlay(self):
        angleText = pygame.font.SysFont("courier",15)
        label = angleText.render("Angle: " + str(math.degrees(self.chows[0].body.angle)), 5, THECOLORS["white"])
        self.screen.blit(label, (0,0))

        angularVelText = pygame.font.SysFont("courier", 15)
        label2 = angularVelText.render("Angular Velocity: " + str(self.chows[0].body.angular_velocity), 5, THECOLORS["white"])
        self.screen.blit(label2, (0, 20))

    def draw(self):
        self.screen.fill(THECOLORS["black"])

        ### Draw noms
        for nom in self.noms:
            self.draw_nom(nom)

        ### Draw chows
        for chow in self.chows:
            self.draw_chow(chow)

        pygame.display.flip()

    '''
    Applies an actionary and reactionary force to spin an object
    in place.
    '''
    def spin_obj(self, obj, direction, force):
        body = obj.body
        # Apply the spin force
        spinAngle = body.angle
        spinVec = Vec2d(-1 * direction * math.sin(spinAngle), direction * math.cos(spinAngle))
        spinVec.length = force
        spinOffsetVec =  (5.0 * math.cos(spinAngle), 5.0 * math.sin(spinAngle))

        body.apply_impulse(spinVec, spinOffsetVec)

        # Apply the reactionary force
        reactVect = Vec2d(-1 * direction * math.sin(spinAngle), direction * math.cos(spinAngle))
        reactVect.length = -20.0
        body.apply_impulse(reactVect, (0,0))

    def loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
                elif event.key == K_RIGHT:
                    print "right"
                    self.spin_obj(self.chows[0], -1.0, 20.0)

                elif event.key == K_LEFT:
                    print "left"
                    self.spin_obj(self.chows[0], 1.0, 20.0)

                elif event.key == K_UP:
                    print "up"
                    force = 20.0
                    body = self.chows[0].body
                    angle = body.angle
                    x_force = force * math.cos(angle)
                    y_force = force * math.sin(angle)
                    self.chows[0].body.apply_impulse((x_force, y_force))

                elif event.key == K_DOWN:
                    print "down"
                    force = 20.0
                    body = self.chows[0].body
                    angle = body.angle
                    x_force = -force * math.cos(angle)
                    y_force = -force * math.sin(angle)
                    self.chows[0].body.apply_impulse((x_force, y_force))
        self.draw()
        self.draw_overlay()

        self.space.step(1/50.0)

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
