import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

class DatasetLoader:

    def prepareDataset(self):
        userListenCounts = pd.read_csv("./data/filtered_listen_counts.csv")
        allUserListenCountsMax = userListenCounts.groupby(by = "userId")['listen_count'].max().reset_index(name = 'max_listen_count')
        allUserListenCountsAvg = userListenCounts.groupby(by = "userId")['listen_count'].mean().reset_index(name = 'avg_listen_count')
        songs_ratings = pd.merge(userListenCounts, allUserListenCountsMax, on = 'userId')
        songs_ratings = pd.merge(songs_ratings, allUserListenCountsAvg, on = 'userId')
        songs_ratings = songs_ratings.drop(songs_ratings[(songs_ratings.max_listen_count <= 5) | (songs_ratings.avg_listen_count <= 2)].index)
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
        userAvgRating = songs_ratings.groupby(by = "userId")['rating'].mean().reset_index(name = 'avg_rating')
        songs_ratings = pd.merge(songs_ratings, userAvgRating, on = 'userId')
        songs_ratings = songs_ratings.drop(songs_ratings[(songs_ratings.avg_rating <= 2) | (round(songs_ratings.avg_rating, 1) == 5.0)].index)
        songs_ratings.drop(['listen_count', 'max_listen_count', 'avg_listen_count', 'avg_rating'], 1, inplace = True)
        songs_ratings.to_csv("./data/songs_ratings.csv", index = False)

    def drawPlots(self):

        plt.rc('font', size=16) 
        #userSongsRatings = pd.read_csv("./data/filtered_ratings.csv")
        userMeanRating = self.songsRatings.groupby(by = "userId")['rating'].mean().round(1).reset_index(name = 'mean_rating')
        totalListeners = userMeanRating.groupby(by = "mean_rating")['userId'].count().reset_index(name = 'listeners_count')
        plot = totalListeners.plot(kind = 'bar', x = 'mean_rating', y = 'listeners_count', title = 'Średnia ocena piosenek dokonana przez użytkowników', legend = False)
        plot.set_xlabel("Średnia ocena")
        plot.set_ylabel("Liczba użytkowników")

        userListenCounts = pd.read_csv("./data/filtered_listen_counts.csv")
        userSongsMaxListenCount = userListenCounts.groupby(by = "userId")['listen_count'].max().reset_index(name = 'max_listen_count')
        totalListeners = userSongsMaxListenCount.groupby(by = "max_listen_count")['userId'].count().reset_index(name = 'listeners_count')
        plot = totalListeners.plot(kind = 'bar', x = 'max_listen_count', y = 'listeners_count', title = ' Maksymalna liczba odsłuchań piosenek przez użytkowników', legend = False)
        plt.xlim(0, 101)
        plt.xticks(np.arange(0, 101, 10), np.arange(1, 102, 10))
        plot.set_xlabel("Maksymalna ocena")
        plot.set_ylabel("Liczba użytkowników")

        ratingsSummary = self.songsRatings.groupby(by = "rating")['userId'].count().reset_index(name = 'rating_count')
        plot = ratingsSummary.plot(kind = 'bar', x = 'rating', y = 'rating_count', title='Liczba poszczególnych ocen', legend = False)
        plot.set_xlabel("Ocena")
        plot.set_ylabel("Liczba ocen")
        plt.show()


    def loadDataset(self):
        self.songs = pd.read_csv("./data/filtered_songs_data.csv", encoding = "Latin1")
        self.songsRatings = pd.read_csv("./data/filtered_songs_ratings.csv", encoding = "Latin1")
        #self.drawPlots()
        return self.songs, self.songsRatings