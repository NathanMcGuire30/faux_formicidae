#!/usr/bin/env python3

"""
Class to represent single ant
"""

import math
import random
import numpy as np

from world import AntWorld, PHEROMONE_INDEX
from celldata import HOMEPHEROMONE, FOODPHEROMONE, FOODOBJECT

ANGLEOFCHANGE = 0.75

DOWN = (0, 1)
UP = (0, -1)
RIGHT = (1, 0)
DOWN_RIGHT = (1, 1)
UP_RIGHT = (1, -1)
LEFT = (-1, 0)
DOWN_LEFT = (-1, 1)
UP_LEFT = (-1, -1)
EXPLORE_DIRECTIONS = {0: RIGHT, 1: UP_RIGHT, 2: UP, 3: UP_LEFT, 4: LEFT, 5: DOWN_LEFT, 6: DOWN, 7: DOWN_RIGHT}

ADJ_MATRIX = [DOWN, DOWN_RIGHT, RIGHT, UP_RIGHT, UP, UP_LEFT, LEFT, DOWN_LEFT]


def get_adjacent_directions(direction):
    # Find the index of the given direction
    idx = ADJ_MATRIX.index(direction)

    # Get the adjacent directions
    adjacent_directions = [ADJ_MATRIX[(idx + 1) % len(ADJ_MATRIX)],  # Next direction
                           ADJ_MATRIX[(idx - 1) % len(ADJ_MATRIX)]]  # Previous direction

    return adjacent_directions


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

        # what pheromone am I laying down
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

    def seeking(self):
        # What pheromone am I looking for
        return FOODPHEROMONE if self.mode == HOMEPHEROMONE else HOMEPHEROMONE

    def move(self, angle, distance):
        new_x = self.xPosition + math.cos(angle) * distance
        new_y = self.yPosition + math.sin(angle) * distance
        isFree, objType = self.world.isFreePosition(new_x, new_y)
        if isFree:
            self.xPosition = new_x
            self.yPosition = new_y
            # self.world.reducePheromone(self.xPosition, self.yPosition)
            self.world.addPheromone(self.xPosition, self.yPosition, self.mode)
            return True
        else:
            # for testing, just swap modes each collision
            if objType == FOODOBJECT:
                self.mode = FOODPHEROMONE
            return False

    def sampleNearby(self, angle, distance):
        '''
        delta angles: +sector, angle, -sector
        get the pheromone strength at each of these locations
        compute the weighted average of the pheromone and test angle
        compute and return the delta from this weight to the given angle 
        '''
        sample_angle = 2 * math.pi / 8
        left_angle = angle + sample_angle
        right_angle = angle - sample_angle
        targets = np.array([angle, left_angle, right_angle])

        def getTargetPheromone(angle):
            seeking = PHEROMONE_INDEX[self.seeking()]
            target_x = self.xPosition + math.cos(angle) * distance
            target_y = self.yPosition + math.sin(angle) * distance

            isFree, _ = self.world.isFreePosition(target_x, target_y)
            strength = 0
            if isFree:
                i, j = self.world.worldSpaceToPixelSpace(target_x, target_y)
                strength = self.world.world[i, j, seeking]
                strength = 1 if strength > 0 else 0
            return angle * strength

        vectored = np.vectorize(getTargetPheromone)
        targets = vectored(targets)
        result = np.average(targets)
        # print(result)
        return result

    def randomExplore(self, delta_t):
        direction_adj = np.random.uniform(-1, 1) * ANGLEOFCHANGE
        direction_sampled = self.sampleNearby(self.exploreDirection, self.antSpeed * delta_t * .05)
        direction = self.exploreDirection + direction_adj + direction_sampled

        if not self.move(direction, self.antSpeed * delta_t):
            # if can't move, turn around and wander in a direction
            self.exploreDirection = direction + math.pi + np.random.uniform(-1, 1) * ANGLEOFCHANGE

    def runOnce(self, delta_t):
        """
        Run ant simulation one timestep
        :param delta_t: length of timestep
        """

        self.randomExplore(delta_t)
