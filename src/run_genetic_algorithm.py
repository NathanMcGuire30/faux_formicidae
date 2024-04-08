"""
Test code to run the genetic algorithm
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from faux_formicidae.genetic_algorithm import GeneticAlgorithm
from run_visualization import visualizeColony


def run():
    # Runs and saves one iteration
    g = GeneticAlgorithm()

    g.loadColonyParameters()
    # Added this to retrain:
    # g.generateRandomColonies()
    # for i in range(4):
    #     print(i)
    #     g.runBatch()
    #     g.generateColoniesFromSimResults()

    # So we can see it work based on the best results from the last run:
    g.enableRenderer = True
    print(g.simResults)
    g.runSimulationOnce(0)
    g.saveColonyParameters()


if __name__ == '__main__':
    run()
