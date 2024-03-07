import numpy as np
import cv2
import pygame

from simulation import Simulation
from celldata import WALL, ENTITY_COLOR


class Renderer(object):
    def __init__(self, sim: Simulation):
        self.sim = sim

        self.width = self.sim.getWorld().widthCells
        self.height = self.sim.getWorld().heightCells

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.set_colorkey((255,255,255))
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

        self.renderPheromone()

        # world_surface.blit(pheromone_surface, (0,0))
        # self.screen.blit(world_surface,(0,0))
        self.renderAnts()

        # flip() the display to put your work on screen
        pygame.display.flip()

    def running(self):
        return self.isRunning

    def quit(self):
        pygame.quit()

    def renderPheromone(self):
        surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surface.set_colorkey((255,255,255))
        terrain = self.sim.getWorld().getLayer(1)
        test = {1: (0,0,255), 0:(255,255,255)}
        palette = np.stack(np.vectorize(test.get)(terrain), axis=-1)
        # print(palette.shape)

        pygame.surfarray.blit_array(surface, palette)
        self.screen.blit(surface, (0, 0))

    def renderWorld(self):
        obstacles = self.sim.getWorld().getLayer(0).astype(np.uint8).T
        obstacles = (WALL - obstacles) * 255

        obstacles_img = cv2.cvtColor(obstacles, cv2.COLOR_GRAY2BGR)

        pygame_img = pygame.image.frombuffer(obstacles_img.tostring(), obstacles_img.shape[1::-1], "BGR")
        # return pygame_img
        self.screen.blit(pygame_img, (0, 0))

    def renderAnts(self):
        for ant in self.sim.getAnts():
            pygame.draw.circle(self.screen, pygame.Color('brown'), ant.getPositionPixelSpace(), 2)
