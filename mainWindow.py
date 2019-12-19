import sys
#import pandas as pd
from widgets.menuWidget import MenuWidget
from widgets.playerWidget import PlayerWidget
from widgets.scoreWidget import ScoreWidget
from widgets.infoWidget import InfoWidget
from widgets.paramsWidget import ParamsWidget
from logic.state import State
from PyQt5 import QtWidgets, QtGui, QtCore
from logic.collaborativeRecommender import CollaborativeRecommender
from logic.datasetLoader import DatasetLoader

class RecommenderViewer( QtWidgets.QMainWindow ):
   
    def __init__(self, size):
        super().__init__( flags = QtCore.Qt.Window )

        #Set initial size
        self.setFixedSize(size.width()*0.6, size.height()*0.8)
        self.fixedWidth = size.width()*0.6
        self.fixedHeight = size.height()*0.8

        #Loading style sheet      
        self.loadStyleSheet()

        #Creating state object representing 

        #Loading music - na razie milionsong a w zasadzie jego podzbiór (MillionSongSubset)
        # http://static.echonest.com/millionsongsubset_full.tar.gz 
        # Z powodu dużego rozmiaru tego pliku nie zalaczam go do repo, wypakujcie tara do folderu "data"
        self.loadMusic()

        #Creating widgets
        self.menuWidget = MenuWidget(self.fixedWidth, self.fixedHeight)
        self.playerWidget = PlayerWidget(self.fixedWidth, self.fixedHeight)
        self.scoreWidget = ScoreWidget(self.fixedWidth, self.fixedHeight)
        self.infoWidget = InfoWidget(self.fixedWidth, self.fixedHeight)
        self.paramsWidget = ParamsWidget(self.fixedWidth, self.fixedHeight)

        #Creating stacked widget
        self.stack = QtWidgets.QStackedWidget()
        self.stack.addWidget(self.menuWidget)
        self.stack.addWidget(self.playerWidget)
        self.stack.addWidget(self.scoreWidget)
        self.stack.addWidget(self.infoWidget)
        self.stack.addWidget(self.paramsWidget)
        self.stack.setCurrentIndex(0)

        #initialization
        self.setWindowTitle( "System rekomendujący muzykę" )
        self.setWindowIcon(QtGui.QIcon("./data/icons/mainWindowIcon.png"))
        self.setCentralWidget(self.stack)

        self._state = None
        #There is one userIdToRecommend for one window (that implies one recommender for one window and so on one state for one window)
        self._state = State(self._state, CollaborativeRecommender())

    def loadStyleSheet(self):
        with open ("styleSheet.txt", "r") as stylesFile:
            styles=stylesFile.readlines()

        self.setStyleSheet("".join(styles))

    def loadMusic(self):
        # Generuje oceny na podstawie listen_count - wywołać tylko, jeżeli chcesz wygenerować ratingi
        # DatasetLoader().prepareDataset()
        # self.songs, self.songs_ratings = DatasetLoader().loadDataset()
        pass

    def showMenu(self):
        self.stack.setCurrentIndex(0)

    def startRecomendation(self):
        self.playerWidget.addRandomSongsInitially(self.fixedWidth, self.fixedHeight, self._state.getRecommender())
        self.stack.setCurrentIndex(1)

    def showScore(self):
        self.scoreWidget.updateAccuracyPlot()
        self.stack.setCurrentIndex(2)

    def showInfo(self):
        self.stack.setCurrentIndex(3)

    def showParams(self):
        self.stack.setCurrentIndex(4)

    def getState(self):
        return self._state


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    w = RecommenderViewer(app.primaryScreen().size())
    w.show()

    sys.exit(app.exec_())
