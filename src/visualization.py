#!/usr/bin/env python3

"""
Code to visualize the simulation

Currently makes a pretty bad visualization in matplotlib
"""

import numpy
import matplotlib.pyplot as plt

from simulation import Simulation


def visualizeWorldMatplotlib(sim: Simulation):
    world = sim.getWorld()
    ants = sim.getAnts()

    # Clear old stuff
    plt.clf()

    # Draw obstacles
    w = world.world.T
    plt.imshow(w)
    height = w.shape[0]

    # Limits
    plt.xlim([0, w.shape[1]])
    plt.ylim([0, w.shape[0]])

    # Draw ants
    for ant in ants:
        i, j = ant.getPositionPixelSpace()
        plt.plot(i, j, 'k.', markersize=10)

    # Matplotlib stuff
    plt.draw()
    plt.pause(0.01)
