import pandas as pd
import numpy as np

class DatasetLoader:

    def prepareDataset(self):
        userListenCounts = pd.read_table("./data/user_songs_listen_counts.txt", header = None)
        userListenCounts.columns = ['userId', 'song_id', 'listen_count']
        allUserListenCounts = userListenCounts.groupby(by = "userId")['listen_count'].sum().reset_index(name = 'all_listen_count')
        songs_ratings = pd.merge(userListenCounts, allUserListenCounts, on = 'userId')
        songs_ratings['rating'] = (( songs_ratings['listen_count'] / songs_ratings['all_listen_count'] ) * 5).apply(np.ceil)
        songs_ratings.drop(['listen_count', 'all_listen_count'], 1, inplace = True)
        songs_ratings.to_csv("./data/songs_ratings.csv", index = False)

    def prepareDataset2(self):
        userListenCounts = pd.read_table("./data/user_songs_listen_counts.txt", header = None)
        userListenCounts.columns = ['userId', 'song_id', 'listen_count']
        allUserListenCounts = userListenCounts.groupby(by = "userId")['listen_count'].max().reset_index(name = 'max_listen_count')
        songs_ratings = pd.merge(userListenCounts, allUserListenCounts, on = 'userId')
        songs_ratings['rating'] = np.select(
            [
                songs_ratings['listen_count'].between(0, 0.2 * songs_ratings['max_listen_count']), 
                songs_ratings['listen_count'].between(0.2 * songs_ratings['max_listen_count'], 0.4 * songs_ratings['max_listen_count']),
                songs_ratings['listen_count'].between(0.4 * songs_ratings['max_listen_count'], 0.6 * songs_ratings['max_listen_count']),
                songs_ratings['listen_count'].between(0.6 * songs_ratings['max_listen_count'], 0.8 * songs_ratings['max_listen_count']),
                songs_ratings['listen_count'].between(0.8 * songs_ratings['max_listen_count'], songs_ratings['max_listen_count']),
            ], 
            [
                1,
                2,
                3,
                4,
                5
            ], 
            default = 3
        )
        songs_ratings.drop(['listen_count', 'max_listen_count'], 1, inplace = True)
        songs_ratings.to_csv("./data/songs_ratings.csv", index = False)

    def loadDataset(self):
        songs = pd.read_csv("./data/song_dataset.csv", encoding = "Latin1")
        songsRatings = pd.read_csv("./data/songs_ratings.csv", encoding = "Latin1")
        return songs, songsRatings