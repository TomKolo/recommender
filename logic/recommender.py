import sys
"""
Class representing recommender.

It can be inherited by CollaborativeReccomender etc.
"""
class Recommender():

    def __init__(self, previousState, recommender):
         self._previousState = previousState
         self._iterationNo = 0
         self._accuracies = []
         self._reccomender = recommender

    