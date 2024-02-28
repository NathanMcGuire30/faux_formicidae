import numpy as np
import cv2
import pygame

from simulation import Simulation


class Renderer(object):
    def __init__(self, sim: Simulation):
        self.sim = sim

        width = self.sim.getWorld().widthCells
        height = self.sim.getWorld().heightCells

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.isRunning = True

        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill(pygame.Color('white'))

    def render(self):
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.isRunning = False

        # fill the screen with a color to wipe away anything from last frame
        self.screen.fill(pygame.Color('white'))

        self.renderWorld()

        self.renderAnts()

        # flip() the display to put your work on screen
        pygame.display.flip()

    def running(self):
        return self.isRunning

    def quit(self):
        pygame.quit()

    def renderWorld(self):
        obstacles = self.sim.getWorld().getLayer(0).astype(np.uint8).T
        obstacles = (1 - obstacles) * 255

        obstacles_img = cv2.cvtColor(obstacles, cv2.COLOR_GRAY2BGR)

        pygame_img = pygame.image.frombuffer(obstacles_img.tostring(), obstacles_img.shape[1::-1], "BGR")
        self.screen.blit(pygame_img, (0, 0))

    def renderAnts(self):
        for ant in self.sim.getAnts():
            pygame.draw.circle(self.screen, pygame.Color('brown'), ant.getPositionPixelSpace(), 5)
