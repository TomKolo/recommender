import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class ParamsWidget(QtWidgets.QWidget):
    def  __init__(self, width, height):
        super().__init__( flags = QtCore.Qt.Window )