#!/usr/bin/env python3


from simulation import Simulation
from world import AntWorld
from ant_colony import AntColony
from renderer import Renderer

WIDTH_SCALE = 16
HEIGHT_SCALE = 9
RESOLUTION = 40

COLONY_START_SIZE = 40

X_Start = 320
Y_Start = 180


def visualizeColony():
    world = AntWorld(WIDTH_SCALE, HEIGHT_SCALE, RESOLUTION)
    colony = AntColony(WIDTH_SCALE / 2, HEIGHT_SCALE / 2)

    sim = Simulation(world)
    sim.addAntColony(colony)
    renderer = Renderer(sim, (X_Start, Y_Start))

    dt = 0.05
    while renderer.running():
        colony.runOnce()
        sim.runOnce(dt)
        renderer.render()

    renderer.quit()


if __name__ == '__main__':
    visualizeColony()
