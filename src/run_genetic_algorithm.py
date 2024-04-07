"""
Test code to run the genetic algorithm
"""

from faux_formicidae.genetic_algorithm import GeneticAlgorithm


def run():
    g = GeneticAlgorithm()
    g.generateRandomColonies()
    g.runBatch()
    g.generateColoniesFromSimResults()


if __name__ == '__main__':
    run()
