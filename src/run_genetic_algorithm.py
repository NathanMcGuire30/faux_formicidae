"""
Test code to run the genetic algorithm
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from faux_formicidae.genetic_algorithm import GeneticAlgorithm
from run_visualization import visualizeColony


def run():
    g = GeneticAlgorithm()
    g.generateRandomColonies()
    g.runBatch()
    g.generateColoniesFromSimResults()
    g.runBatch()
    g.generateColoniesFromSimResults()
    g.runBatch()
    g.generateColoniesFromSimResults()
    g.runBatch()
    g.generateColoniesFromSimResults()
    g.enableRenderer = True
    print(g.simResults)
    g.runSimulationOnce(0)



if __name__ == '__main__':
    run()
