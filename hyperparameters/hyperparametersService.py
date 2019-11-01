from hyperparameters.hyperparametersState import CollaborativeHyperparametersState
from hyperparameters.hyperparameterConsts import DistanceAlgorithm
from sklearn.metrics.pairwise import *

class HyperparameterService:
    def callDistanceAlgorithm(self, input):
        chosenAlgorithm = CollaborativeHyperparametersState().distanceAlgorithm;
        if (chosenAlgorithm == DistanceAlgorithm.cosineSimilarity):
            return cosine_similarity(input)
        elif (chosenAlgorithm == DistanceAlgorithm.cosineDistance):
            return cosine_distances(input)
        elif (chosenAlgorithm == DistanceAlgorithm.euclideanDistance):
            return euclidean_distances(input)
        elif (chosenAlgorithm == DistanceAlgorithm.haversineDistance):
            return haversine_distances(input)
        elif (chosenAlgorithm == DistanceAlgorithm.manhattanDistance):
            return manhattan_distances(input)

    def getNumberOfNeighbours(self):
        return CollaborativeHyperparametersState().numberOfNeighbours