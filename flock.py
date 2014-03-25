import sys
import pygame
import random
from pygame.locals import *
from pygame.color import *
import pymunk

'''
A Pymunk specific function to add a single ball to space
'''
def add_boyd(space):
    mass = 5
    radius = 14
    inertia = pymunk.moment_for_circle(mass, 0, radius)
    body = pymunk.Body(mass, inertia)
    x = random.randint(120, 380)
    body.position = x, 550
    shape = pymunk.Circle(body,radius)
    space.add(body, shape)
    return shape

def draw_ball(screen, ball):
    ballPos = int(ball.body.position.x), 600 - int(ball.body.position.y)
    pygame.draw.circle(screen, THECOLORS["blue"], ballPos, int(ball.radius), 2)

def draw_wall(screen, wall):

def main():
    pygame.init()
    screen = pygame.display.set_mode((600,600))
    pygame.display.set_caption("Joints, yo")
    clock = pygame.time.Clock()
    running = True

    space = pymunk.Space()
    space.gravity = (0.0, -900.0)

    #Keep tabs on the balls
    balls = []

    #Ticks per ball spawn
    ticks_to_next_ball = 10

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                running = False

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        screen.fill(THECOLORS["white"])

        for ball in balls:
            draw_ball(screen, ball)

        space.step(1/50.0)

        pygame.display.flip()
        clock.tick(50)

if __name__ == '__main__':
    sys.exit(main())
