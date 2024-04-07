"""
Class to manage the spawning of ants

Contains the actual parameters that are managed by the genetic algorithm, since all ants are the same
"""

from dataclasses import dataclass

from ant import Ant


# TODO: Get these parameters into the ant colony from the genetic algorithm
# TODO: Do stuff with them

@dataclass
class ColonyParameters(object):
    speed: float
    spawn_interval: float


class AntColony(object):
    def __init__(self, x, y):
        self.addAnt = None
        self.xPosition = x
        self.yPosition = y

    def setCallback(self, callback_fn):
        self.addAnt = callback_fn

    def makeAnt(self):
        """
        Call this to spawn a new ant
        """

        # TODO: Set ant parameters

        self.addAnt(Ant(), self.xPosition, self.yPosition)

    def runOnce(self):
        # TODO: Control how often ants spawn

        self.makeAnt()
