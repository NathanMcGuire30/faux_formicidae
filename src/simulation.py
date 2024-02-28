#!/usr/bin/env python3

"""
Class to run the simulation

Contains a world and a list of ant colony classes, manages the updates of each
"""

import typing
import pygame

from world import AntWorld
from ant import Ant


class Simulation(object):
    def __init__(self, world: AntWorld):
        self.world = world

        self.ants: typing.List[Ant] = []

    def addAnt(self, ant: Ant, x: float, y: float):
        isFree, objType = self.world.isFreePosition(x, y)
        if isFree:
            self.ants.append(ant)
            ant.setWorld(self.world)
            ant.setPosition(x, y)
        else:
            pass
            # TODO: This really shouldn't happen, but we should probably do something here

    def getWorld(self):
        return self.world

    def getAnts(self):
        return self.ants

    def runOnce(self, screen, delta_t=0.1):
        """
        Function to advance the simulation one time step
        :param delta_t: time step length, in seconds
        :return:
        """

        # Update the world
        self.world.runOnce(delta_t)
        self.world.render(screen)

        # Update the ants
        for ant in self.ants:
            ant.runOnce(delta_t)
            pygame.draw.circle(screen, pygame.Color('brown'), ant.getPositionPixelSpace(), 2)
