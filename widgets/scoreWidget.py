import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import pyqtgraph as pg

class ScoreWidget(QtWidgets.QWidget):
    def  __init__(self, width, height):
        super().__init__( flags = QtCore.Qt.Window )

        #Create widgets
        self.accuracyLayout = QtWidgets.QHBoxLayout()
        self.accuracyLabel = QtWidgets.QLabel("Trafnie zarekomendowane utwory")
        self.accuracyLayout.addWidget(self.accuracyLabel)
        self.accuracyLayout.addStretch()
        self.accuracyGraphWidget = pg.PlotWidget(name='AccuracyPlot')
        self.accuracyPlot = self.accuracyGraphWidget.plot()
        # self.accuracyPlot.setDownsampling(mode='peak')
        self.accuracyPlot.setClipToView(True)
        self.accuracyLayout.addWidget(self.accuracyGraphWidget)
        self.accuracyLayout.addStretch()

        self.setLayout(self.accuracyLayout)

    def updateAccuracyPlot(self):
        self.accuracyPlot.setData(self.window().getState().getAccuracies())
        