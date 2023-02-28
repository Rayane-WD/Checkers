from Objets_dames import Damier
import StyleSheet_dames as ssd
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt




class GamePage(QWidget):
   """
   Il s'agit de la page de jeu, l'endroit où les joueurs
   pourront mouvoir leur pièces et ainsi jouer aux Dames
   """
   def __init__(self, i=None):
      super().__init__()

      #On instancie le damier
      size_case = 80
      self.my_board = Damier(size_case, i)

      #Layout du damier
      layout_checkboard = QVBoxLayout()
      layout_checkboard.addWidget(self.my_board)

      #Bouton retour
      self.button_return = QPushButton("Retourner à l'écran titre")
      self.button_return.setStyleSheet(ssd.style_return_button)
      layout_checkboard.addWidget(self.button_return)
      layout_checkboard.setAlignment(self.button_return, Qt.AlignBottom | Qt.AlignRight)

      self.setLayout(layout_checkboard)


   def getCheckerBoard(self):
      return self.my_board.getInfo()



