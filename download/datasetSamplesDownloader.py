from download.sampleDownloader import SampleDownloader
import pandas as pd
import time

class DatasetSamplesDownloader:
    def downloadSamplesForSubset(self, startIndex, endIndex):
        self.songs = pd.read_csv("./data/filtered_songs_data.csv", encoding="Latin1")
        notFoundIds = []
        downloader = SampleDownloader()
        #print(self.songs.head())


        for i in range(startIndex, endIndex):
            result = downloader.downloadSong(self.songs['title'][i], self.songs['artistName'][i], self.songs['songId'][i])
            if not result:
                notFoundIds.append(self.songs['song_id'][i])
        fileName = "notFound{}-{}.txt".format(startIndex, endIndex)
        with open(fileName, 'w') as f:
            for item in notFoundIds:
                f.write("%s," % item)

        return notFoundIds

    def checkAvailableSongsForSubset(self, startIndex, endIndex):
        self.songs = pd.read_csv("./data/filtered_songs_data.csv", encoding="Latin1")
        notFoundIds = []
        foundIds = []
        downloader = SampleDownloader()
        fileName = "Found{}-{}.txt".format(startIndex, endIndex)
        with open(fileName, 'w') as f:
            for i in range(startIndex, endIndex):
                result = downloader.checkIfSongIsAvailable(self.songs['title'][i], self.songs['artistName'][i], self.songs['songId'][i])
                if result:
                    f.write("%s\n" % self.songs['songId'][i])              
        print("FINISHED FOR {} - {}\n".format(startIndex, endIndex))
        return foundIds