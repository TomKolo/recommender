import enum

class DistanceAlgorithm(enum.Enum):
    canberraDistance = 0
    cosineDistance = 1
    euclideanDistance = 2
    chebyshevDistance = 3
    manhattanDistance = 4  #will add more soon

class NNeighbours:
    defaultN = 30

class IterationsNumber:
    iterationsNumber = 6


