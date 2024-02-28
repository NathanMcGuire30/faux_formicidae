#!/usr/bin/env python3

"""
Class to represent single ant
"""

import math
import random

from world import AntWorld

ANGLEOFCHANGE = 0.8

class Ant(object):
    def __init__(self, world: AntWorld = None, x=0, y=0):
        self.xPosition = x
        self.yPosition = y
        self.world = world

        self.antSpeed = 1  # cm/s

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
            return True
        else:
            return False

    def randomExplore(self, delta_t):
        direction_adj = random.random() * ANGLEOFCHANGE
        direction = self.exploreDirection + direction_adj

        if not self.move(direction, self.antSpeed * delta_t):
            self.exploreDirection = random.random() * 2 * math.pi

    def runOnce(self, delta_t):
        """
        Run ant simulation one timestep
        :param delta_t: length of timestep
        """

        self.randomExplore(delta_t)
