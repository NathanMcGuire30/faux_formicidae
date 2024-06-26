"""
Class to actually run the genetic algorithm
"""

import os
import time
import curses

import numpy as np
import yaml
import numpy
import heapq
import random
import multiprocessing

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
    progress = {}

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
        self.progress = {}

        # Use multiprocessing to parallelize stuff
        pool = multiprocessing.Pool()
        for i in pool.imap_unordered(self.runSimulationOnce, range(self.batchSize)):
            heapq.heappush(self.simResults, i)

        # Sort list
        self.simResults = [heapq.heappop(self.simResults) for i in range(len(self.simResults))]
        self.simResults.reverse()

    def runSimulationOnce(self, index, visualizing=False):
        # We do the same thing as the visualization script, just without the renderer

        print(f"  Starting colony {index}")

        colony_params = self.colonyParameters[index]

        world = AntWorld()
        sim = Simulation(world)

        colony = AntColony(world.width / 2, world.height / 2, colony_params)
        sim.addAntColony(colony)

        # I fixed the code bug in the steady-state checking and combined Vasilis' min length check together
        dt = 0.05
        min_iterations = np.random.uniform(2500, 5000)
        next_population_check_time = min_iterations * dt
        next_print_time = 0

        population = 0
        last_population = 0
        population_constant_for = 0

        if self.enableRenderer:
            renderer = Renderer(sim)
            if visualizing:
                i = 0
                while renderer.running():
                    if i % 1000 == 0:
                        print(len(sim.ants))
                    i += 1
                    sim.runOnce(dt)
                    renderer.render()
                renderer.quit()
                return None

        max_run_time = 10000
        for i in range(max_run_time):
            sim.runOnce(dt)

            if time.time() > next_print_time:
                # TODO: Figure out how to make a nice display output in a threadsafe way (I'm not sure its doable)
                next_print_time = time.time() + 1

            if self.enableRenderer:
                renderer.render()

            # Make sure we don't get weird false positives here
            #   Vasilis: To prevent this I am requiring the sim run for at least 2500 ticks. Might be overkill but
            #   it prevents a reward for just spawning all the ants at once with a lifespan of 11 ticks, which
            #   it liked to do

            # Randomize the number of ticks, to some range around 2500
            # it it does not bias towards one epoch length
            # print(sim.clock, next_population_check_time)
            if sim.clock >= next_population_check_time:
                population = int(len(sim.ants))
                # print(population)

                # Calculate percent diff
                if population + last_population == 0:
                    percent_diff = 0
                else:
                    percent_diff = abs(population - last_population) / ((population + last_population) / 2)

                # If it hasn't changed, start counting
                # TODO: potentially lower this value so the colony is required to keep a steadier population
                if abs(percent_diff) < 0.05:
                    population_constant_for += 1
                else:
                    population_constant_for = 0

                # If it hasn't changed for 10 seconds, we're done
                if population_constant_for > 10:
                    # print(f"Population leveled off after {sim.clock} seconds")
                    # print(f'Population leveled off after {i} iterations')
                    break

                last_population = population

                next_population_check_time = sim.clock + 1

            if i == max_run_time - 1:
                print(f"Index {index} hit runtime limit before population stabilized")

        if self.enableRenderer:
            renderer.quit()

        return population, index, colony_params
        # heapq.heappush(self.simResults, (population, index, colony_params))  # Use index to break ties

    def saveColonyParameters(self, path=None, batch_id=None):
        if batch_id is not None:
            path = os.path.join(PATH, "data", f"batch_{batch_id}.yaml")
        elif path is None:
            path = self.defaultSaveFile

        # TODO: Add hyperparameters
        data_dict = {"ants": [i.floatDict() for i in self.colonyParameters],
                     }

        file = open(path, 'w')
        yaml.dump(data_dict, file)
        file.close()

    def saveColonyResults(self, batch_id):
        path = os.path.join(PATH, "data", f"results_{batch_id}.yaml")

        results = []

        for result in self.simResults:
            population, index, params = result
            data_dict = {"population": population}
            data_dict.update(params.floatDict())

            while len(results) <= index:
                results.append({})

            results[index] = data_dict

        full_data = {"ants": results}

        file = open(path, 'w')
        yaml.dump(full_data, file)
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
