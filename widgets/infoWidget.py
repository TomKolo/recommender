import sys
from PyQt5 import QtWidgets, QtGui, QtCore

class InfoWidget(QtWidgets.QWidget):
    def  __init__(self, width, height):
        super().__init__( flags = QtCore.Qt.Window )
        self.width = width
        self.height = height
        self.initUI()

    def initUI(self):
        grid = QtWidgets.QGridLayout()
        grid.setRowStretch(0, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(3, 1)
        grid.setRowStretch(4, 1)
        grid.setRowStretch(5, 1)

        titleLabel = QtWidgets.QLabel('Jak korzystać z programu?')
        titleLabel.setObjectName('InfoTitleLabel')
        labelLayout = QtWidgets.QHBoxLayout()
        labelLayout.addStretch()
        labelLayout.addWidget(titleLabel)
        labelLayout.addStretch()

        exitButton = QtWidgets.QPushButton("Wróć do menu")
        exitButton.setObjectName("PlayerButton")    
        exitButton.setFixedSize(self.width*0.2, self.height*0.08)
        exitButton.clicked.connect(self.showMenu)
        exitLabelLayout = QtWidgets.QHBoxLayout()
        exitLabelLayout.addStretch()
        exitLabelLayout.addWidget(exitButton)

        aboutAlgorithmLabel = QtWidgets.QLabel('1. O algorytmie używanym w programie:')
        aboutAlgorithmLabel.setObjectName('InfoLabel')
        aboutAlgorithmLabelLayout = QtWidgets.QHBoxLayout()
        aboutAlgorithmLabelLayout.addWidget(aboutAlgorithmLabel)
        aboutAlgorithmLabelLayout.addStretch()

        collaborativeFilteringLabel = QtWidgets.QLabel('Collaborative filtering recommender algorithm - algorytm, który na podstawie analizy porównawczej użytkowników rekomenduje utwory\ndla danego użytkownika. Filtrowanie oparte na współpracy (​Collaborative filtering​) opiera się na założeniu, że ludzie, którzy zgodzili się\nw przeszłości, zgodzą się w przyszłości i że będą im podobać się piosenki, które lubili w przeszłości (podobni użytkownicy lubią\npodobne utwory). Na tej podstawie tworzy się macierz ocen, które każdy użytkownik wystawił lub wystawiłby każdemu z\nutworów, a następnie wyznacza się ten z najlepszym wynikiem. Opisywany system rekomendacyjny generuje\nrekomendacje, wykorzystując informacje dotyczące tylko ocen użytkowników.')
        collaborativeFilteringLabel.setObjectName('InfoSecLabel')
        collaborativeFilteringLabelLayout = QtWidgets.QHBoxLayout()
        collaborativeFilteringLabelLayout.addWidget(collaborativeFilteringLabel)

        editParamsLabel = QtWidgets.QLabel('2. Edytuj hiperparametry algorytmu, klikając na przycisk:')
        editParamsLabel.setObjectName('InfoLabel')
        grid.addWidget(editParamsLabel, 0, 1)

        editParamsButton = QtWidgets.QPushButton("Edytuj hiperparametry\nalgorytmu")
        editParamsButton.setObjectName("PlayerButton")    
        editParamsButton.setFixedSize(self.width*0.2, self.height*0.08)
        grid.addWidget(editParamsButton, 0, 2)

        emptyLabel = QtWidgets.QLabel('')
        emptyLabel.setObjectName('InfoLabel')
        grid.addWidget(emptyLabel, 0, 3)

        startRecommendationLabel = QtWidgets.QLabel('3. Rozpocznij proces rekomendacji, klikając na przycisk:')
        startRecommendationLabel.setObjectName('InfoLabel')
        grid.addWidget(startRecommendationLabel, 1, 1)

        startRecommendationButton = QtWidgets.QPushButton("Rozpocznij proces\nrekomendacji")
        startRecommendationButton.setObjectName("PlayerButton")    
        startRecommendationButton.setFixedSize(self.width*0.2, self.height*0.08)
        grid.addWidget(startRecommendationButton, 1, 2)

        rateLabel = QtWidgets.QLabel('4. Oceń poszczególne utwory w skali od 1 do 5')
        rateLabel.setObjectName('InfoLabel')
        grid.addWidget(rateLabel, 2, 1)

        afterRatingLabel = QtWidgets.QLabel('5. Po ocene wszystkich utworów możesz przejść do kolejnej iteracji,\nklikając na przycisk:')
        afterRatingLabel.setObjectName('InfoLabel')
        grid.addWidget(afterRatingLabel, 3, 1)

        afterRatingButton = QtWidgets.QPushButton("Następna iteracja >")
        afterRatingButton.setObjectName("PlayerButton")    
        afterRatingButton.setFixedSize(self.width*0.2, self.height*0.08)
        grid.addWidget(afterRatingButton, 3, 2)

        afterIter2Label = QtWidgets.QLabel('6. Po ocenie wszystkich utworów możesz w każdej chwili\nzakończyć proces rekomendacji i zobaczyć podsumowanie dotychczasowych iteracji,\nklikając na przycisk:')
        afterIter2Label.setObjectName('InfoLabel')
        grid.addWidget(afterIter2Label, 4, 1)

        afterIter2Button = QtWidgets.QPushButton("Zakończ i podsumuj")
        afterIter2Button.setObjectName("PlayerButton")    
        afterIter2Button.setFixedSize(self.width*0.2, self.height*0.08)
        grid.addWidget(afterIter2Button, 4, 2)

        layout = QtWidgets.QVBoxLayout()
        layout.addLayout(labelLayout)
        layout.addLayout(exitLabelLayout)
        layout.addLayout(aboutAlgorithmLabelLayout)
        layout.addLayout(collaborativeFilteringLabelLayout)
        
        layout.addLayout(grid)

        self.setLayout(layout)   
        self.show()

    def showMenu(self):
        self.window().showMenu()