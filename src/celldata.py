# we store the grid as an np array
# each cell has an integer value
# each possible entity has a unique prime number (wall, pheromones, other ants, etc)
# The value in the cell is the product of all the entities that are present in the cell
# So when we want to add an entity to a cell, we multiply the existing cell by the corresponding prime number 
# removing is just dividing
# since every number is prime, there won't be any common factors

## Examples ##
# 3 represents an empty cell (can't use 1 otherwise a cell would always return as empty)
# 5 represents a wall
# 7 represents an ant
# 143 represents both a food and home pheromone (11 * 13)
# 77 represents both another ant and a home peromone (7 * 11)

EMPTY = 3
WALL = 5
ANT = 7
HOMEPHEROMONE = 11
FOODPHEROMONE = 13

class CellData:

    def convert(self, data: int):
        isEmpty = self.entityExists(data, EMPTY)
        isWall = self.entityExists(data, WALL)
        isAnt = self.entityExists(data, ANT)
        isHome = self.entityExists(data, HOMEPHEROMONE)
        isFood = self.entityExists(data, FOODPHEROMONE)
        return isEmpty, isWall, isAnt, isHome, isFood
    
    def entityExists(self, data: int, entityType: int):
        return data % entityType == 0

    def add(self, data:int, newVal):
        return data * newVal
    
    def remove(self, data:int, remVal):
        return data / remVal
