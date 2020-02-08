import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
import pandas as pd
from widgets.musicWidget import MusicWidget
from download.sampleDownloader import SampleDownloader
import os 
from hyperparameters.hyperparameterConsts import IterationsNumber

class PlayerWidget(QtWidgets.QWidget):
    def  __init__(self, width, height):
        super().__init__( flags = QtCore.Qt.Window )
        self.width = width
        self.height = height
        self.liOfIterationSongsIds = []

        #Initialize widgets
        self.titleLabel = QtWidgets.QLabel()
        self.titleLabel.setObjectName("MenuLabel")
        self.subTitleLabel = QtWidgets.QLabel("Oceń poniższe utwory")
        self.subTitleLabel.setObjectName("PlayerLabel")

        self.menuButton = QtWidgets.QPushButton("Wyjście")
        self.menuButton.setObjectName("PlayerButton")    
        self.menuButton.setFixedSize(width*0.2, height*0.08)
        self.menuButton.clicked.connect(self.showMenu)

        self.nextIterationButton = QtWidgets.QPushButton("Następna iteracja >")
        self.nextIterationButton.setObjectName("PlayerButton")    
        self.nextIterationButton.setFixedSize(width*0.25, height*0.1)
        self.nextIterationButton.clicked.connect(self.showNextiteration)
        self.nextIterationButton.setEnabled(False)

        self.showScoreButton = QtWidgets.QPushButton("Zakończ i podsumuj")
        self.showScoreButton.setObjectName("PlayerButton")    
        self.showScoreButton.setFixedSize(width*0.25, height*0.1)
        self.showScoreButton.clicked.connect(self.showScore)
        self.showScoreButton.setEnabled(False)

        #Create layouts
        self.labelLayout = QtWidgets.QHBoxLayout()
        self.labelLayout.addStretch()
        self.labelLayout.addWidget(self.titleLabel)
        self.labelLayout.addStretch()

        self.joinedLabelsLayout = QtWidgets.QVBoxLayout()
        self.joinedLabelsLayout.addLayout(self.labelLayout)
        self.joinedLabelsLayout.addWidget(self.subTitleLabel)
        
        self.topBarLayout = QtWidgets.QHBoxLayout()
        self.topBarLayout.addStretch()
        self.topBarLayout.addStretch()
        self.topBarLayout.addLayout(self.joinedLabelsLayout)
        self.topBarLayout.addStretch()
        self.topBarLayout.addWidget(self.menuButton)

        self.bottomBarLayout = QtWidgets.QHBoxLayout()
        self.bottomBarLayout.addStretch()
        self.bottomBarLayout.addWidget(self.showScoreButton)
        self.bottomBarLayout.addWidget(self.nextIterationButton)
        self.bottomBarLayout.addStretch()

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.topBarLayout)

        self.__musicWidgets = []
        self.__songRatings = [-1 for x in range(0, 5)]

        self.layout.addLayout(self.bottomBarLayout)

        self.setLayout(self.layout)

        #Semafor pozwalający na jednoczesne odtwarzanie tylko jednego utworu
        #Zawiera pozycje aktualnie odtwarzającego audio widgetu
        self.__audioSemafor = -1


    def registerAudio(self, id):
        if self.__audioSemafor >= 0:
            self.__musicWidgets[self.__audioSemafor].stopPlaying()
        self.__audioSemafor = id

    def unregisterAudio(self):
        self.__audioSemafor = -1

    def songRated(self, id):
        self.__songRatings[id] = self.__musicWidgets[id].returnSongRating()
        if(self.__allSongsRated()):    
            self.showScoreButton.setEnabled(True)
            self.nextIterationButton.setEnabled(True)

    def appendNewUserRatings(self):
        userIdToRecommendId = self.window().getState().getRecommender().getUserIdToRecommend()
        #add rated songs by current user to songs_ratings
        for i in range(5):
            liToAppend = [{'userId':str(userIdToRecommendId),
                                'songId':self.liOfIterationSongsIds[i],
                                'rating':self.__songRatings[i]}]
            dataToAppend = pd.DataFrame(liToAppend)
            dataToAppend.to_csv("./data/filtered_songs_ratings.csv", mode='a', header=None, index=False) 

    def showScore(self):
        self.removeAllDownloadedSamples()
        self.window().getState().addIteration(self.__calculateItarationAccuracy())
        self.window().showScore()
    
    def showNextiteration(self):
        self.removeAllDownloadedSamples()
        self.window().getState().addIteration(self.__calculateItarationAccuracy())
        self.appendNewUserRatings()
        songs_titles, songs_artists, songs_ids = self.window().getState().getRecommender().recommend()
        self.initNewIteration(songs_titles, songs_artists, songs_ids)

    def showMenu(self):
        self.window().showMenu()

    def __allSongsRated(self):
        for x in range(5):
            if(self.__songRatings[x] == -1):
                return False
        return True

    def __calculateItarationAccuracy(self):
        if(self.__allSongsRated()):
            sum = 0
            for x in range(5):
                sum = sum + self.__songRatings[x]
            return sum/5.0

    def clearPlayerElements(self):
        for widget in self.__musicWidgets:
            self.layout.removeWidget(widget)
            widget.setParent(None)
        self.__musicWidgets.clear()
        self.showScoreButton.setEnabled(False)
        self.nextIterationButton.setEnabled(False)
        self.__songRatings = [-1 for x in range(0, 5)]

    def getFiveUniqueRandomSongs(self, recommender):
        ratings = pd.read_csv("./data/filtered_songs_ratings.csv")
        fiveUniqueRandomSongs = None
        numOfSongs = len(recommender.songs.index)
        allSongsRatedByUser = True
        while(allSongsRatedByUser):
            fiveUniqueRandomSongs = random.sample(range(1, numOfSongs), 5)
            someSongRatedByUser = False
            for x in range(5):
                songId = recommender.songs['songId'].values[fiveUniqueRandomSongs[x]]
                songListenedByRecUser = ratings.loc[(ratings['songId'] == songId) & 
                            (ratings['userId'] == recommender.getUserIdToRecommend())]
                # cannot add song which was rated by user before
                if songListenedByRecUser.empty == False:
                    someSongRatedByUser = True
                    break
            if someSongRatedByUser == False:
                allSongsRatedByUser = False
        return fiveUniqueRandomSongs

    def addRandomSongsInitially(self, width, height, recommender):
        self.bottomBarLayout.addWidget(self.nextIterationButton)
        self.nextIterationButton.setEnabled(False)
        iterationNumber = self.window().getState().getIterationNumber()
        text = "Iteracja {}/{}".format(iterationNumber, IterationsNumber.iterationsNumber);
        self.titleLabel.setText(text)
        self.clearPlayerElements()
        fiveUniqueRandomSongs = self.getFiveUniqueRandomSongs(recommender)
        downloader = SampleDownloader()
        self.liOfIterationSongsIds = []     
        for x in range(5):
            titleOfSong = recommender.songs['title'].values[fiveUniqueRandomSongs[x]]
            artistOfSong = recommender.songs['artistName'].values[fiveUniqueRandomSongs[x]]
            songId = recommender.songs['songId'].values[fiveUniqueRandomSongs[x]]
            self.liOfIterationSongsIds.append(songId)
            result = downloader.downloadSong(titleOfSong, artistOfSong, songId)
            if result:
                filePath = "./data/samples/{}.mp3".format(songId)
            else:
                filePath =  "./data/song1.mp3"
            self.__musicWidgets.append(MusicWidget(width*0.99, height*0.1, x, filePath, self, titleOfSong, artistOfSong))
            self.layout.addWidget(self.__musicWidgets[x])

    def initNewIteration(self, songs_titles, songs_artists, songs_ids):
        iterationNumber = self.window().getState().getIterationNumber()
        self.titleLabel.setText("Iteracja " + str(iterationNumber) + "/"+str(IterationsNumber.iterationsNumber))
        self.clearPlayerElements()

        if iterationNumber == IterationsNumber.iterationsNumber:
            self.setEnvironmentForLastIteration()

        downloader = SampleDownloader()
        self.liOfIterationSongsIds = []
        for x in range(5):
            titleOfSong = songs_titles[x]
            artistOfSong = songs_artists[x]
            songId = songs_ids[x]
            self.liOfIterationSongsIds.append(songId)
            result = downloader.downloadSong(titleOfSong, artistOfSong, songId)
            if result: 
                filePath = "./data/samples/{}.mp3".format(songId)
            else:
                filePath =  "./data/samples/song1.mp3"
            self.__musicWidgets.append(MusicWidget(self.width*0.99, self.height*0.1, x, filePath, self, titleOfSong, artistOfSong))
            self.layout.addWidget(self.__musicWidgets[x])
        self.layout.update();

    def removeAllDownloadedSamples(self):
        for file in os.scandir("./data/samples"):
            os.unlink(file.path)

    def setEnvironmentForLastIteration(self):
        self.layout.removeWidget(self.nextIterationButton)
        self.nextIterationButton.setParent(None)
        self.window().getState().setIterationNumber(0)
