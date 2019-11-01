import sys
import copy
import pandas as pd
import numpy as np
from sklearn.metrics import pairwise_distances
from logic.recommender import Recommender
from hyperparameters.hyperparametersService import HyperparameterService

"""
Class representing CollaborativeFiltering Recommender.

It inherits Recommender.
"""
class CollaborativeRecommender(Recommender):

    def __init__(self):
        pass


    def importDataset(self, objectsToReturn):
        self.songs = pd.read_csv("./data/song_dataset.csv",encoding="Latin1")
        Ratings = pd.read_csv("./data/songs_ratings.csv")

        Mean = Ratings.groupby(by="userId",as_index=False)['rating'].mean()
        Rating_avg = pd.merge(Ratings,Mean,on='userId')
        Rating_avg['adg_rating']=Rating_avg['rating_x']-Rating_avg['rating_y']
        print( Rating_avg.head())

        objectsToReturn.append(Rating_avg)
        objectsToReturn.append(Mean)


    def cleanTheData(self, objectsToReturn, Rating_avg):
        check = pd.pivot_table(Rating_avg,values='rating_x',index='userId',columns='song_id')
        print(check.head())
        final = pd.pivot_table(Rating_avg,values='adg_rating',index='userId',columns='song_id')
        print(final.head())

        # Replacing NaN by Song Average
        final_song= final.fillna(final.mean(axis=0))

        # Replacing NaN by User Average
        final_user = final.apply(lambda row: row.fillna(row.mean()), axis=1)
        print(final_song.head())
        print(final_user.head())

        objectsToReturn.append(check)
        objectsToReturn.append(final_song)
        objectsToReturn.append(final_user)


    def calculateSimilarityBetweenTheUsers(self, objectsToReturn, final_user, final_song):  
        # user similarity on replacing NAN by user avg
        b = HyperparameterService().callDistanceAlgorithm(final_user)

        np.fill_diagonal(b, 0 )
        similarity_with_user = pd.DataFrame(b,index=final_user.index)
        similarity_with_user.columns=final_user.index
        print(similarity_with_user.head())

        # user similarity on replacing NAN by item(song) avg
        cosine = HyperparameterService().callDistanceAlgorithm(final_song)
        np.fill_diagonal(cosine, 0 )
        similarity_with_song = pd.DataFrame(cosine,index=final_song.index)
        similarity_with_song.columns=final_user.index
        print(similarity_with_song.head())

        objectsToReturn.append(similarity_with_user)
        objectsToReturn.append(similarity_with_song)

    def findNneighbours(self, df, n):
        order = np.argsort(df.values, axis=1)[:, :n]
        df = df.apply(lambda x: pd.Series(x.sort_values(ascending=False)
               .iloc[:n].index, 
              index=['top{}'.format(i) for i in range(1, n+1)]), axis=1)
        return df

    
    def findNneighboursForEachUser(self, numberOfNeighbours, objectsToReturn, similarity_with_user, similarity_with_song):
        sim_user_N_user = self.findNneighbours(similarity_with_user,numberOfNeighbours)
        print(sim_user_N_user.head())

        sim_user_N_song = self.findNneighbours(similarity_with_song,numberOfNeighbours)
        print(sim_user_N_song.head())

        objectsToReturn.append(sim_user_N_user)
        objectsToReturn.append(sim_user_N_song)


    def getUserSimilarSongs(self, user1, user2, Rating_avg):
        common_songs = Rating_avg[Rating_avg.userId == user1].merge(
        Rating_avg[Rating_avg.userId == user2],
        on = "song_id",
        how = "inner" )
        return common_songs.merge( self.songs, on = 'song_id' )

    def userItemScore(self, user, item,
                        sim_user_N_song, final_song,
                        Mean, similarity_with_song):
        a = sim_user_N_song[sim_user_N_song.index==user].values
        b = a.squeeze().tolist()
        c = final_song.loc[:,item]
        d = c[c.index.isin(b)]
        f = d[d.notnull()]
        avg_user = Mean.loc[Mean['userId'] == user,'rating'].values[0]
        index = f.index.values.squeeze().tolist()
        corr = similarity_with_song.loc[user,index]
        fin = pd.concat([f, corr], axis=1)
        fin.columns = ['adg_score','correlation']
        fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
        nume = fin['score'].sum()
        deno = fin['correlation'].sum()
        final_score = avg_user + (nume/deno)
        return final_score


    def userItemRecommendedSongs(self, user, check, sim_user_N_song, Song_user, 
                                 final_song, Mean, similarity_with_song):
        Song_listened_by_user = check.columns[check[check.index==user].notna().any()].tolist()
        a = sim_user_N_song[sim_user_N_song.index==user].values
        b = a.squeeze().tolist()
        d = Song_user[Song_user.index.isin(b)]
        l = ','.join(d.values)
        Song_listened_by_similar_users = l.split(',')
        Songs_under_consideration = list(set(Song_listened_by_similar_users)-set(list(map(str, Song_listened_by_user))))
        Songs_under_consideration = list(map(str, Songs_under_consideration)) #was int in the first parameter before
        score = []
        for item in Songs_under_consideration:
            c = final_song.loc[:,item]
            d = c[c.index.isin(b)]
            f = d[d.notnull()]
            avg_user = Mean.loc[Mean['userId'] == user,'rating'].values[0]
            index = f.index.values.squeeze().tolist()
            corr = similarity_with_song.loc[user,index]
            fin = pd.concat([f, corr], axis=1)
            fin.columns = ['adg_score','correlation']
            fin['score']=fin.apply(lambda x:x['adg_score'] * x['correlation'],axis=1)
            nume = fin['score'].sum()
            deno = fin['correlation'].sum()
            final_score = avg_user + (nume/deno)
            score.append(final_score)
        data = pd.DataFrame({'song_id':Songs_under_consideration,'score':score})
        top_5_recommendation = data.sort_values(by='score',ascending=False).head(5)
        Song_Name = top_5_recommendation.merge(self.songs, how='inner', on='song_id')
        Song_Names = Song_Name.title.values.tolist()
        return Song_Names


    def getRecommendedSongs(self, Rating_avg, check, sim_user_N_song,
                           final_song, Mean, similarity_with_song):
        Rating_avg = Rating_avg.astype({"song_id": str})
        Song_user = Rating_avg.groupby(by = 'userId')['song_id'].apply(lambda x:','.join(x))
        user = 'bd4c6e843f00bd476847fb75c47b4fb430a06856' #the user for which we're recommending
        predicted_songs = self.userItemRecommendedSongs(user, check, sim_user_N_song,
                                                        Song_user, final_song, 
                                                        Mean, similarity_with_song)
        print("RECOMMENDATIONS for some user : ")
        for i in predicted_songs:
            print(i)

    def recommend(self):
        objectsToReturn = []
        self.importDataset(objectsToReturn)
        Rating_avg = copy.deepcopy(objectsToReturn[0])
        Mean = copy.deepcopy(objectsToReturn[1])

        objectsToReturn = []
        self.cleanTheData(objectsToReturn, Rating_avg)
        check = copy.deepcopy(objectsToReturn[0])
        final_user = copy.deepcopy(objectsToReturn[1])
        final_song = copy.deepcopy(objectsToReturn[2])

        objectsToReturn = []
        self.calculateSimilarityBetweenTheUsers(objectsToReturn, final_user, final_song)
        similarity_with_user = copy.deepcopy(objectsToReturn[0])
        similarity_with_song = copy.deepcopy(objectsToReturn[1])

        objectsToReturn = []
        numberOfNeighbours = HyperparameterService().getNumberOfNeighbours();
        self.findNneighboursForEachUser(numberOfNeighbours, objectsToReturn, similarity_with_user, similarity_with_song)
        sim_user_N_user = copy.deepcopy(objectsToReturn[0])
        sim_user_N_song = copy.deepcopy(objectsToReturn[1])

       # a = self.getUserSimilarSongs(370,86309, Rating_avg)
       # a = a.loc[ : , ['rating_x_x','rating_x_y','title']]
        #print(a.head())

        partialScore = self.userItemScore('bd4c6e843f00bd476847fb75c47b4fb430a06856', 'SOHIROU12AB01852AF', 
                                          sim_user_N_song, 
                                          final_song, 
                                          Mean,
                                          similarity_with_song)
        print("Partial score (u,i) is", partialScore)

        self.getRecommendedSongs(Rating_avg, check, sim_user_N_song, final_song, Mean, similarity_with_song)

