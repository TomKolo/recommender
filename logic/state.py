import sys
"""
Class representing current state of recommendation.

It stores data needed for accuracy visualization, current recommender and previous states.

It holds current recommender!
"""
class State():

    def __init__(self, previousState, recommender):
         self._previousState = previousState
         self._iterationNo = 0
         self._accuracies = []
         self._reccomender = recommender

    def setRecommender(self, recommender):
        pass

    def getRecommnder(self):
        return self._reccomender

    def getPreviousState(self):
        return self._previousState

    def addIteration(self, accuracy):
        self._accuracies.append(accuracy)
        self._iterationNo = self._iterationNo + 1

    def getAccuracies(self):
        return self._accuracies
    