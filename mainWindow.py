import sys
#import pandas as pd
from widgets.menuWidget import MenuWidget
from widgets.playerWidget import PlayerWidget
from widgets.scoreWidget import ScoreWidget
from widgets.infoWidget import InfoWidget
from widgets.paramsWidget import ParamsWidget
from PyQt5 import QtWidgets, QtGui, QtCore


# Główne okno przeglądarki grafów.
class RecommenderViewer( QtWidgets.QMainWindow ):

   
    def __init__(self, size):
        super().__init__( flags = QtCore.Qt.Window )

        #Set initial size
        self.setFixedSize(size.width()*0.6, size.height()*0.8)

        #Loading style sheet      
        self.loadStyleSheet()

        #Loading music - na razie milionsong a w zasadzie jego podzbiór (MillionSongSubset)
        # http://static.echonest.com/millionsongsubset_full.tar.gz 
        # Z powodu dużego rozmiaru tego pliku nie zalaczam go do repo, wypakujcie tara do folderu "data"
        self.loadMusic()

        #Creating widgets
        self.menuWidget = MenuWidget(size.width()*0.6, size.height()*0.8)
        self.playerWidget = PlayerWidget(size.width()*0.6, size.height()*0.8)
        self.scoreWidget = ScoreWidget(size.width()*0.6, size.height()*0.8)
        self.infoWidget = InfoWidget(size.width()*0.6, size.height()*0.8)
        self.paramsWidget = ParamsWidget(size.width()*0.6, size.height()*0.8)

        #initialization
        self.setWindowTitle( "System rekomendujący muzykę" )
        self.setCentralWidget(self.menuWidget)

    def loadStyleSheet(self):
        with open ("styleSheet.txt", "r") as stylesFile:
            styles=stylesFile.readlines()

        self.setStyleSheet("".join(styles))

    def loadMusic(self):
        #TODO
        pass

    def startRecomendation(self):
        self.setCentralWidget(self.playerWidget)

    def showParams(self):
        self.setCentralWidget(self.paramsWidget)

    def showInfo(self):
        self.setCentralWidget(self.infoWidget)

    def showScore(self):
        self.setCentralWidget(self.scoreWidget)

    def showMenu(self):
        self.setCentralWidget(self.menuWidget)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    w = RecommenderViewer(app.primaryScreen().size())
    w.show()

    sys.exit(app.exec_())
