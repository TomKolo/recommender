import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class MenuWidget(QtWidgets.QWidget):
    def  __init__(self, width, height):
        super().__init__( flags = QtCore.Qt.Window )

        #Create widgets
        self.titleLayout = QtWidgets.QHBoxLayout()
        self.titleLayout.addStretch()
        self.titleLabel = QtWidgets.QLabel("System rekomendujący muzykę")
        self.titleLabel.setObjectName("MenuLabel")
        self.titleLayout.addWidget(self.titleLabel)
        self.titleLayout.addStretch()

        self.startButton = QtWidgets.QPushButton("Rozpocznij proces rekomendacji")
        self.startButton.setObjectName("MenuButton")
        self.startButton.setFixedSize(width*0.8, height*0.2)
        self.startButton.clicked.connect(self.startRecomendation)

        self.showParamsButton = QtWidgets.QPushButton("Edytuj hiperparametry algorytmu")
        self.showParamsButton.setObjectName("MenuButton")    
        self.showParamsButton.setFixedSize(width*0.8, height*0.2)
        self.showParamsButton.clicked.connect(self.showParams)

        self.infoButton = QtWidgets.QPushButton("O programie")
        self.infoButton.setObjectName("MenuButton") 
        self.infoButton.setFixedSize(width*0.8, height*0.2)
        self.infoButton.clicked.connect(self.showInfo)

        #Create main layout
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.addStretch()
        self.verticalLayout.addLayout(self.titleLayout)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.startButton)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.showParamsButton)
        self.verticalLayout.addStretch()
        self.verticalLayout.addWidget(self.infoButton)
        self.verticalLayout.addStretch()
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.addStretch()
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.addStretch()
        self.setLayout(self.horizontalLayout)

    def startRecomendation(self):
        self.window().startRecomendation()

    def showParams(self):
        self.window().showParams()

    def showInfo(self):
        self.window().showInfo()