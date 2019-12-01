import sys, time
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia

class MusicWidget(QtWidgets.QWidget):
    def  __init__(self, width, height, id, path, parent, titleOfSong, artistOfSong):
        super().__init__( flags = QtCore.Qt.Window )
        self.__parent = parent
        self.UNHAPPY_WITH_SONG = 0
        self.HAPPY_WITH_SONG = 1
        self.UNSELECTED = -1
        self.HAPPY_SELECTED_ICON = "./data/icons/smilingFaceSelected.png"
        self.HAPPY_UNSELECTED_ICON = "./data/icons/smilingFace.png"
        self.SAD_SELECTED_ICON = "./data/icons/sadFaceSelected.png"
        self.SAD_UNSELECTED_ICON = "./data/icons/sadFace.png"
        self.setObjectName("MusicPlayer")
        self.setFixedSize(width, height)
        self.__id = id
        #self.label = QtWidgets.QLabel(path.split('/')[-1]) #getting title of song from path
        self.label = QtWidgets.QLabel(titleOfSong + " - " + artistOfSong)
        self.label.setObjectName("MusicLabel")
        self.playerButton = QtWidgets.QPushButton("")
        self.playerButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_MediaPlay")))
        self.playerButton.setObjectName("MusicButton")
        self.playerButton.clicked.connect(self.startPlaying)
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setValue(0)
        self.progressBar.setMaximum(100)
        self.progressBar.setObjectName("MusicProgressBar")

        self.happyButton = QtWidgets.QPushButton("")
        self.happyButton.setIcon(QtGui.QIcon(self.HAPPY_UNSELECTED_ICON))
        self.happyButton.clicked.connect(self.feelingHappy)
        self.sadButton = QtWidgets.QPushButton("")
        self.sadButton.setIcon(QtGui.QIcon(self.SAD_UNSELECTED_ICON))
        self.sadButton.clicked.connect(self.feelingSad)

        self.bottomLayout = QtWidgets.QGridLayout()
        self.bottomLayout.setColumnStretch(2, 5) #progress bar must be the longest column in musicWidget

        self.bottomLayout.addWidget(self.playerButton, 0, 0, 0, 1)
        self.bottomLayout.addWidget(self.progressBar, 0, 1, 0, 5)
        self.addRatingRadioButtons(self.bottomLayout)
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addLayout(self.bottomLayout)
        self.layout.setObjectName("MusicLayout")

        self.setLayout(self.layout)
        self.thread = Thread()
        self.progress = 0
        fullpath = QtCore.QDir.current().absoluteFilePath(path) 
        url= QtCore.QUrl.fromLocalFile(fullpath)
        content= QtMultimedia.QMediaContent(url)
        self.player = QtMultimedia.QMediaPlayer()
        self.player.setMedia(content)

        #Variable storing user choice (if he likes the song or not) -1 - not selected, 0 - doesnt like the song, 1 - likes it
        self.__songRating = self.UNSELECTED 

    def addRatingRadioButton(self, bottomLayout, ratingNum, columnPos):
        self.ratingRadioButton = QtWidgets.QRadioButton(str(ratingNum))
        self.ratingRadioButton.rating = ratingNum
        self.ratingRadioButton.toggled.connect(self.onRatingRBclicked)
        bottomLayout.addWidget(self.ratingRadioButton, 0, columnPos, 0, 1)

    def addRatingRadioButtons(self, bottomLayout):
        self.addRatingRadioButton(bottomLayout, 1, 6)
        self.addRatingRadioButton(bottomLayout, 2, 7)
        self.addRatingRadioButton(bottomLayout, 3, 8)
        self.addRatingRadioButton(bottomLayout, 4, 9)
        self.addRatingRadioButton(bottomLayout, 5, 10)

    def onRatingRBclicked(self):
        self.ratingRadioButton = self.sender()
        self.__songRating = self.ratingRadioButton.rating
        self.__parent.songRated(self.__id)

    def startPlaying(self):
        self.playerButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_MediaPause")))
        self.playerButton.disconnect()
        self.playerButton.clicked.connect(self.stopPlaying)
        self.thread.countChanged.connect(self.onCountChanged)
        self.thread.count = self.progress
        self.thread.pause = False
        self.thread.start()
        self.player.play()
        self.__parent.registerAudio(self.__id)

    def stopPlaying(self):
        self.playerButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_MediaPlay")))    
        self.playerButton.disconnect()
        self.playerButton.clicked.connect(self.startPlaying)
        self.thread.pause = True
        self.player.pause()
        self.__parent.unregisterAudio()
        
    def onCountChanged(self, value):
        self.progressBar.setValue((int(value)*1000.0)/(self.player.duration())*100)
        self.progress = value
        if int(value*1000.0) > int(self.player.duration()):
            self.playerButton.setIcon(self.style().standardIcon(getattr(QtWidgets.QStyle, "SP_MediaPlay")))
            self.playerButton.disconnect()
            self.playerButton.clicked.connect(self.startPlaying)
            self.progress = 0
            self.thread.pause = True

    def selectHappy(self):
        self.__songRating = self.HAPPY_WITH_SONG
        self.happyButton.setIcon(QtGui.QIcon(self.HAPPY_SELECTED_ICON))
        self.sadButton.setIcon(QtGui.QIcon(self.SAD_UNSELECTED_ICON))
        self.__parent.songRated(self.__id)

    def unselectHappy(self):
        self.__songRating = self.UNSELECTED
        self.happyButton.setIcon(QtGui.QIcon(self.HAPPY_UNSELECTED_ICON))
        self.__parent.songRated(self.__id)

    def selectSad(self):
        self.__songRating = self.UNHAPPY_WITH_SONG
        self.happyButton.setIcon(QtGui.QIcon(self.HAPPY_UNSELECTED_ICON))
        self.sadButton.setIcon(QtGui.QIcon(self.SAD_SELECTED_ICON))
        self.__parent.songRated(self.__id)

    def unselectSad(self):
        self.__songRating = self.UNSELECTED
        self.sadButton.setIcon(QtGui.QIcon(self.SAD_UNSELECTED_ICON))
        self.__parent.songRated(self.__id)

    def feelingHappy(self):
        if (self.__songRating == self.UNSELECTED or self.__songRating == self.UNHAPPY_WITH_SONG):
            self.selectHappy()
        elif (self.__songRating == self.HAPPY_WITH_SONG):
            self.unselectHappy()

    def feelingSad(self):
        if (self.__songRating == self.HAPPY_WITH_SONG or self.__songRating == self.UNSELECTED):
            self.selectSad()
        elif (self.__songRating == self.UNHAPPY_WITH_SONG):
            self.unselectSad()

    def returnSongRating(self):
        return self.__songRating

class Thread(QtCore.QThread):
    countChanged = QtCore.pyqtSignal(int)
    pause = False
    count = 0

    def run(self):
        while self.pause == False:
            self.count +=1
            time.sleep(1)
            self.countChanged.emit(self.count)
      
        
