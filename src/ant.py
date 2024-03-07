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

UP = (0,1)
DOWN = (0,-1)
RIGHT = (1,0) 
UP_RIGHT = (1,1)
DOWN_RIGHT = (1,-1)
LEFT = (-1, 0)
UP_LEFT = (-1, 1)
DOWN_LEFT = (-1, -1)
EXPLORE_DIRECTIONS = {0:RIGHT, 1: UP_RIGHT, 2:UP, 3:UP_LEFT, 4:LEFT, 5:DOWN_LEFT, 6:DOWN, 7:DOWN_RIGHT}

# How does an ant know the direction of a trail?
# flows towards highest strength?
# an ant knows where home is
    # an ant going home will follow the home trail in the direction of home
    # an ant going for food will follow the food trail in the direction away of home

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

    def radDirectionToGridDirection(self, angle_rad):
        normalized = angle_rad % (2 * math.pi)
        # make 8 sectors
        sectors = 2 * math.pi / 8
        # shift the sectors by one half a sector
        offset = sectors / 2

        index = int(normalized + offset // sectors)
        return EXPLORE_DIRECTIONS[index]


    def move(self, angle, distance):
        # split circle into eight sectors, map them to a direction
        # each sector is pi/4 radians, needs to have an offset of pi/8 radians
        # convert radians into directions
        # can I just mod by 2pi?
        # mod by 2pi, subtract pi/8, and take a range
        new_x = self.xPosition + math.cos(angle) * distance
        new_y = self.yPosition + math.sin(angle) * distance
        # new_dir = self.radDirectionToGridDirection(angle)
        # print(angle, new_dir)
        # new_x = self.xPosition + new_dir[0]
        # new_y = self.yPosition + new_dir[1]
        isFree, objType = self.world.isFreePosition(new_x, new_y)
        if isFree:
            self.xPosition = new_x
            self.yPosition = new_y
            # self.world.reducePheromone(self.xPosition, self.yPosition)
            self.world.addPheromone(self.xPosition, self.yPosition, self.mode)
            return True
        else:
            return False

    def randomExplore(self, delta_t):
        direction_adj = np.random.uniform(-1, 1) * ANGLEOFCHANGE + 0
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
