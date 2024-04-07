#!/usr/bin/env python3


from faux_formicidae.simulation import Simulation
from faux_formicidae.world import AntWorld
from faux_formicidae.ant_colony import AntColony, ColonyParameters
from faux_formicidae.renderer import Renderer

WIDTH_SCALE = 16
HEIGHT_SCALE = 9
RESOLUTION = 40

COLONY_START_SIZE = 40

X_Start = 320
Y_Start = 180


def visualizeColony():
    world = AntWorld(WIDTH_SCALE, HEIGHT_SCALE, RESOLUTION)
    colony = AntColony(WIDTH_SCALE / 2, HEIGHT_SCALE / 2, ColonyParameters(1, 1, 1))

    sim = Simulation(world)
    sim.addAntColony(colony)
    renderer = Renderer(sim)

    dt = 0.05
    while renderer.running():
        sim.runOnce(dt)
        renderer.render()

    renderer.quit()


if __name__ == '__main__':
    visualizeColony()
