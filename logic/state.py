import sys
import pandas as pd

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

        ratings = pd.read_csv("./data/filtered_songs_ratings.csv")
        lastUserId = ratings.iloc[-1:].iloc[0][0]
        #usersIds for which recommendation process will be carried out are simple integers
        if lastUserId.isdigit(): 
            self._userToRecommendId = int(lastUserId) + 1
        else: 
            self._userToRecommendId = 0

    def setRecommender(self, recommender):
        pass

    def getRecommender(self):
        return self._reccomender

    def getPreviousState(self):
        return self._previousState

    def addIteration(self, accuracy):
        self._accuracies.append(accuracy)
        self._iterationNo = self._iterationNo + 1

    def getAccuracies(self):
        return self._accuracies

    def getIterationNumber(self):
        return self._iterationNo

    def getUserIdToRecommend(self):
        return self._userToRecommendId
    