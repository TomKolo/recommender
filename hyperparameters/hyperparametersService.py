from hyperparameters.hyperparametersState import CollaborativeHyperparametersState
from hyperparameters.hyperparameterConsts import DistanceAlgorithm

class HyperparameterService:
    def callDistanceAlgorithm(self):
        chosenAlgorithm = CollaborativeHyperparametersState().distanceAlgorithm;
        if (chosenAlgorithm == DistanceAlgorithm.canberraDistance):
            return 'canberra'
        elif (chosenAlgorithm == DistanceAlgorithm.cosineDistance):
            return 'cosine'
        elif (chosenAlgorithm == DistanceAlgorithm.euclideanDistance):
            return 'euclidean'
        elif (chosenAlgorithm == DistanceAlgorithm.chebyshevDistance):
            return 'chebyshev'
        elif (chosenAlgorithm == DistanceAlgorithm.manhattanDistance):
            return 'cityblock'

    def getNumberOfNeighbours(self):
        return CollaborativeHyperparametersState().numberOfNeighbours