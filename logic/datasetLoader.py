import pandas as pd
import matplotlib.pyplot as plt
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

    def drawPlots(self):
        userListenCounts = pd.read_table("./data/user_songs_listen_counts.txt", header = None)
        userListenCounts.columns = ['userId', 'song_id', 'listen_count']
        userUniqueSongsCount = userListenCounts.groupby(by = "userId")['listen_count'].count().reset_index(name = 'songs_count')
        totalListeners = userUniqueSongsCount.groupby(by = "songs_count")['userId'].count().reset_index(name = 'listeners_count')
        totalListeners.plot(kind = 'bar', x = 'songs_count', y = 'listeners_count')
        plt.xticks(np.arange(1, max(totalListeners['songs_count']) + 1, 50), np.arange(1, max(totalListeners['songs_count']) + 1, 50))
        totalListeners.plot(kind = 'bar', x = 'songs_count', y = 'listeners_count')
        plt.xlim(1, 101)
        plt.xticks(np.arange(1, 101, 11), np.arange(1, 101, 11))

        totalListens = userListenCounts.groupby(by = "userId")['listen_count'].sum().reset_index(name = 'total_listens')
        print(max(totalListens['total_listens']))
        uniqueListeners = totalListens.groupby(by = "total_listens")['userId'].count().reset_index(name = 'listeners_count')
        uniqueListeners.plot(kind = 'bar', x = 'total_listens', y = 'listeners_count')
        plt.xlim(1, 1001)
        plt.xticks(np.arange(0, 1000, 100), np.arange(0, 1000, 100))

        ratingsSummary = self.songsRatings.groupby(by = "rating")['userId'].count().reset_index(name = 'rating_count')
        print(ratingsSummary)
        ratingsSummary.plot(kind = 'bar', x = 'rating', y = 'rating_count')
        plt.show()


    def loadDataset(self):
        self.songs = pd.read_csv("./data/song_dataset.csv", encoding = "Latin1")
        self.songsRatings = pd.read_csv("./data/songs_ratings.csv", encoding = "Latin1")
        #self.drawPlots()
        return self.songs, self.songsRatings