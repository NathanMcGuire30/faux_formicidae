#!/usr/bin/env python3

"""
Class to represent single ant
"""

import math
import random
import numpy as np

from world import AntWorld
from celldata import HOMEPHEROMONE, FOODPHEROMONE

ANGLEOFCHANGE = 0.75

class Ant(object):
    def __init__(self, world: AntWorld = None, x=0, y=0, speed=1):
        self.xPosition = x
        self.yPosition = y
        self.world = world

        self.antSpeed = speed  # cm/s

        self.mode = HOMEPHEROMONE

        self.exploreDirection = random.random() * 2 * math.pi

    def setWorld(self, world):
        self.world = world

    def setPosition(self, x, y):
        self.xPosition = x
        self.yPosition = y

    def getPosition(self):
        return self.xPosition, self.yPosition

    def getPositionPixelSpace(self):
        return self.world.worldSpaceToPixelSpace(self.xPosition, self.yPosition)

    def move(self, angle, distance):
        new_x = self.xPosition + math.cos(angle) * distance
        new_y = self.yPosition + math.sin(angle) * distance

        if self.world.isFreePosition(new_x, new_y):
            self.xPosition = new_x
            self.yPosition = new_y
            self.world.addPheromone(self.xPosition, self.yPosition, self.mode)
            return True
        else:
            return False

    def randomExplore(self, delta_t):
        direction_adj = np.random.uniform(-1, 1) * ANGLEOFCHANGE
        direction = self.exploreDirection + direction_adj

        if not self.move(direction, self.antSpeed * delta_t):
            # if can't move, turn around and wander in a direction
            # change colors for testing
            self.mode = FOODPHEROMONE
            self.exploreDirection = direction + math.pi + np.random.uniform(-1, 1) * ANGLEOFCHANGE

    def runOnce(self, delta_t):
        """
        Run ant simulation one timestep
        :param delta_t: length of timestep
        """

        self.randomExplore(delta_t)
