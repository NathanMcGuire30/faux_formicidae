#!/usr/bin/env python3

"""
Class to run the simulation

Contains a world and a list of ant colony classes, manages the updates of each
"""

import typing

from faux_formicidae.world import AntWorld
from faux_formicidae.ant_colony import AntColony
from faux_formicidae.ant import Ant


class Simulation(object):
    def __init__(self, world: AntWorld):
        self.world = world
        self.clock = 0

        self.antColony = None
        self.ants: typing.List[Ant] = []
        self.deadAnts = 0

    def addAntColony(self, colony: AntColony):
        self.antColony = colony
        self.antColony.setCallback(self.addAnt)

    def addAnt(self, ant: Ant, x: float, y: float):
        isFree, objType = self.world.isFreePosition(x, y)
        if isFree:
            self.ants.append(ant)
            ant.setWorld(self.world)
            ant.setPosition(x, y)
        else:
            print(f"Can't add ant at {x}, {y}")

    def getWorld(self):
        return self.world

    def getAnts(self):
        return self.ants

    def runOnce(self, delta_t=0.1):
        """
        Function to advance the simulation one time step
        :param delta_t: time step length, in seconds
        :return:
        """

        # Update the world
        self.world.runOnce(delta_t)

        # Update the colony
        if self.antColony is not None:
            self.antColony.runOnce(delta_t, self.clock)

        # Update the ants
        for ant in self.ants:
            ant.runOnce(delta_t)

            if ant.energy <= 0:
                self.ants.remove(ant)
                self.deadAnts += 1

        # print(len(self.ants), self.deadAnts)

        # Update the clock
        self.clock += delta_t
