import sys
import copy
import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist, squareform
from logic.recommender import Recommender
from hyperparameters.hyperparametersService import HyperparameterService

"""
Class representing CollaborativeFiltering Recommender.

It inherits Recommender.
"""
class CollaborativeRecommender(Recommender):

    def __init__(self):
        super(CollaborativeRecommender, self).__init__()
        self.songs = pd.read_csv("./data/filtered_songs_data.csv",encoding="Latin1")

    def importAndScaleRatings(self, objectsToReturn):
        ratings = pd.read_csv("./data/filtered_songs_ratings.csv")

        average = ratings.groupby(by="userId",as_index=False)['rating'].mean()
        averageRatings = pd.merge(ratings,average,on='userId', suffixes=('', 'Scaled'))
        averageRatings['ratingSubstr']=averageRatings['rating']-averageRatings['ratingScaled']
        ratingsSubstr = pd.pivot_table(averageRatings,values='ratingSubstr',index='userId',columns='songId')

        ratingsSubstrAvgUser = ratingsSubstr.apply(lambda row: row.fillna(row.mean()), axis=1)

        objectsToReturn.append(ratingsSubstrAvgUser)
        objectsToReturn.append(ratings)


    def calcSimBetweenRecUserAndTheRest(self, objectsToReturn, ratingsSubstrAvgUser):
        metricMethod = HyperparameterService().callDistanceAlgorithm()
        listOfUsersIds = []
        listOfSimilaritiesToRecUser = []
        for index, row in ratingsSubstrAvgUser.iterrows():
            if(index != str(self.getUserIdToRecommend())):
                simBetweenRecUserAndOtherUser = pdist(ratingsSubstrAvgUser.reindex([str(self.getUserIdToRecommend()), index]), metricMethod)[0]
                listOfUsersIds.append(index)
                listOfSimilaritiesToRecUser.append(simBetweenRecUserAndOtherUser)

        dictOfSimilaritiesBetweenRecUserAndTheRest = {'userId': listOfUsersIds, 'similarityToRecUser': listOfSimilaritiesToRecUser}
        similaritiesBetweenRecUserAndTheRest = pd.DataFrame(dictOfSimilaritiesBetweenRecUserAndTheRest)
        print('SIMILARITIES TO USER WITHOUT SORT')
        print(similaritiesBetweenRecUserAndTheRest.head())
        similaritiesBetweenRecUserAndTheRest.sort_values(by=['similarityToRecUser'], inplace=True)
        objectsToReturn.append(similaritiesBetweenRecUserAndTheRest)

    def getFirstKneighborsForUser(self, objectsToReturn, k, similaritiesBetweenRecUserAndTheRest):
        similaritiesBetweenRecUserAndTheRest.sort_values(by=['similarityToRecUser'], inplace=True)
        firstNeighborsForUser = pd.DataFrame(similaritiesBetweenRecUserAndTheRest.head(k))
        objectsToReturn.append(firstNeighborsForUser)

    def getSongsTakenIntoProcess(self, objectsToReturn, firstNeighborsForUser, ratings):  
        songsRatedByNeighborsLi = []
        for index,row in firstNeighborsForUser.iterrows():
            #get rows with songs rated by one user from neighbors
            rowsWithRatedSongsByOneUser = pd.DataFrame(ratings.loc[ratings['userId'] == row['userId']])                                                                                            
            songsRatedByNeighborsLi.extend(rowsWithRatedSongsByOneUser['songId'].tolist())
        songsRatedByNeighborsLi = list(dict.fromkeys(songsRatedByNeighborsLi)) #delete duplicate songs
        
        #get rows with songs rated by user for which reccomendation will be carried out
        rowsWithRatedSongsByRecUser = pd.DataFrame(ratings.loc[ratings['userId'] == str(self.getUserIdToRecommend())])
        songsRatedByRecUserLi = rowsWithRatedSongsByRecUser['songId'].tolist() 

        # we dont want to recommend the same songs that user has rated before
        songsTakenIntoRecProcessLi = list(set(songsRatedByNeighborsLi) - set(songsRatedByRecUserLi))
        objectsToReturn.append(songsTakenIntoRecProcessLi)

    def getRecommendedSongs(self, songsTakenIntoRecProcessLi, firstNeighborsForUser, ratingsSubstrAvgUser):
        calcWeightedRatingsForSongs = []
        simBetweenUsersSum = 0
        firstLoopWithinNeighbors = True
        for songId in songsTakenIntoRecProcessLi:
            rUmultiSimUsum = 0
            for index,row in firstNeighborsForUser.iterrows():
                #get rating of some song given by user from neighbors
                rU = ratingsSubstrAvgUser.loc[[row['userId']], [songId]].values[0][0]
                #the inversion of distances because less distance implies higher similarity,
                #+ 0.000000001 because we dont want to divide by 0 (when similarity is 0)
                simU = 1 / (row['similarityToRecUser'] + 0.000000001)
                if firstLoopWithinNeighbors: simBetweenUsersSum += simU
                rUmultiSimUsum += rU * simU
            calcWeightedRatingForOneSong = rUmultiSimUsum/simBetweenUsersSum
            calcWeightedRatingsForSongs.append(calcWeightedRatingForOneSong)
            if firstLoopWithinNeighbors: firstLoopWithinNeighbors = False
        songsWithWeightedRatings = pd.DataFrame({'songId':songsTakenIntoRecProcessLi,'weightedRating':calcWeightedRatingsForSongs})

        #get five best songs recommended to user
        fiveBestSongsForRecUser = songsWithWeightedRatings.sort_values(by=['weightedRating'], ascending=False).head(5)
        print(fiveBestSongsForRecUser)

        predictedSongsTitles = []
        predictedSongsArtists = []
        predictedSongsIds = []
        for index,row in fiveBestSongsForRecUser.iterrows():
            predictedSongTitle = self.songs.loc[self.songs['songId'] == row['songId'], 'title'].iloc[0]
            predictedSongArtist = self.songs.loc[self.songs['songId'] == row['songId'], 'artistName'].iloc[0]
            predictedSongsTitles.append(predictedSongTitle)
            predictedSongsArtists.append(predictedSongArtist)
            predictedSongsIds.append(row['songId'])

        cnt = 0
        for i in predictedSongsTitles:
            print('{0} - {1} + ID: {2}'.format(i, predictedSongsArtists[cnt], predictedSongsIds[cnt]))
            cnt += 1

        return predictedSongsTitles, predictedSongsArtists, predictedSongsIds

    def recommend(self):
        objectsToReturn = []
        self.importAndScaleRatings(objectsToReturn)
        ratingsSubstrAvgUser = copy.deepcopy(objectsToReturn[0])
        ratings = copy.deepcopy(objectsToReturn[1])
        
        objectsToReturn = []
        self.calcSimBetweenRecUserAndTheRest(objectsToReturn, ratingsSubstrAvgUser)
        similaritiesBetweenRecUserAndTheRest = copy.deepcopy(objectsToReturn[0])

        objectsToReturn = []
        numberOfNeighbours = HyperparameterService().getNumberOfNeighbours();
        self.getFirstKneighborsForUser(objectsToReturn, numberOfNeighbours, similaritiesBetweenRecUserAndTheRest)
        firstNeighborsForUser = copy.deepcopy(objectsToReturn[0])

        objectsToReturn = []
        self.getSongsTakenIntoProcess(objectsToReturn, firstNeighborsForUser, ratings)
        songsTakenIntoRecProcessLi = copy.deepcopy(objectsToReturn[0])

        return self.getRecommendedSongs(songsTakenIntoRecProcessLi, firstNeighborsForUser, ratingsSubstrAvgUser)

