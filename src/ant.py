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
        self.mode = FOODPHEROMONE
        self.exploring = True

        self.exploreDirection = random.random() * 2 * math.pi

        self.max_hunger = np.random.randint(100, 1000)
        self.hunger = self.max_hunger

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
        self.hunger -= 1
        if self.hunger < 7*self.max_hunger/8:
            self.exploring = False
            self.mode = HOMEPHEROMONE
        # TODO: Make the ant return (will wait till we have that working)
        new_x = self.xPosition + math.cos(angle) * distance
        new_y = self.yPosition + math.sin(angle) * distance
        isFree, objType = self.world.isFreePosition(new_x, new_y)

        if isFree:
            if self.exploring:
                self.world.addPheromoneLine((self.xPosition, self.yPosition), (new_x, new_y), self.mode)

            self.xPosition = new_x
            self.yPosition = new_y

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
        if self.exploring:
            self.randomExplore(delta_t)
        else:
            curr_x, curr_y = self.world.worldSpaceToPixelSpace(self.xPosition, self.yPosition)
            best_direction = {} # Initialize best direction
            for i in range(21):
                for j in range(21):
                    # Check 5x5 grid around ant for pheromones
                    target_x, target_y = (curr_x + i - 10, curr_y + j - 10)
                    x_pixel, y_pixel = self.world.pixelSpaceToWorldSpace(target_x, target_y)

                    # Check if the position is free and has a home pheromone
                    if not (0 <= target_x < self.world.world.shape[0] and 0 <= target_y < self.world.world.shape[1]):
                        continue
                    if self.world.isFreePosition(x_pixel, y_pixel):
                        food_pheromone_intensity = self.world.world[target_x, target_y, PHEROMONE_INDEX[FOODPHEROMONE]]
                        if food_pheromone_intensity > 0:
                            # Update best direction if food pheromone is stronger
                            best_direction[food_pheromone_intensity] = i, j

            if not len(best_direction) == 0:
                # Calculate the delta between ant's position and target position
                print(best_direction)
                items = sorted(best_direction)
                print(items)
                i = 0
                while i < len(items):
                    temp_x, temp_y = best_direction[items[i]][0], best_direction[items[i]][1]
                    target_x, target_y = self.world.pixelSpaceToWorldSpace(curr_x + temp_x, curr_y + temp_y)
                    dx = self.xPosition - target_x
                    dy = self.yPosition - target_y

                    distance = np.linalg.norm(np.array([dy, dx]))

                    # Calculate the direction to move towards
                    explore_direction = math.atan2(dy, dx) + math.pi
                    # Move towards the direction
                    if not self.move(explore_direction, self.antSpeed * delta_t/6):
                        # if can't move, turn around and wander in a direction
                        print("not")
                        pass
                    else:
                        print('moved')
                        break
                        pass
                    i += 1