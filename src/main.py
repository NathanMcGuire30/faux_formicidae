#!/usr/bin/env python3

import time

from simulation import Simulation
from world import AntWorld
from ant import Ant
from visualization import visualizeWorldMatplotlib

if __name__ == '__main__':
    world = AntWorld(20, 30, 5)

    sim = Simulation(world)

    # Add 10 ants
    for i in range(20):
        sim.addAnt(Ant(), 1, 1)

    d_t = 0.1
    while True:
        sim.runOnce(d_t)
        visualizeWorldMatplotlib(sim)
        # time.sleep(d_t)
