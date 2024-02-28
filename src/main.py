#!/usr/bin/env python3

import time
import pygame
import numpy as np

from simulation import Simulation
from world import AntWorld
from ant import Ant
from visualization import visualizeWorldMatplotlib
# colors
BROWN = (139, 69, 19)
BLACK = (0,0,0)
WHITE = (255,255,255)

WIDTHSCALE = 16
HEIGHTSCALE = 9
RESOLUTION = 40

def main():
    
    world = AntWorld(WIDTHSCALE, HEIGHTSCALE, RESOLUTION)

    sim = Simulation(world)

    # Add 10 ants
    for i in range(200):
        sim.addAnt(Ant(), 1, 1)

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((WIDTHSCALE*RESOLUTION, HEIGHTSCALE*RESOLUTION))
    clock = pygame.time.Clock()
    running = True
    dt = 0
    # fill the screen with a color to wipe away anything from last frame
    screen.fill(WHITE)

    while running:
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Step the sim once
        sim.runOnce()


        # fill the screen with a color to wipe away anything from last frame
        screen.fill(WHITE)
        # Draw Ants
        all_ants = sim.getAnts()
        for ant in all_ants:
            pygame.draw.circle(screen, BROWN, ant.getPositionPixelSpace(), 5)

            
        all_cells = sim.getWorld().world
        for idx, cell in np.ndenumerate(all_cells):
            if cell == 1:
                # x, y = sim.getWorld().worldSpaceToPixelSpace(idx[0], idx[1])
                pygame.draw.rect(screen, BLACK, pygame.Rect(idx[0], idx[1], 1, 1), 10)
        
        # Boundaries
        # x = max(0, min(screen.get_width(), x))
        # y = max(0, min(screen.get_height(), y))


        keys = pygame.key.get_pressed()
        # if keys[pygame.K_w]:
        #     player_pos.y -= 300 * dt
        # if keys[pygame.K_s]:
        #     player_pos.y += 300 * dt
        # if keys[pygame.K_a]:
        #     player_pos.x -= 300 * dt
        # if keys[pygame.K_d]:
        #     player_pos.x += 300 * dt
        if keys[pygame.K_ESCAPE]:
            running = False

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

    pygame.quit()



if __name__ == '__main__':
    main()