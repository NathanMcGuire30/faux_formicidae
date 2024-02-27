#!/usr/bin/env python3

"""
Class to represent the world
"""

import numpy


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
        self.world = numpy.zeros((width_cells, height_cells))

        # Hard-code a few obstacles for now
        self.world[40:60, 10:15] = 1
        self.world[60:80, 60:100] = 1
        self.world[20:30, 50:80] = 1

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
        return self.isWithinBounds(i, j) and self.world[i][j] == 0

    def runOnce(self, delta_t):
        """
        Advance the simulation one timestep.  Since the world doesn't change yet, this function does nothing
        If the world ever changes that code should go in here

        :param delta_t: timestep in seconds
        """

        pass
