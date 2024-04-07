"""
Class to actually run the genetic algorithm
"""

import os
import yaml
import numpy
import heapq
import random

from tqdm import tqdm
from typing import List

from faux_formicidae.world import AntWorld
from faux_formicidae.simulation import Simulation
from faux_formicidae.renderer import Renderer
from faux_formicidae.ant_colony import AntColony, ColonyParameters

# set these to control the range of ant colonies that can be generated
MINIMUM = ColonyParameters(0, 0.1, 0)
MAXIMUM = ColonyParameters(1, 1, 10)

PATH = os.path.abspath(os.path.join(os.path.abspath(__file__), "..", "..", ".."))


class GeneticAlgorithm(object):
    def __init__(self, enable_renderer=False, batch_size=20):
        self.enableRenderer = enable_renderer
        self.batchSize = batch_size

        self.defaultSaveFile = os.path.join(PATH, "data", "best_ants.yaml")

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

    def generateColoniesFromSimResults(self):
        """
        The actual genetic algorithm implementation
        """

        # Clean out colony parameters
        self.colonyParameters = []

        # TODO: Define hyper-parameters better

        # Hyper-parameters (for now)
        num_to_keep = max(int(len(self.simResults) * 0.1), 2)
        noise_stdev = 0.1
        alpha = 0.5  # This could use a better name

        # Keep good ones
        kept_sim_results = self.simResults[0:num_to_keep]
        kept_sim_results = [i[2] for i in kept_sim_results]
        num_to_make = len(self.simResults) - num_to_keep

        # Start filling out new colony parameters
        for result in kept_sim_results:
            self.colonyParameters.append(result)

        # Mutate and crossover
        num_to_mutate = int(num_to_make * alpha)
        num_to_crossover = num_to_make - num_to_mutate

        # Make some mutations
        # TODO: Enforce limits on new parameters
        for i in range(num_to_mutate):
            base = random.choice(kept_sim_results)
            params = base.getAsNumpy()
            params += numpy.random.normal(0, noise_stdev, params.shape)
            param_object = ColonyParameters(*params)
            self.colonyParameters.append(param_object)

        # Make some crossovers
        for i in range(num_to_crossover):
            parents = random.sample(kept_sim_results, 2)
            parents = [i.getAsList() for i in parents]
            split_point = int(len(parents[0]) / 2)

            # Merge two together naively
            child = parents[0][0:split_point] + parents[1][split_point:]
            self.colonyParameters.append(ColonyParameters(*child))

    def runBatch(self):
        self.simResults = []

        # TODO: Can someone sort out multiprocessing (or some other library) so we can parallelize this?
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

        if self.enableRenderer:
            renderer = Renderer(sim)

        population = 0
        last_population = 0
        next_population_check_time = 10
        population_constant_for = 0

        dt = 0.05
        max_run_time = 10000
        for i in range(max_run_time):
            sim.runOnce(dt)

            if self.enableRenderer:
                renderer.render()

            # TODO: Make sure we don't get weird false positives here
            if sim.clock >= next_population_check_time:
                population = int(len(sim.ants))

                # Calculate percent diff
                if population + last_population == 0:
                    percent_diff = 0
                else:
                    percent_diff = abs(population - last_population) / ((population + last_population) / 2)

                # If it hasn't changed, start counting
                if abs(percent_diff) < 0.05:
                    population_constant_for += 1
                else:
                    population_constant_for = 0

                # If it hasn't changed for 10 seconds, we're done
                if population_constant_for > 10:
                    # print(f"Population leveled off after {sim.clock} seconds")
                    break

                last_population = population

        if i == max_run_time - 1:
            print("Hit runtime limit before population stabilized")

        if self.enableRenderer:
            renderer.quit()

        heapq.heappush(self.simResults, (population, index, colony_params))  # Use index to break ties

    def saveColonyParameters(self, path=None):
        if path is None:
            path = self.defaultSaveFile

        # TODO: Add hyperparameters
        data_dict = {"ants": [i.floatDict() for i in self.colonyParameters],
                     }

        file = open(path, 'w')
        yaml.dump(data_dict, file)
        file.close()

    def loadColonyParameters(self, path=None):
        if path is None:
            path = self.defaultSaveFile

        file = open(path)
        data = yaml.safe_load(file)
        file.close()

        # Read in ant data
        ants = data["ants"]
        self.colonyParameters = []
        for ant in ants:
            parameter_object = ColonyParameters(**ant)
            self.colonyParameters.append(parameter_object)
        self.batchSize = len(self.colonyParameters)
