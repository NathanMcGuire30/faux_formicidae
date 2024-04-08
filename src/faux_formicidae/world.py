#!/usr/bin/env python3

"""
Class to represent the world
"""

import numpy as np
from enum import IntEnum
from skimage.draw import line
import cv2


# Possible states for world cells
class WorldCell(IntEnum):
    EMPTY = 0
    WALL = 1
    FOOD = 128


# Pheromone options
class Pheromones(IntEnum):
    HOME = 1
    FOOD = 2


NUM_PHEROMONES = Pheromones.__len__()
WIDTH_SCALE = 16
HEIGHT_SCALE = 9
RESOLUTION = 40


class AntWorld(object):
    def __init__(self, width_cm: int = WIDTH_SCALE, height_cm: int = HEIGHT_SCALE, resolution: int = RESOLUTION):
        """
        :param width_cm:  World width in centimeters
        :param height_cm:  World height in centimeters
        :param resolution: World resolution (cells per centimeter)
        """

        self.width = width_cm
        self.height = height_cm

        self.widthCells = width_cm * resolution
        self.heightCells = height_cm * resolution
        self.resolution = resolution

        # Currently 0s in this array are free, 1s are occupied, probably need to work on this some eventually
        # Question, how to implement pheromones.  Do we make a new array, or do we add more values to this one?
        # If multiple types of pheromones can occupy the same cell we'll probably need multiple arrays
        self.world = np.zeros((self.widthCells, self.heightCells, NUM_PHEROMONES + 1))
        self.world[:, :, 0] = WorldCell.EMPTY

        # Hard-code a few obstacles for now
        # 640, 380 for now 
        self.world[400:500, 100:150, 0] = WorldCell.WALL
        self.world[100:300, 200:300, 0] = WorldCell.WALL
        self.world[100:300, 0:100, 0] = WorldCell.WALL
        # self.world[0:50, 0:50, 0] = WorldCell.FOOD
        # self.world[590:640, 330:380, 0] = WorldCell.FOOD

        self.timeSince = 0

    def getWidth(self):
        return self.widthCells

    def getHeight(self):
        return self.heightCells

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
        return self.isWithinBounds(i, j) and self.world[i][j][0] == WorldCell.EMPTY, int(self.world[i][j][0]) if self.isWithinBounds(i, j) else None

    # Pheromone as a float
    # whole numbers is amount of time since epoch the last pheromone was updated
    # decimal number is the strength of the pheromone [0,1)
    def changePheromone(self, x: float, y: float, pheromone: int, amnt: float = 1.0):
        i, j = self.worldSpaceToPixelSpace(x, y)
        self.world[i, j, int(pheromone)] = amnt
        return

    def addPheromone(self, x: int, y: int, pheromone: int, amnt: float = 1.0):
        """
        Refresh the pheromone at the given location with the current time since epoch
        """
        return self.changePheromone(x, y, pheromone, amnt)

    def addPheromoneLine(self, start, end, pheromone, amount: float = 1.0):
        s_i, s_j = self.worldSpaceToPixelSpace(start[0], start[1])
        e_i, e_j = self.worldSpaceToPixelSpace(end[0], end[1])

        discrete_line = list(zip(*line(s_i, s_j, e_i, e_j)))

        for point in discrete_line:
            self.world[point[0], point[1], int(pheromone)] = amount

        pass

    def sampleArea(self, x, y, radius):
        start_x = x - radius
        end_x = x + radius
        start_y = y - radius
        end_y = y + radius

        start_i, start_j = self.worldSpaceToPixelSpace(start_x, start_y)
        end_i, end_j = self.worldSpaceToPixelSpace(end_x, end_y)

        return start_i, end_i, start_j, end_j#self.getLayerSection(start_i, end_i, start_j, end_j)

    def getLayerSection(self, start_i, end_i, start_j, end_j):
        return self.world[start_i:end_i, start_j:end_j, :]

    def getLayer(self, layer_id: int):
        return self.world[:, :, layer_id]

    def runOnce(self, delta_t):
        """
        Advance the simulation one timestep.  Since the world doesn't change yet, this function does nothing
        If the world ever changes that code should go in here

        :param delta_t: timestep in seconds
        """

        evaporate_step = 0.05 * delta_t
        self.timeSince += delta_t
        for pheromone in Pheromones:
            np.clip(self.world[:, :, int(pheromone)] - evaporate_step, 0.0, 1.0, self.world[:, :, int(pheromone)])
        # Note: we can stop food spawning and see interesting results, the colony spawns ants expecting food to be found
        if self.timeSince > 40:# and False:
            rand_pnt_x = np.random.uniform(WIDTH_SCALE)
            rand_pnt_y = np.random.uniform(HEIGHT_SCALE)
            s_i, e_i, s_j, e_j = self.sampleArea(rand_pnt_x, rand_pnt_y, 0.2)
            # print("Point", rand_pnt_x, rand_pnt_y)
            # print("Area", s_i, e_i, s_j, e_j)
            if self.world[s_i: e_i, s_j: e_j, 0].sum() == WorldCell.EMPTY:
                self.world[s_i: e_i, s_j: e_j, 0] = WorldCell.FOOD
                # print("Success")
            # print("Fail")
            self.timeSince = 0
            # I don't think the blur stuff helps right, now but we can put it back if needed
            # if self.timeSince > 10:
            #     self.world[:, :, int(pheromone)] = cv2.blur(self.world[:, :, int(pheromone)], (3, 3))
            #     self.timeSince = 0
            #     print("Blur")
