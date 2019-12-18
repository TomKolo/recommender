import sys
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QVBoxLayout, QRadioButton, QInputDialog)
from hyperparameters.hyperparameterConsts import DistanceAlgorithm
from hyperparameters.hyperparametersState import CollaborativeHyperparametersState

class ParamsWidget(QtWidgets.QWidget):
    def  __init__(self, width, height):
        super().__init__( flags = QtCore.Qt.Window )
        self.width = width
        self.height = height
        self.currentlyChosenAlgorithm = CollaborativeHyperparametersState().distanceAlgorithm
        self.initUI()
        
    def initUI(self):
        grid = QGridLayout()
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 3)
        grid.setRowStretch(2, 3)
        grid.setRowStretch(3, 2)
        grid.setRowStretch(4, 3)
        grid.setRowStretch(5, 1)
        saveButton = QtWidgets.QPushButton("Zapisz i wyjdź")
        saveButton.setObjectName("PlayerButton")    
        saveButton.setFixedSize(self.width*0.2, self.height*0.08)
        saveButton.clicked.connect(self.saveAndExit)
        grid.addWidget(saveButton, 4, 1)

        exitButton = QtWidgets.QPushButton("Wróć do menu")
        exitButton.setObjectName("PlayerButton")    
        exitButton.setFixedSize(self.width*0.2, self.height*0.08)
        exitButton.clicked.connect(self.exitToMenu)
        grid.addWidget(exitButton, 1, 2)

        distanceLayout = self.getDistanceLayout()
        grid.addLayout(distanceLayout, 2, 1)

        neighboursLayout = self.getNeighboursLayout()
        grid.addLayout(neighboursLayout, 3, 1)
        
        self.setLayout(grid)   
        self.show()

    def exitToMenu(self):
        self.window().showMenu()

    def saveAndExit(self):
        CollaborativeHyperparametersState().distanceAlgorithm = self.currentlyChosenAlgorithm
        print("setting distance {}".format(self.currentlyChosenAlgorithm))
        n = self.nInput.text()
        if n and n.isdigit():
            print("setting number {}".format(n))
            CollaborativeHyperparametersState().numberOfNeighbours = int(n)
        else:
            self.nInput.setText(CollaborativeHyperparametersState().numberOfNeighbours.__str__())
        self.window().showMenu()

    def algorithmSelectionChanged(self):
        radiobutton = self.sender()
        if radiobutton.isChecked():
            self.currentlyChosenAlgorithm = radiobutton.algorithm

    def getDistanceLayout(self):
        distanceBox = QGridLayout()
        distanceLabel = QLabel('Wybierz metodę obliczania dystansu')
        distanceLabel.setObjectName('ParamLabel')
        distanceBox.addWidget(distanceLabel, 0, 0)

        canberraRadiobutton = QRadioButton("Canberra Distance")
        canberraRadiobutton.algorithm = DistanceAlgorithm.canberraDistance
        canberraRadiobutton.toggled.connect(self.algorithmSelectionChanged)
        self.setChecked(canberraRadiobutton)
        distanceBox.addWidget(canberraRadiobutton, 1, 0)

        euclideanRadiobutton = QRadioButton("Euclidean distance")
        euclideanRadiobutton.algorithm = DistanceAlgorithm.euclideanDistance
        euclideanRadiobutton.toggled.connect(self.algorithmSelectionChanged)
        self.setChecked(euclideanRadiobutton)
        distanceBox.addWidget(euclideanRadiobutton, 3, 0)

        cosineDistanceRadiobutton = QRadioButton("Cosine distance")
        cosineDistanceRadiobutton.algorithm = DistanceAlgorithm.cosineDistance
        cosineDistanceRadiobutton.toggled.connect(self.algorithmSelectionChanged)
        self.setChecked(cosineDistanceRadiobutton) 
        distanceBox.addWidget(cosineDistanceRadiobutton, 2, 0)

        manhattanRadiobutton = QRadioButton("Manhattan distance")
        manhattanRadiobutton.algorithm = DistanceAlgorithm.manhattanDistance
        manhattanRadiobutton.toggled.connect(self.algorithmSelectionChanged) 
        self.setChecked(manhattanRadiobutton)
        distanceBox.addWidget(manhattanRadiobutton, 4, 0)

        chebyshevRadiobutton = QRadioButton("Chebyshev distance")
        chebyshevRadiobutton.algorithm = DistanceAlgorithm.chebyshevDistance
        chebyshevRadiobutton.toggled.connect(self.algorithmSelectionChanged) 
        self.setChecked(chebyshevRadiobutton)
        distanceBox.addWidget(chebyshevRadiobutton, 5, 0)

        return distanceBox

    def setChecked(self, radiobutton):
        currentlyCheckedAlgorithm = CollaborativeHyperparametersState().distanceAlgorithm
        if (radiobutton.algorithm == currentlyCheckedAlgorithm):
            radiobutton.setChecked(True)
        else: 
            radiobutton.setChecked(False)

    def getNeighboursLayout(self):
        neighboursGrid = QVBoxLayout()
        label = QLabel('Wybierz n w n-nearest neighbours')
        label.setObjectName('ParamLabel')
        neighboursGrid.addWidget(label)

        self.nInput = QLineEdit()
        self.nInput.setObjectName('NInput')
        self.nInput.setValidator(QtGui.QIntValidator())
        self.nInput.setMaxLength(3)
        n = CollaborativeHyperparametersState().numberOfNeighbours.__str__()
        print("Current n: {}".format(n))
        self.nInput.setText(n)
        neighboursGrid.addWidget(self.nInput)

        return neighboursGrid
