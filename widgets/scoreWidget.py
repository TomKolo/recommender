import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg
import numpy as np

class ScoreWidget(QtWidgets.QWidget):
    def  __init__(self, width, height):
        super().__init__( flags = QtCore.Qt.Window )
        self.width = width
        self.height = height

        grid = QtWidgets.QGridLayout()
        grid.setRowStretch(0, 2)
        grid.setRowStretch(1, 2)
        
        exitButton = QtWidgets.QPushButton("Wróć do menu")
        exitButton.setObjectName("PlayerButton")    
        exitButton.setFixedSize(self.width*0.25, self.height*0.08)
        exitButton.clicked.connect(self.exitToMenu)
        grid.addWidget(exitButton, 0, 2, QtCore.Qt.AlignRight)
        
        self.accuracyGraphWidget = pg.PlotWidget(title = 'Średnia ocen utworów w kolejnych iteracjach')
        self.accuracyGraphWidget.setLabel('bottom','Numer iteracji')
        self.accuracyGraphWidget.setLabel('left','Średnia ocen')
        #self.accuracyGraphWidget.setBackground('w')
        grid.addWidget(self.accuracyGraphWidget, 1, 2)

        accuracyLayout = QtWidgets.QGridLayout()
        accuracyLayout.setRowStretch(0, 1)
        accuracyLayout.setRowStretch(1, 1)
        accuracyLayout.setRowStretch(2, 1)
        accuracyLayout.setRowStretch(3, 1)
        accuracyLabel = QtWidgets.QLabel('Skuteczność rekomendacji')
        accuracyLabel.setObjectName('AccuracyLabel')
        accuracyLayout.addWidget(accuracyLabel, 1, 1, QtCore.Qt.AlignHCenter)
        self.accuracyButton = QtWidgets.QPushButton()
        self.accuracyButton.setFixedSize(self.width*0.20, self.height*0.20)
        self.accuracyButton.setStyleSheet("background-color: #54d0d9; border: 2px solid black; border-radius: 60px; font-size: 35px; color: black;")
        self.accuracyButton.setEnabled(False)
        accuracyLayout.addWidget(self.accuracyButton, 2, 1, QtCore.Qt.AlignHCenter)
        grid.addLayout(accuracyLayout, 1, 1)

        self.setLayout(grid)   

    def updateAccuracyPlot(self):
        accuracyAvg = np.average(self.window().getState().getAccuracies())*20
        x = np.arange(1, len(self.window().getState().getAccuracies())+1).tolist()
        y = self.window().getState().getAccuracies()
        dx = [(value, str(value)) for value in list((range(1, len(self.window().getState().getAccuracies()) + 1)))]
        self.accuracyGraphWidget.getAxis('bottom').setTicks([dx, []])
        pen = pg.mkPen(color=(0, 0, 255), width = 3)
        self.accuracyPlot = self.accuracyGraphWidget.plot(x, y, symbol = 'o', pen=pen)
        self.accuracyButton.setText(str(round(accuracyAvg)) + "%")

    def exitToMenu(self):
        self.window().showMenu()