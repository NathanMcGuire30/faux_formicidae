"""
Class to manage the spawning of ants

Contains the actual parameters that are managed by the genetic algorithm, since all ants are the same
"""

import numpy

from dataclasses import dataclass

from faux_formicidae.src.faux_formicidae.ant import Ant


# TODO: Get these parameters into the ant colony from the genetic algorithm
# TODO: Do stuff with them

@dataclass
class ColonyParameters(object):
    speed: float  # Faster ants go faster
    size: float  # Larger ants carry more
    spawn_interval: float  # How often does the colony spawn new ants

    def getAsList(self):
        return list(self.__dict__.values())

    def getAsNumpy(self):
        return numpy.asarray(self.getAsList())

    def floatDict(self):
        """
        YAML has issues if the values are numpy data types
        """

        data_dict = self.__dict__
        for key in data_dict:
            data_dict[key] = float(data_dict[key])
        return data_dict


class AntColony(object):
    def __init__(self, x, y, params: ColonyParameters):
        self.addAnt = None
        self.xPosition = x
        self.yPosition = y

        self.colonyParameters = params

        self.energy = 100000
        self.nextSpawnTime = 0

    def setParams(self, params: ColonyParameters):
        self.colonyParameters = params

    def position(self):
        return [self.xPosition, self.yPosition]

    def giveFood(self, amount):
        # print("Colony food")

        # If an ant tries to take food, don't let it take more than there is
        if amount <= 0:
            self.energy -= min(-1*amount, self.energy)
            # The ant needs to know how much food it is taking from the nest
            return min(-1*amount, self.energy)

        self.energy += amount


    def setCallback(self, callback_fn):
        self.addAnt = callback_fn

    def makeAnt(self):
        """
        Call this to spawn a new ant
        """

        # TODO: Set ant parameters

        ant = Ant(self.giveFood, speed=self.colonyParameters.speed, size=self.colonyParameters.size)
        ant.setHomePosition(self.xPosition, self.yPosition)
        ant.energy = min(ant.stamina, self.energy)
        self.addAnt(ant, self.xPosition, self.yPosition)

        # TODO: scale (this should work now - since we spawn an ant with x stamina we are effectively feeding it that much on spawn)
        self.energy -= min(ant.stamina, self.energy)

    def runOnce(self, dt, clock_time):
        # TODO: Control how often ants spawn

        # TODO: energy is parameter

        if self.energy > 5 and clock_time > self.nextSpawnTime:
            self.makeAnt()
            self.nextSpawnTime += self.colonyParameters.spawn_interval
