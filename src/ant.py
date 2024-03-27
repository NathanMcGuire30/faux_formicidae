#!/usr/bin/env python3

"""
Class to represent single ant
"""

import math
import random
import numpy as np

from enum import Enum

from world import AntWorld, Pheromones


class AntMode(Enum):
    EXPLORE = 0
    GO_HOME = 1


class Ant(object):
    def __init__(self, world: AntWorld = None, x=0, y=0, speed=1):
        self.xPosition = x
        self.yPosition = y
        self.world = world

        self.antSpeed = speed  # cm/s

        # Mode tracking variables
        self.mode = AntMode.EXPLORE
        self.activePheromone = None

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
        new_x = self.xPosition + math.cos(angle) * distance
        new_y = self.yPosition + math.sin(angle) * distance
        is_free, objType = self.world.isFreePosition(new_x, new_y)

        if is_free:
            if self.activePheromone is not None:
                self.world.addPheromoneLine((self.xPosition, self.yPosition), (new_x, new_y), self.activePheromone)

            self.xPosition = new_x
            self.yPosition = new_y
            return True
        else:
            return False

    def pheromonepathfinding(self, delta_t):
        """
        When searching for food:
        When no pheromone present, move with a random wiggle
                
        When returning home:
        Get the vector from the current position and home position
        move in that straight line


        In general: 
        When hit a wall, bounce off

        Finding Pheromones
        Sample three areas around the ant: left, right, and forward
        If a sample is found, follow that sample
        """

        # Finding food, remember means we are placing down home pheromones
        if self.mode == AntMode.EXPLORE:
            self.randomExplore(delta_t)
            self.activePheromone = Pheromones.HOME
        elif self.mode == AntMode.GO_HOME:
            pass
        else:
            raise RuntimeError("What")

        return

    def randomExplore(self, delta_t):
        direction_adj = np.random.uniform(-0.05, 0.05)
        direction_adj = 0
        direction = self.exploreDirection + direction_adj

        if not self.move(direction, self.antSpeed * delta_t):
            # if can't move, turn around and wander in a direction
            self.exploreDirection = direction + math.pi + np.random.uniform(-1.5, 1.5)

    def runOnce(self, delta_t):
        """
        Run ant simulation one timestep
        :param delta_t: length of timestep
        """

        # self.randomExplore(delta_t)
        self.pheromonepathfinding(delta_t)
