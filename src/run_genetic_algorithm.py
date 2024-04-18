"""
Test code to run the genetic algorithm
"""
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

from faux_formicidae.genetic_algorithm import GeneticAlgorithm
from run_visualization import visualizeColony


def run():
    # Runs and saves one iteration
    g = GeneticAlgorithm(batch_size=5)

    g.loadColonyParameters()
    # Added this to retrain:
    g.generateRandomColonies()
    for i in range(10):
        print(f"\n\nRunning batch {i}")
        g.saveColonyParameters(batch_id=i)
        g.runBatch()
        g.saveColonyResults(i)
        g.generateColoniesFromSimResults()

    # So we can see it work based on the best results from the last run:
    # g.enableRenderer = False
    # print(g.simResults)
    # g.runSimulationOnce(0)
    g.saveColonyParameters()


if __name__ == '__main__':
    run()
