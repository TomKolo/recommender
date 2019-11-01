import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QVBoxLayout, QRadioButton)

class ParamsWidget(QtWidgets.QWidget):
    def  __init__(self, width, height):
        super().__init__( flags = QtCore.Qt.Window )
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.setSpacing(10)

        distanceLayout = self.getDistanceLayout()
        grid.addLayout(distanceLayout, 0, 0)

        neighboursLayout = self.getNeighboursLayout()
        grid.addLayout(neighboursLayout, 0, 1)
        
        self.setLayout(grid) 
        self.setGeometry(300, 300, 350, 300)   
        self.show()

    def onClicked(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            print("Checked is %s" % (radioButton.algorithm))

    def getDistanceLayout(self):
        distanceBox = QGridLayout()
        distanceLabel = QLabel('Wybierz metodę obliczania dystansu')
        distanceBox.addWidget(distanceLabel, 0, 0)

        cosineRadiobutton = QRadioButton("Cosine")
        cosineRadiobutton.setChecked(True)
        cosineRadiobutton.algorithm = "Cosine"
        cosineRadiobutton.toggled.connect(self.onClicked)
        distanceBox.addWidget(cosineRadiobutton, 1, 0)

        euclideanRadiobutton = QRadioButton("Euclidean")
        euclideanRadiobutton.algorithm = "Euclidean"
        euclideanRadiobutton.toggled.connect(self.onClicked) 
        distanceBox.addWidget(euclideanRadiobutton, 2, 0)
        return distanceBox


    def getNeighboursLayout(self):
        neighboursGrid = QGridLayout()
        label = QLabel('Wybierz k w k-nearest neighbours')
        neighboursGrid.addWidget(label, 0, 0)

        cousineRadiobutton = QRadioButton("Cousine")
        cousineRadiobutton.setChecked(True)
        cousineRadiobutton.algorithm = "Cousine"
        cousineRadiobutton.toggled.connect(self.onClicked)
        neighboursGrid.addWidget(cousineRadiobutton, 1, 0)

        euclideanRadiobutton = QRadioButton("Euclidean")
        euclideanRadiobutton.algorithm = "Euclidean"
        euclideanRadiobutton.toggled.connect(self.onClicked)
        neighboursGrid.addWidget(euclideanRadiobutton, 2, 0)
        return neighboursGrid