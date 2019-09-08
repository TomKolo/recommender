import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from widgets.musicWidget import MusicWidget

class PlayerWidget(QtWidgets.QWidget):
    def  __init__(self, width, height):
        super().__init__( flags = QtCore.Qt.Window )

        #Initialize widgets
        self.titleLabel = QtWidgets.QLabel("Iteracja 1")
        self.titleLabel.setObjectName("MenuLabel")
        self.subTitleLabel = QtWidgets.QLabel("Oceń poniższe utwory")
        self.subTitleLabel.setObjectName("PlayerLabel")

        self.menuButton = QtWidgets.QPushButton("Wyjście")
        self.menuButton.setObjectName("PlayerButton")    
        self.menuButton.setFixedSize(width*0.2, height*0.08)
        self.menuButton.clicked.connect(self.showMenu)

        self.nextIterationButton = QtWidgets.QPushButton("Przejdź do następnej itaracji")
        self.nextIterationButton.setObjectName("PlayerButton")    
        self.nextIterationButton.setFixedSize(width*0.2, height*0.1)
        self.nextIterationButton.clicked.connect(self.showNextiteration)
        self.nextIterationButton.setEnabled(False)

        self.showScoreButton = QtWidgets.QPushButton("Podsumowanie iteracji")
        self.showScoreButton.setObjectName("PlayerButton")    
        self.showScoreButton.setFixedSize(width*0.2, height*0.1)
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
        for x in range(5):
            self.__musicWidgets.append(MusicWidget(width*0.99, height*0.1, x, "./data/song1.mp3", self))
            self.layout.addWidget(self.__musicWidgets[x])

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
        self.__songRatings[id] = self.__musicWidgets[id].returnValue()
        if(self.__allSongsRated()):
            self.showScoreButton.setEnabled(True)
            self.nextIterationButton.setEnabled(True)

    def showScore(self):
        self.window().showScore()
    
    def showNextiteration(self):
        pass

    def showMenu(self):
        self.window().showMenu()

    def __allSongsRated(self):
        for x in range(5):
            if(self.__songRatings[x] == -1):
                return False
        return True