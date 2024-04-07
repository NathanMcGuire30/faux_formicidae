"""
Class to actually run the genetic algorithm
"""

import numpy
import heapq

from tqdm import tqdm
from typing import List

from faux_formicidae.world import AntWorld
from faux_formicidae.simulation import Simulation
from faux_formicidae.renderer import Renderer
from faux_formicidae.ant_colony import AntColony, ColonyParameters

# set these to control the range of ant colonies that can be generated
MINIMUM = ColonyParameters(0, 0.1, 0)
MAXIMUM = ColonyParameters(1, 1, 10)


class GeneticAlgorithm(object):
    def __init__(self, enable_renderer=True, batch_size=10):
        self.enableRenderer = enable_renderer
        self.batchSize = batch_size

        self.simResults = []
        self.colonyParameters: List[ColonyParameters] = []

    def generateRandomColonies(self):
        """
        Generates random colonies
        """

        self.colonyParameters = []

        for i in range(self.batchSize):
            minimum = MINIMUM.getAsList()
            maximum = MAXIMUM.getAsList()

            new_params = numpy.random.uniform(minimum, maximum)
            param_object = ColonyParameters(*new_params)
            self.colonyParameters.append(param_object)

    def runBatch(self):
        for i in tqdm(range(self.batchSize)):
            self.runSimulationOnce(i)

        # Sort list
        self.simResults = [heapq.heappop(self.simResults) for i in range(len(self.simResults))]
        self.simResults.reverse()

    def runSimulationOnce(self, index):
        # We do the same thing as the visualization script, just without the renderer

        colony_params = self.colonyParameters[index]

        world = AntWorld()
        sim = Simulation(world)

        colony = AntColony(world.width / 2, world.height / 2, colony_params)
        sim.addAntColony(colony)

        self.enableRenderer = True

        if self.enableRenderer:
            renderer = Renderer(sim)

        dt = 0.05
        for i in range(100):
            sim.runOnce(dt)

            if self.enableRenderer:
                renderer.render()

        if self.enableRenderer:
            renderer.quit()

        population = int(len(sim.ants))

        heapq.heappush(self.simResults, (population, index, colony_params))  # Use index to break ties
