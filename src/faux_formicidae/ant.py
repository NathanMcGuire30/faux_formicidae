#!/usr/bin/env python3

"""
Class to represent single ant
"""

import math
import random
import numpy as np

from enum import Enum

from faux_formicidae.src.faux_formicidae.world import AntWorld, Pheromones, WorldCell


class AntMode(Enum):
    EXPLORE = 0
    GO_HOME = 1


def angle_diff_radians(a, b):
    """
    Takes a current and desired angle in radians, returns a signed difference i>
    Should do a-b (difference from a to b)
    logic from https://bitbucket.org/whoidsl/ds_base/src/master/ds_util/src/ds_>
    """

    dot = np.sin(a) * np.sin(b) + np.cos(a) * np.cos(b)
    cross = np.cos(a) * np.sin(b) - np.sin(a) * np.cos(b)
    diff = np.arctan2(cross, dot)

    return diff


class Ant(object):
    def __init__(self, give_food, world: AntWorld = None, x=0, y=0, speed=1, size=1):
        # speed = 1
        # size = 1
        self.xPosition = x
        self.yPosition = y
        self.world = world
        self.giveFood = give_food
        self.homePosition = (x, y)

        # Energy is how much we have left, stamina is the max
        # In order to make size matter (and not make the smallest size optimal),
        # It directly impacts how much food an ant cant hold
        # TODO: Probably would be a good idea to create constants for these multipliers
        self.energy = 1000.0 * size
        self.stamina = 1000.0 * size
        self.food_carried = 0
        self.carrying_capacity = 10*self.stamina

        # How fast we go
        self.antSpeed = speed  # cm/s
        self.antSize = size

        # Mode tracking variables
        self.mode = AntMode.EXPLORE
        self.activePheromone = None
        self.currentTrail = None

        # Temper is how far the ant is willing to continue on a dead trail to find food
        # Hope is how far the ant is willing to continue on a dead trail to find home
        self.temper = -1
        self.hope = -1

        self.temperInc = 5
        self.hopeInc = 5

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
        else:
            self.exploreDirection += math.pi + np.random.uniform(-1, 1)

        # TODO: Scale by speed
        self.energy -= (1 + self.antSpeed**2/1000 * self.antSize)
        if self.energy < self.stamina * (1 / 8):
            self.mode = AntMode.GO_HOME

        return obstacle_type

    def getDirectionToNest(self):
        x_diff = self.xPosition - self.homePosition[0]
        y_diff = self.yPosition - self.homePosition[1]
        angle = -1 * (math.pi - math.atan2(y_diff, x_diff))

        return angle

    def getDirectionAlongPheromone(self, fov: np.ndarray, pheromone):
        use_gradient = pheromone != self.currentTrail

        visible_area = fov[:, :, int(pheromone)].copy().T
        non_zero_locations = np.nonzero(visible_area)
        non_zero_values = visible_area[non_zero_locations]
        non_zero_locations = np.asarray(non_zero_locations)

        ant_location = np.asarray(visible_area.shape) / 2.0

        if min(non_zero_locations.shape) > 0:
            r = np.linalg.norm(non_zero_locations, axis=0)
            r = r * math.pi / ant_location[0]

            v = (ant_location - non_zero_locations.T).T
            theta = np.arctan2(v[0, :], v[1, :]) - np.pi
            diff = abs(angle_diff_radians(theta, self.exploreDirection - math.pi))

            # Trying to detect bends in the trail
            # max_diff = np.max(diff)
            # use_gradient = use_gradient or max_diff < 2.5

            if use_gradient:
                weights = 1.0 / non_zero_values
            else:
                weights = diff * (1.0 / non_zero_values)

            i = np.argmax(weights)
            direction = theta[i]
            self.currentTrail = pheromone
            return direction
        else:
            self.currentTrail = None
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
        DROPOFF_DISTANCE = .5
        visible_area = self.world.sampleArea(self.xPosition, self.yPosition, 0.15)
        world_layer = visible_area[:, :, 0]

        # Finding food, remember means we are placing down home pheromones
        if self.mode == AntMode.EXPLORE:
            direction = self.getDirectionAlongPheromone(visible_area, Pheromones.FOOD)
            # TODO: This can be abstracted for the returning / exploring cases
            direction_to_home = self.getDirectionToNest()
            if not(direction is None or direction_to_home is None):
                adjusted_direction = direction % (2 * math.pi)
                adjusted_direction_to_food = direction_to_home % (2 * math.pi)
                difference = abs(adjusted_direction - adjusted_direction_to_food)
                is_within_range = difference <= math.pi / 4
                if is_within_range:
                    direction = None
            food_cells = self.worldObjectVisible(visible_area, WorldCell.FOOD)
            can_see_food = food_cells is not None and len(food_cells) > 0

            if direction is not None:
                obstacle_type = self.move(direction, self.antSpeed * delta_t)
                self.exploreDirection = direction
                # if we don't find the right direction, keep trying
                # add to our hope count, larger hopeInc is, faster lose hope
                self.hope += self.hopeInc
            # if still have hope just keep going
            elif 0 < self.hope < 100:
                obstacle_type = self.move(self.exploreDirection, self.antSpeed * delta_t)
                # print("Hopefull")
            else:
                # can't find phero and no hope left
                self.hope = -1
                obstacle_type = self.randomExplore(delta_t)

            # If we found food we start going home
            # TODO: add functionality that removes food from a food source (if we get there)
            # TODO: fix the issue where the ant gets stuck once the home trail runs out (the fix seems to work but it can be improved)
            if can_see_food or obstacle_type == int(WorldCell.FOOD):
                self.mode = AntMode.GO_HOME
                self.activePheromone = Pheromones.FOOD
                self.exploreDirection += math.pi
                self.energy = self.stamina
                # I chose 10*stamina because that allows us to put more reward to carrying food, so we should see populations
                # lean towards sending ants to the end
                self.food_carried = self.carrying_capacity
            else:
                self.activePheromone = Pheromones.HOME
        elif self.mode == AntMode.GO_HOME:
            direction = self.getDirectionAlongPheromone(visible_area, Pheromones.HOME)

            # This code fixes ants getting stuck if the trail disappears
            direction_to_home = self.getDirectionToNest()
            if not(direction is None or direction_to_home is None):
                adjusted_direction = direction % (2 * math.pi)
                adjusted_direction_to_food = direction_to_home % (2 * math.pi)
                difference = abs(adjusted_direction - adjusted_direction_to_food)
                is_within_range = difference <= math.pi / 4
                if not is_within_range:
                    direction = self.getDirectionToNest()
            # direction = self.getDirectionToNest()

            if self.distanceToHome() < DROPOFF_DISTANCE:
                self.mode = AntMode.EXPLORE
                self.exploreDirection += math.pi
                if self.giveFood is not None:
                    self.giveFood(self.food_carried)
                    self.food_carried = 0
                    # In order to take food from the nest, we "fill" the remaining energy.
                    # Updated the giveFood method to return min(colony energy, amount) so the colony energy >= 0
                    self.energy = self.giveFood(-1 * (self.stamina - self.energy))
                    # TODO: Test the following:
                    # Giving its whole energy value kills the ant  We need to separate out carried food from ant energy (should work now)
                    # take food from nest (done, needs testing)
            elif direction is not None:
                # direction = self.getDirectionToNest()
                self.move(direction, self.antSpeed * delta_t)
                self.exploreDirection = direction
                self.temper += self.temperInc
            elif 0 < self.temper < 100:
                self.move(self.exploreDirection, self.antSpeed * delta_t)
            else:
                self.temper = -1
                self.randomExplore(delta_t)
        else:
            raise RuntimeError("What")

    def randomExplore(self, delta_t):
        noise_mag = math.pi / 4
        direction_adj = np.random.uniform(-noise_mag, noise_mag)
        direction = self.exploreDirection + direction_adj

        obstacle_type = self.move(direction, self.antSpeed * delta_t)

        if obstacle_type != 0:
            # if can't move, turn around and wander in a direction
            self.exploreDirection += np.random.uniform(-1.5, 1.5)

        return obstacle_type

    def runOnce(self, delta_t):
        """
        Run ant simulation one timestep
        :param delta_t: length of timestep
        """

        # self.randomExplore(delta_t)
        self.pheromonePathFinding(delta_t)
