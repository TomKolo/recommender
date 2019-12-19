import sys
import pandas as pd

"""
Class representing recommender.

It can be inherited by CollaborativeReccomender etc.
"""
class Recommender():

    def __init__(self):
        ratings = pd.read_csv("./data/filtered_songs_ratings.csv")
        lastUserId = ratings.iloc[-1:].iloc[0][0]
        #usersIds for which recommendation process will be carried out are simple integers
        if lastUserId.isdigit(): 
            self.userIdToRecommend = int(lastUserId) + 1
        else: 
            self.userIdToRecommend = 0
        print("Recommendation for user with ID: {}".format(self.userIdToRecommend))

    def getUserIdToRecommend(self):
        return self.userIdToRecommend

    