"""
Test code to run the genetic algorithm
"""

from faux_formicidae.genetic_algorithm import GeneticAlgorithm


def run():
    # Runs and saves one iteration
    g = GeneticAlgorithm()
    g.loadColonyParameters()
    g.runBatch()
    g.generateColoniesFromSimResults()
    g.saveColonyParameters()


if __name__ == '__main__':
    run()
