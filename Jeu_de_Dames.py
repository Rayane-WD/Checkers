import sys, pickle
import GamePage_dames as Gp
import HomePage_dames as Hp
import StyleSheet_dames as ssd
import Text_dames as t
from PyQt5.QtWidgets import QApplication, QMainWindow,QToolBar, QAction,\
                           QMessageBox, QFileDialog, QInputDialog
from PyQt5.QtCore import QCoreApplication, QSize, QFile
from PyQt5.QtGui import QIcon, QKeySequence



class MainWindow(QMainWindow):
   def __init__(self):
      super().__init__()
      self.initUi()


      #On crée un menu
      self.menu_file = self.menuBar().addMenu("&Fichier")
      self.menu_history = self.menuBar().addMenu("&Historique")
      self.menu_theme = self.menuBar().addMenu("&Theme")
      self.menu_help = self.menuBar().addMenu("&Aide")
      self.menuBar().setStyleSheet("background-color : white; color : black")

      #On crée une toolbar
      self.myToolbar = QToolBar("Afficher la toolbar")
      self.myToolbar.setIconSize(QSize(16,16))
      self.myToolbar.setStyleSheet(f"background-color : {ssd.bar_color}")
      self.addToolBar(self.myToolbar)


      #Action 'Nouvelle partie'
      self.new_game_action = QAction(QIcon("assets/board-game-go.png"),"Nouvelle partie", self)
      self.new_game_action.setShortcut(QKeySequence("Ctrl+T"))
      self.new_game_action.triggered.connect(self.startNewGame)
      self.menu_file.addAction(self.new_game_action)
      self.myToolbar.addAction(self.new_game_action)

      #Action 'Charger une partie'
      self.load_action = QAction(QIcon("assets/blue-folder-network-horizontal-open.png"),"Charger une partie", self)
      self.load_action.setShortcut(QKeySequence("Ctrl+O"))
      self.load_action.triggered.connect(self.onpenGame)
      self.menu_file.addAction(self.load_action)
      self.myToolbar.addAction(self.load_action)

      #Action 'Sauvegarder'
      self.save_action = QAction(QIcon("assets/disk-return.png"),"Sauvegarder", self)
      self.save_action.setShortcut(QKeySequence("Ctrl+S"))
      self.save_action.triggered.connect(self.saveGame)
      self.menu_file.addAction(self.save_action)
      self.myToolbar.addAction(self.save_action)

      #Action 'avoir les précedents historiques'
      self.previous_history = QAction(QIcon("assets/a-magnifier-history.png"),"Afficher l'historique des déplacements d'une partie précédente", self)
      self.previous_history.setShortcut(QKeySequence("Ctrl+H"))
      self.previous_history.triggered.connect(self.dispPreviousHistory)
      self.menu_history.addAction(self.previous_history)

      #Action 'Sauvegarder l'historique des déplacements'
      self.save_history = QAction(QIcon("assets/a-magnifier--plus.png"),"Sauvegarder l'historique des déplacements", self)
      self.save_history.setShortcut(QKeySequence("Ctrl+P"))
      self.save_history.triggered.connect(self.saveHistory)
      self.menu_history.addAction(self.save_history)
      self.myToolbar.addAction(self.save_history)

      #Action 'Manuel'
      self.help_action = QAction(QIcon("assets/book-question.png"),"Obtenir de l'aide", self)
      self.help_action.setShortcut(QKeySequence("Ctrl+M"))
      self.help_action.triggered.connect(self.dispHelp)
      self.menu_help.addAction(self.help_action)
      self.myToolbar.addAction(self.help_action)

      #Action 'À  propos'
      self.aboutus_action = QAction(QIcon("assets/a-user-silhouette-question.png"),"À propos", self)
      self.aboutus_action.setShortcut(QKeySequence("Ctrl+W"))
      self.aboutus_action.triggered.connect(self.dispAboutUs)
      self.menu_help.addAction(self.aboutus_action)
      self.myToolbar.addAction(self.aboutus_action)

      #Action 'Bleu'
      self.theme_ocean = QAction(QIcon("assets/a-blue-flag.png"),"Thème Bleu Océan", self)
      self.theme_ocean.triggered.connect(self.changeThemeO)
      self.menu_theme.addAction(self.theme_ocean)

      #Action 'Rouge'
      self.theme_lava = QAction(QIcon("assets/a-red-flag.png"), "Thème Rouge Lave", self)
      self.theme_lava.triggered.connect(self.changeThemeL)
      self.menu_theme.addAction(self.theme_lava)

      #Action 'Violet'
      self.theme_candy = QAction(QIcon("assets/a-flag-pink.png"), "Thème Rose Bonbon", self)
      self.theme_candy.triggered.connect(self.changeThemeC)
      self.menu_theme.addAction(self.theme_candy)

      self.startHomePage()


   def initUi(self):
      self.setWindowTitle('Jeu de Dames')
      self.setGeometry(20,50,1350,900)
      self.setStyleSheet(f"background-color : {ssd.color_background}")

   def startGamePage(self,i=None):
      #On instancie la page de jeu
      self.game_page = Gp.GamePage(i)
      #On l'applique
      self.setCentralWidget(self.game_page)
      #On initialise le bouton retour
      self.game_page.button_return.clicked.connect(self.startHomePage)


   def startHomePage(self):
      #On instancie la page d'accueil
      self.home_page = Hp.HomePage()
      #On l'applique
      self.setCentralWidget(self.home_page)
      #On initialise le bouton mode PvP
      self.home_page.button_pvp.clicked.connect(self.startGamePage)

   def startNewGame(self):
      self.startGamePage()

   def onpenGame(self):
      #On affiche l'explorateur de fichier
      popup_file = QFileDialog()
      path, extension = popup_file.getOpenFileName(parent = None, caption = "Ouvrir un fichier",
                                                       filter = "Fichier (*.dam)")
      #On ouvre le fichier
      file = QFile(path)
      ok = file.open(QFile.ReadOnly)
      if ok :
         #On récupère les données
         with open (path, 'rb') as f :
            collected_info = pickle.load(f)
         file.close()
         self.startGamePage(collected_info)

      else : print("Problème lors du chargement du fichier")


   def saveGame(self):
      #On laisse l'utilisateur nommer et entreposer son fichier
      try :
         which_file = QFileDialog.getSaveFileName(self, 'Enregistrer la partie', filter = "Fichier (*.dam)" )

         #On l'enregistre
         with open( which_file[0],'wb') as file :
            game = self.game_page.getCheckerBoard()
            pickle.dump(game, file)

      except FileNotFoundError : print("Sauvegarde annulée")


   def dispHelp(self):
      popup = QMessageBox(QMessageBox.Information, "Comment jouer", t.text_how_to_play)
      popup.exec()

   def dispAboutUs(self):
      popup = QMessageBox(QMessageBox.Information, "Qui sommes nous ?", t.text_about_us)
      popup.exec()

   def dispPreviousHistory(self):
      #On affiche l'explorateur de fichier
      popup_file = QFileDialog()
      path, extension = popup_file.getOpenFileName(parent = None, caption = "Ouvrir un fichier",
                                                       filter = "Fichier (*.dam)")
      #On ouvre le fichier
      file = QFile(path)
      ok = file.open(QFile.ReadOnly)
      if ok :
         #On récupère les données
         with open (path, 'rb') as f :
            collected_info = pickle.load(f)
         file.close()

         c_i = [s for s in collected_info[3]]
         popup = QMessageBox(QMessageBox.Information, "Historique", "\n".join(c_i))
         popup.exec()

   def saveHistory(self):
      hist = self.game_page.getCheckerBoard()[3]
      #Popup pour nommer l'historique
      name, ok = QInputDialog.getText(self, "Enregistrer l'historique", "Nom de l'historique :")
      if ok:
         with open(f"historique - {name}.txt", "w") as f:
            f.write(str(hist))

      popup = QMessageBox(QMessageBox.Information, "Historique", "Enregistré avec succès !")
      popup.exec()


   def changeThemeO(self):
      return self.changeTheme("blue")

   def changeThemeL(self):
      return self.changeTheme("red")

   def changeThemeC(self):
      return self.changeTheme("pink")

   def changeTheme(self, s):
      popup = QMessageBox(QMessageBox.Question, "Changement de thème",t.text_u)
      popup.addButton(QMessageBox.Ok)
      popup.addButton(QMessageBox.Cancel)
      a = popup.exec()
      if a == QMessageBox.Ok:
         ssd.setTheme(s)





#Test si l'app tourne déjà
myApp = QCoreApplication.instance()
if myApp is None :
   myApp = QApplication(sys.argv)

#Creation d'une fenêtre
myWindow = MainWindow()
myWindow.show()
#Lancement de l'app
myApp.exec()
