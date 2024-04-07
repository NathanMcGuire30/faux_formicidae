#!/usr/bin/env python3

from faux_formicidae.simulation import Simulation
from faux_formicidae.world import AntWorld
from faux_formicidae.ant import Ant
from faux_formicidae.renderer import Renderer

WIDTH_SCALE = 16
HEIGHT_SCALE = 9
RESOLUTION = 40

COLONY_START_SIZE = 40

X_Start = 320
Y_Start = 180


def pathFindTest():
    world = AntWorld(WIDTH_SCALE, HEIGHT_SCALE, RESOLUTION)
    sim = Simulation(world)
    renderer = Renderer(sim, (X_Start, Y_Start))

    ant_1 = Ant(None)
    ant_1.exploreDirection = 0.5

    sim.addAnt(ant_1, X_Start, Y_Start)

    dt = 0.05
    while renderer.running():
        sim.runOnce(dt)
        renderer.render()

    renderer.quit()


if __name__ == '__main__':
    pathFindTest()