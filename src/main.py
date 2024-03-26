#!/usr/bin/env python3

import time

from simulation import Simulation
from world import AntWorld
from ant import Ant
from renderer import Renderer

WIDTH_SCALE = 16
HEIGHT_SCALE = 9
RESOLUTION = 40

COLONY_START_SIZE = 100

X_Start = 320
Y_Start = 180


def main():
    world = AntWorld(WIDTH_SCALE, HEIGHT_SCALE, RESOLUTION)

    sim = Simulation(world)
    renderer = Renderer(sim)

    # Add ants
    for _ in range(COLONY_START_SIZE):
        sim.addAnt(Ant(), X_Start, Y_Start)

    dt = 0.05

    while renderer.running():
        # a = time.time()

        # Step the sim once
        sim.runOnce(dt)

        # Render
        renderer.render()

        # time.sleep(0.01)

        # print(time.time() - a)

    renderer.quit()


if __name__ == '__main__':
    main()
