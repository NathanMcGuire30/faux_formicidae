#!/usr/bin/env python3

"""
Class to represent the world
"""

import numpy as np
import cv2
import pygame
from celldata import WALL, EMPTY, HOMEPHEROMONE, FOODPHEROMONE, FOODOBJECT, CellData

NUM_PHEROMONES = 2
PHEROMONE_INDEX = {HOMEPHEROMONE: 1, FOODPHEROMONE: 2}


class AntWorld(object):
    def __init__(self, width_cm: int, height_cm: int, resolution: int):
        """
        :param width_cm:  World width in centimeters
        :param height_cm:  World height in centimeters
        :param resolution: World resolution (cells per centimeter)
        """

        width_cells = width_cm * resolution
        height_cells = height_cm * resolution
        self.resolution = resolution

        # Currently 0s in this array are free, 1s are occupied, probably need to work on this some eventually
        # Question, how to implement pheromones.  Do we make a new array, or do we add more values to this one?
        # If multiple types of pheromones can occupy the same cell we'll probably need multiple arrays
        self.world = np.zeros((width_cells, height_cells,NUM_PHEROMONES+1))
        self.world[:,:,0] = self.world[:,:,0] + EMPTY
        # Hard-code a few obstacles for now
        # 640, 380 for now 
        self.world[400:500, 100:150,0] = self.world[400:500, 100:150,0] * WALL / EMPTY
        self.world[100:300, 200:300,0] = self.world[100:300, 200:300,0] * WALL / EMPTY
        self.world[100:300, 0:100,0] = self.world[100:300, 0:100,0] * WALL / EMPTY
        self.world[0:50, 0:50,0] = self.world[0:50, 0:50,0] * FOODOBJECT / EMPTY


    def worldSpaceToPixelSpace(self, x, y):
        """
        Function to convert coordinates in cm to array indices
        """

        return int(x * self.resolution), int(y * self.resolution)

    def pixelSpaceToWorldSpace(self, i, j):
        """
        Function to convert array indices to coordinates in cm
        """

        return float(i) / self.resolution, float(j) / self.resolution

    def isWithinBounds(self, i, j):
        return 0 <= i < self.world.shape[0] and 0 <= j < self.world.shape[1]

    def isFreePosition(self, x: float, y: float):
        """
        Returns true if the coordinate (x, y) (in cm) is not occupied by an obstacle
        """

        i, j = self.worldSpaceToPixelSpace(x, y)
        return self.isWithinBounds(i, j) and self.world[i][j][0] == EMPTY, self.world[i][j][0] if  self.isWithinBounds(i, j) else None

    def addPheromone(self, x: float, y: float, pheromone: int, amnt: int=1):
        i, j = self.worldSpaceToPixelSpace(x, y)
        self.world[i, j, PHEROMONE_INDEX[pheromone]] = amnt
        return

    def getLayer(self, layer_id: int):
        return self.world[:, :, layer_id]

    def runOnce(self, delta_t):
        """
        Advance the simulation one timestep.  Since the world doesn't change yet, this function does nothing
        If the world ever changes that code should go in here

        :param delta_t: timestep in seconds
        """

        pass

    def render(self, screen):
        
        # pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(400, 100, 100, 50))
        # pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(100, 200, 200, 100))
        # pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(100, 0, 200, 100))
        pygame.draw.rect(screen, pygame.Color('chartreuse4'), pygame.Rect(0, 0, 50, 50))

        for idx, cell in np.ndenumerate(self.world[:,:,0]):
            # if cell == WALL:
            #     pygame.draw.rect(screen, pygame.Color('black'), pygame.Rect(idx[0], idx[1], 1, 1))

            # incorporate Pheromone render
                
            if self.world[idx[0], idx[1], 1] > 0:
                pygame.draw.rect(screen, pygame.Color('blue'), pygame.Rect(idx[0], idx[1], 1, 1))
                
            if self.world[idx[0], idx[1], 2] > 0:
                pygame.draw.rect(screen, pygame.Color('green'), pygame.Rect(idx[0], idx[1], 1, 1))
        

        obstacles = self.getLayer(0).astype(np.uint8).T
        obstacles = (1 - obstacles) * 255

        obstacles_img = cv2.cvtColor(obstacles, cv2.COLOR_GRAY2BGR)

        pygame_img = pygame.image.frombuffer(obstacles_img.tostring(), obstacles_img.shape[1::-1], "BGR")
        screen.blit(pygame_img, (0, 0))
