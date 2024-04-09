#!/usr/bin/env python3

from faux_formicidae.simulation import Simulation
from faux_formicidae.world import AntWorld
from faux_formicidae.ant import Ant, AntMode
from faux_formicidae.renderer import Renderer

WIDTH_SCALE = 16
HEIGHT_SCALE = 9
RESOLUTION = 40

COLONY_START_SIZE = 40

X_Start = 1
Y_Start = 1


def giveFood(amount):
    print(f"Give food {amount}")
    return 0


def pathFindTest():
    world = AntWorld(WIDTH_SCALE, HEIGHT_SCALE, RESOLUTION)

    sim = Simulation(world)
    renderer = Renderer(sim)

    ant_1 = Ant(giveFood)
    ant_1.energy = 100000
    ant_1.antSpeed = 1
    ant_1.exploreDirection = 0.1
    ant_1.mode = AntMode.GO_HOME
    ant_1.setHomePosition(WIDTH_SCALE / 2.0, HEIGHT_SCALE / 2.0)

    sim.addAnt(ant_1, 1, 1)

    dt = 0.05
    while renderer.running():
        sim.runOnce(dt)
        renderer.render()

    renderer.quit()


if __name__ == '__main__':
    pathFindTest()
