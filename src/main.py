#!/usr/bin/env python3

import time
import pygame
import numpy as np

from simulation import Simulation
from world import AntWorld
from ant import Ant

WIDTHSCALE = 16
HEIGHTSCALE = 9
RESOLUTION = 40

COLONY_START_SIZE = 100


def main():
    world = AntWorld(WIDTHSCALE, HEIGHTSCALE, RESOLUTION)

    sim = Simulation(world)

    # Add ants
    for _ in range(COLONY_START_SIZE):
        sim.addAnt(Ant(), 8, 5)

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTHSCALE * RESOLUTION, HEIGHTSCALE * RESOLUTION))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(pygame.Color('white'))

    while running:
        a = time.time()

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill(pygame.Color('white'))

        # Step the sim once
        # also renders
        sim.runOnce(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 10
        # don't really need a delay
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(0) / 1000

        print(time.time() - a)

    pygame.quit()


if __name__ == '__main__':
    main()
