"""
Class to manage the spawning of ants

Contains the actual parameters that are managed by the genetic algorithm, since all ants are the same
"""

import numpy

from dataclasses import dataclass

from faux_formicidae.ant import Ant


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


class AntColony(object):
    def __init__(self, x, y, params: ColonyParameters):
        self.addAnt = None
        self.xPosition = x
        self.yPosition = y

        self.colonyParameters = params

        self.energy = 100
        self.nextSpawnTime = 0

    def setParams(self, params: ColonyParameters):
        self.colonyParameters = params

    def position(self):
        return [self.xPosition, self.yPosition]

    def giveFood(self, amount):
        # print("Colony food")

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
        self.addAnt(ant, self.xPosition, self.yPosition)

        # TODO: scale
        self.energy -= 1

    def runOnce(self, dt, clock_time):
        # TODO: Control how often ants spawn

        # TODO: energy is parameter

        if self.energy > 5 and clock_time > self.nextSpawnTime:
            self.makeAnt()
            self.nextSpawnTime += self.colonyParameters.spawn_interval
