#!/usr/bin/env python3

"""
Class to represent single ant
"""

import math
import random
import numpy as np

from enum import Enum

from world import AntWorld, Pheromones, WorldCell


class AntMode(Enum):
    EXPLORE = 0
    GO_HOME = 1


def angle_diff_radians(a, b):
    """
    Takes a current and desired angle in radians, returns a signed difference i>
    Should do a-b (difference from a to b)
    logic from https://bitbucket.org/whoidsl/ds_base/src/master/ds_util/src/ds_>
    """

    dot = math.sin(a) * math.sin(b) + math.cos(a) * math.cos(b)
    cross = math.cos(a) * math.sin(b) - math.sin(a) * math.cos(b)
    diff = math.atan2(cross, dot)

    return diff


class Ant(object):
    def __init__(self, world: AntWorld = None, x=0, y=0, speed=1):
        self.xPosition = x
        self.yPosition = y
        self.world = world
        self.homePosition = [x, y]

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

    def setHomePosition(self, x, y):
        self.homePosition = [x, y]

    def distanceToHome(self):
        v = np.asarray([self.xPosition, self.yPosition]) - np.asarray(self.homePosition)
        return np.linalg.norm(v)

    def getPosition(self):
        return self.xPosition, self.yPosition

    def getPositionPixelSpace(self):
        return self.world.worldSpaceToPixelSpace(self.xPosition, self.yPosition)

    def move(self, angle, distance):
        new_x = self.xPosition + math.cos(angle) * distance
        new_y = self.yPosition + math.sin(angle) * distance
        is_free, obstacle_type = self.world.isFreePosition(new_x, new_y)

        if is_free:
            if self.activePheromone is not None:
                self.world.addPheromoneLine((self.xPosition, self.yPosition), (new_x, new_y), self.activePheromone)

            self.xPosition = new_x
            self.yPosition = new_y

        return obstacle_type

    def getDirectionAlongPheromone(self, fov: np.ndarray, pheromone):
        visible_area = fov[:, :, int(pheromone)].copy()
        non_zero_values = visible_area[np.nonzero(visible_area)]

        # If we can see a pheromone
        if len(non_zero_values) > 0:
            visible_area = visible_area.T
            min_val = np.min(non_zero_values)
            min_location = np.where(visible_area == min_val)
            min_location = np.asarray([float(min_location[0][0]), float(min_location[1][0])])
            ant_location = np.asarray(visible_area.shape) / 2.0

            v = ant_location - min_location
            return math.atan2(v[0], v[1]) - math.pi
        else:
            return None

    def worldObjectVisible(self, fov: np.ndarray, object_type):
        visible_area = fov[:, :, 0].copy()
        locations = visible_area[np.where(visible_area == object_type)]
        return locations

    def pheromonePathFinding(self, delta_t):
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

        visible_area = self.world.sampleArea(self.xPosition, self.yPosition, 0.1)
        world_layer = visible_area[:, :, 0]

        # Finding food, remember means we are placing down home pheromones
        if self.mode == AntMode.EXPLORE:
            direction = self.getDirectionAlongPheromone(visible_area, Pheromones.FOOD)
            food_cells = self.worldObjectVisible(visible_area, WorldCell.FOOD)
            can_see_food = food_cells is not None and len(food_cells) > 0

            if direction is not None:
                obstacle_type = self.move(direction, self.antSpeed * delta_t)
                self.exploreDirection = direction
            else:
                obstacle_type = self.randomExplore(delta_t)

            # If we found food we start going home
            if can_see_food or obstacle_type == int(WorldCell.FOOD):
                self.mode = AntMode.GO_HOME
                self.activePheromone = Pheromones.FOOD
            else:
                self.activePheromone = Pheromones.HOME
        elif self.mode == AntMode.GO_HOME:
            direction = self.getDirectionAlongPheromone(visible_area, Pheromones.HOME)

            if self.distanceToHome() < 0.1:
                self.mode = AntMode.EXPLORE
            elif direction is not None:
                self.move(direction, self.antSpeed * delta_t)
                self.exploreDirection = direction
            else:
                self.randomExplore(delta_t)
        else:
            raise RuntimeError("What")

    def randomExplore(self, delta_t):
        noise_mag = 0.4
        direction_adj = np.random.uniform(-noise_mag, noise_mag)
        direction = self.exploreDirection + direction_adj

        obstacle_type = self.move(direction, self.antSpeed * delta_t)

        if obstacle_type != 0:
            # if can't move, turn around and wander in a direction
            self.exploreDirection = direction + math.pi + np.random.uniform(-1.5, 1.5)

        return obstacle_type

    def runOnce(self, delta_t):
        """
        Run ant simulation one timestep
        :param delta_t: length of timestep
        """

        # self.randomExplore(delta_t)
        self.pheromonePathFinding(delta_t)
