import sys, time
from PyQt5 import QtWidgets, QtGui, QtCore, QtMultimedia

class MusicWidget(QtWidgets.QWidget):
    def  __init__(self, width, height, id, path, parent):
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
        self.label = QtWidgets.QLabel(path.split('/')[-1])
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
        self.bottomLayout.addWidget(self.playerButton, 0, 0, 0, 1)
        self.bottomLayout.addWidget(self.progressBar, 0, 1, 0, 5)
        self.bottomLayout.addWidget(self.happyButton, 0, 6, 0, 1)
        self.bottomLayout.addWidget(self.sadButton, 0, 7, 0, 1)

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
        self.__songValue = -1 


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
        self.__songValue = self.HAPPY_WITH_SONG
        self.happyButton.setIcon(QtGui.QIcon(self.HAPPY_SELECTED_ICON))
        self.sadButton.setIcon(QtGui.QIcon(self.SAD_UNSELECTED_ICON))
        self.__parent.songRated(self.__id)

    def unselectHappy(self):
        self.__songValue = self.UNSELECTED
        self.happyButton.setIcon(QtGui.QIcon(self.HAPPY_UNSELECTED_ICON))
        self.__parent.songRated(self.__id)

    def selectSad(self):
        self.__songValue = self.UNHAPPY_WITH_SONG
        self.happyButton.setIcon(QtGui.QIcon(self.HAPPY_UNSELECTED_ICON))
        self.sadButton.setIcon(QtGui.QIcon(self.SAD_SELECTED_ICON))
        self.__parent.songRated(self.__id)

    def unselectSad(self):
        self.__songValue = self.UNSELECTED
        self.sadButton.setIcon(QtGui.QIcon(self.SAD_UNSELECTED_ICON))
        self.__parent.songRated(self.__id)

    def feelingHappy(self):
        if (self.__songValue == self.UNSELECTED or self.__songValue == self.UNHAPPY_WITH_SONG):
            self.selectHappy()
        elif (self.__songValue == 1):
            self.unselectHappy()

    def feelingSad(self):
        if (self.__songValue == self.HAPPY_WITH_SONG or self.__songValue == self.UNSELECTED):
            self.selectSad()
        elif (self.__songValue == self.UNHAPPY_WITH_SONG):
            self.unselectSad()

    def returnValue(self):
        return self.__songValue

class Thread(QtCore.QThread):
    countChanged = QtCore.pyqtSignal(int)
    pause = False
    count = 0

    def run(self):
        while self.pause == False:
            self.count +=1
            time.sleep(1)
            self.countChanged.emit(self.count)
      
        
