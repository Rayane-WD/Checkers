import StyleSheet_dames as ssd
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout,QLabel
from PyQt5.QtCore import  Qt





class HomePage(QWidget):
   """
   Page d'accueil de l'application
   L'utilisateur pourra y choisir son mode de jeu
   """
   def __init__(self):
      super().__init__()

      #Label de bienvenue
      welcome_phrase = QLabel(self)
      welcome_phrase.setStyleSheet('color : #03558c; font-size : 50px ; font-stlye : bold')
      welcome_phrase.setAlignment(Qt.AlignCenter)
      welcome_phrase.setText("Bienvenue sur Le Jeu de Dames.\nChoisissez votre mode de jeu.\n\n")

      #Bouton qui permet de choisir le mode PvP
      self.button_pvp = QPushButton(" Mode PvP ")
      self.button_pvp.setStyleSheet(ssd.style_general_buttonE)

      #Bouton qui permet de choisir le mode PvE
      self.button_pve = QPushButton(" Mode PvE (En cours de construction ⚒) ")
      self.button_pve.setStyleSheet(ssd.style_general_buttonD)
      self.button_pve.setEnabled(False)

      #On crée un layout vertical
      self.myVerticalLayout = QVBoxLayout()
      self.myVerticalLayout.setAlignment(Qt.AlignCenter)
      self.myVerticalLayout.setSpacing(0)
      self.myVerticalLayout.addWidget(welcome_phrase)
      self.myVerticalLayout.addWidget(self.button_pvp)
      self.myVerticalLayout.addWidget(self.button_pve)

      #On ajoute le layout au widget
      self.setLayout(self.myVerticalLayout)



