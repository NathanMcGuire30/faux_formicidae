import numpy as np
import cv2
import pygame

from simulation import Simulation
from world import WorldCell


class Renderer(object):
    def __init__(self, sim: Simulation, nestLoc):
        self.sim = sim
        self.nestLoc = nestLoc

        self.width = self.sim.getWorld().widthCells
        self.height = self.sim.getWorld().heightCells

        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.set_colorkey((255, 255, 255))
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

        import time

        a = time.time()
        self.renderWorld()

        self.renderPheromoneFast(1, (0, 0, 255))
        self.renderPheromoneFast(2, (0, 100, 0))

        self.renderAnts()

        self.renderNest()

        # flip() the display to put your work on screen
        pygame.display.flip()

    def running(self):
        return self.isRunning

    def quit(self):
        pygame.quit()

    def renderWorld(self):
        obstacles = self.sim.getWorld().getLayer(0).astype(np.uint8).T
        obstacles = (WorldCell.WALL - obstacles) * 255

        obstacles_img = cv2.cvtColor(obstacles, cv2.COLOR_GRAY2BGR)

        pygame_img = pygame.image.frombuffer(obstacles_img.tostring(), obstacles_img.shape[1::-1], "BGR")
        pygame_img.set_colorkey((255, 255, 255))
        self.screen.blit(pygame_img, (0, 0))

    def renderPheromoneFast(self, layer, color):
        pheromones = self.sim.getWorld().getLayer(layer).astype(np.float64).T

        pheromones_img = np.zeros((pheromones.shape[0], pheromones.shape[1], 4), dtype=np.uint8)
        pheromones_img[:, :, 0:3] = color
        pheromones_img[:, :, 3] = (pheromones * 255).astype(np.uint8)

        pygame_img = pygame.image.frombuffer(pheromones_img.tostring(), pheromones_img.shape[1::-1], "RGBA")
        pygame_img.set_colorkey((255, 255, 255))
        # return pygame_img
        self.screen.blit(pygame_img, (0, 0))

    def renderAnts(self):
        for ant in self.sim.getAnts():
            pygame.draw.circle(self.screen, pygame.Color('brown'), ant.getPositionPixelSpace(), 2)

    def renderNest(self):
        pygame.draw.circle(self.screen, pygame.Color('orange'), self.nestLoc, 2)
