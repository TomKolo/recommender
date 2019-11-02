import pandas as pd

class DatasetLoader:

    def prepareDataset(self):
        userListenCounts = pd.read_table("./data/user_songs_listen_counts.txt", header = None)
        userListenCounts.columns = ['userId', 'song_id', 'listen_count']
        allUserListenCounts = userListenCounts.groupby(by = "userId")['listen_count'].sum().reset_index(name = 'all_listen_count')
        songs_ratings = pd.merge(userListenCounts, allUserListenCounts, on = 'userId')
        songs_ratings['rating'] = ( songs_ratings['listen_count'] / songs_ratings['all_listen_count'] ) * 5
        songs_ratings.drop(['listen_count', 'all_listen_count'], 1, inplace = True)
        songs_ratings.to_csv("./data/songs_ratings.csv", index = False)

    def loadDataset(self):
        songs = pd.read_csv("./data/song_dataset.csv", encoding = "Latin1")
        songsRatings = pd.read_csv("./data/songs_ratings.csv", encoding = "Latin1")
        return songs, songsRatings