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
FOODOBJECT = 17

ENTITY_COLOR = {EMPTY: (255,255,255), WALL: (0,0,0)}
                # ANT: (139, 69, 19), HOMEPHEROMONE: (65, 105, 225),
                # FOODPHEROMONE: (34, 139, 34)}


# D: we need to quantify pheromone intensity unique to each type of pheromone

class CellData:

    def convert(self, data: int):
        isEmpty = self.entityExists(data, EMPTY)
        isWall = self.entityExists(data, WALL)
        isAnt = self.entityExists(data, ANT)
        isHome = self.entityExists(data, HOMEPHEROMONE)
        isFood = self.entityExists(data, FOODPHEROMONE)
        isFoodObj = self.entityExists(data, FOODOBJECT)
        return isEmpty, isWall, isAnt, isHome, isFood, isFoodObj
    
    def entityExists(self, data: int, entityType: int):
        return int(data) % entityType == 0

    def add(self, data:int, newVal):
        return data if self.entityExists(data, newVal) else int(data) * newVal
    
    def remove(self, data:int, remVal):
        return int(data) / remVal if self.entityExists(data, remVal) else data 

# Process:
    # Want to use a single array, so how can I fit multiple identifiers in a single cell
    # could use a concatenated string, but how does that fit into an np array
    # lets just use numbers and convert to a string, but that just lets us use 0-9
    # well how do we add/remove values to this list, we can't just add them
    # we can separate each digit by multiplying by 10 and adding the digit we want
    # well this means we can't use 0, if we use 0 we cant add anything
    # also how do we remove a value, have to convert to a string and remove
    # can we remove values any faster, what if we multiplied/divided
    # well if we have a lot of numbers then we can have common factors
    # well there are some numbers that don't have any common factors, prime numbers
    # we can set each entity to a unique prime number. 
    # We can check its existance by using the modulo operator
    # we can add it by multiplying
    # we can remove it by dividing
    # we just need to keep track of what entity matches to a prime number