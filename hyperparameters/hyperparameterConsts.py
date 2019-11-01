import enum

class DistanceAlgorithm(enum.Enum):
    cosineSimilarity = 0
    cosineDistance = 1
    euclideanDistance = 2
    haversineDistance = 3
    manhattanDistance = 4

class NNeighbours:
    defaultN = 30


