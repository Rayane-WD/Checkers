import StyleSheet_dames as ssd
import Text_dames as t
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout, QVBoxLayout, QMessageBox, QLabel, QHBoxLayout, QScrollArea
from PyQt5.QtCore import Qt




class Damier(QWidget):
   """
   Objet Damier (100 cases).
   """

   def __init__(self, case_size, i=None):
      super().__init__()

      #Taille d'une case et d'un pion
      self.case_size = case_size
      self.pawn_size = case_size//3 * 5

      #Le layout du damier est une grille
      self.layout_checkerboard = QGridLayout()
      self.layout_checkerboard.setSpacing(0)

      #Liste des cases
      self.playable_cases_index = []
      self.all_cases_index = []

      #Dico des pions des 2 joueurs
      #Clef -> réf du widget || Valeur -> position sur le plateau
      self.p1_pawn_index = {}
      self.p2_pawn_index = {}
      self.queen_index = {}

      #Boutons qui peuvent produire une action (bouton courant, diags, joueur, mangeables)
      self.currents_btns = [None, [], None, {}]
      self.btns_which_can_take = []

      #L'historique : nJoueur-début-fin-prise (prise=1 sinon 0)
      self._history_game = []
      self.nbTurn = 0
      c_p = 2
      self.n_p = c_p

      #Initialisation du plateau
      self.intiCheckerboard()




# =============================================================================
#        c degeu mais c obligatoire...
# =============================================================================
      #Historique
      self.history = ScrollLayout(title="Historique")
      self.history.setStyleSheetTitle(ssd.style_title_history)
      self.history.setStyleSheetText(ssd.style_history)

      #Label joueur actuel
      label_title_actual_p = QLabel("\n\nJoueur : ")
      label_title_actual_p.setAlignment(Qt.AlignCenter)
      label_title_actual_p.setStyleSheet(ssd.who_plays_color)

      self.label_player = QLabel(ssd.text_pawn)
      self.label_player.setAlignment(Qt.AlignCenter)

      #Labels joueur 1
      label_title_j1 = QLabel("Joueur 1 \nPions restants : ")
      label_title_j1.setAlignment(Qt.AlignCenter)
      label_title_j1.setStyleSheet(ssd.who_plays_color2)

      self.label_nbPions_j1 = QLabel("")
      self.label_nbPions_j1.setAlignment(Qt.AlignCenter)
      self.label_nbPions_j1.setStyleSheet(ssd.nb_btn_restants)

      #Labels joueur 2
      label_title_j2 = QLabel("Joueur 2 \nPions restants : ")
      label_title_j2.setAlignment(Qt.AlignCenter)
      label_title_j2.setStyleSheet(ssd.who_plays_color2)

      self.label_nbPions_j2 = QLabel("")
      self.label_nbPions_j2.setAlignment(Qt.AlignCenter)
      self.label_nbPions_j2.setStyleSheet(ssd.nb_btn_restants)

      #Layout de l'historique
      layout_history = QVBoxLayout()
      layout_history.addLayout(self.history)
      layout_history.setContentsMargins(0,50,0,0)

      layout_history.addWidget(label_title_actual_p)
      layout_history.addWidget(self.label_player)
      layout_history.addWidget(label_title_j1)
      layout_history.addWidget(self.label_nbPions_j1)
      layout_history.addWidget(label_title_j2)
      layout_history.addWidget(self.label_nbPions_j2)


      #Layout principal de la page
      main_layout = QHBoxLayout()
      main_layout.addLayout(self.layout_checkerboard)

      main_layout.addLayout(layout_history)
      main_layout.setAlignment(layout_history, Qt.AlignTop)

      self.setLayout(main_layout)




      #Recup les données
      if i :
         #On réinitialise le plateau
         self.removeAllPawns()
         #j1
         for pos in i[0] :
            q = False
            if pos in i[2] : q = True
            self.becomeAPawn(pos, 1, queen = q)
         #J2
         for pos in i[1] :
            q = False
            if pos in i[2] : q = True
            self.becomeAPawn(pos, 2, queen = q)
         #H
         self._history_game = i[3]
         #nb Tours
         self.nbTurn = i[4]
         #current player
         c_p = i[5]


      #Les blancs commencent
      self.yourTurn(c_p)

# =============================================================================
#     Mode Développeur (appeler la méthode removeAllPawns pour avoir un damier vide)
## =============================================================================
      # self.removeAllPawns()
      # self.setCase((8,3), 1,True)
      # self.setCase((1,2), 2,False)
      
      
# =============================================================================
#     Fin du mode Développeur 
## =============================================================================




   def intiCheckerboard(self):
      """
      Initialise le damier et ses pions.
      """
      #Ajout des repères
      for x in range(1,11):
         marks_x = QLabel(chr(64+x))
         marks_x.setStyleSheet(ssd.style_mark_edges)
         marks_x.setAlignment(Qt.AlignCenter)
         self.layout_checkerboard.addWidget(marks_x,10,x)
      for y in range(10):
         marks_y = QLabel(str(y+1) + "  " )
         marks_y.setStyleSheet(ssd.style_mark_edges)
         marks_y.setAlignment(Qt.AlignCenter)
         self.layout_checkerboard.addWidget(marks_y,y,0)

      #Ajout des boutons
      for y in range(10):
         self.playable_cases_index.append([])
         self.all_cases_index.append([])
         for x in range(1,11):

            #Création du bouton
            button = QPushButton()
            button.setFixedSize(self.case_size, self.case_size)
            self.becomeAnEmptyCase(button, (y+x-1)%2)

            #Ajout du bouton au layout
            self.layout_checkerboard.addWidget(button, y, x)

            #Ajout du bouton à leur liste de réferencement (cases noires seulement)
            if (y+x-1)%2 : self.playable_cases_index[y].append(button)
            #Ajout de TOUT les boutons du jeu à  une liste de réferencement
            self.all_cases_index[y].append(button)

      #Ajout des pions à leur position initiale
      n_case = 0
      for idx_row, row in enumerate(self.all_cases_index) :
         for idx_col, btn in enumerate(row):

            #Cases de 0 à 19 (p2)
            if n_case <= 38 and (idx_row+idx_col)%2 == 1:
               self.becomeAPawn(btn, 2)
               #On enregistre la position des joueurs dans le même temps
               self.p2_pawn_index[btn] = (idx_col, idx_row)

            #Cases de 30 à 50 (p1)
            if n_case >= 60 and (idx_row+idx_col)%2 == 1:
               self.becomeAPawn(btn, 1)
               self.p1_pawn_index[btn] = (idx_col, idx_row)

            n_case += 1



   def setCase(self, pos, player, queen = False):
      """
      Permet de mettre un pion sur une case précise

      pos (tuple/list) -> position en x et y de la case actuelle
      player (int) -> numéro du joueur
      queen (bool) -> si l'on veut ajouter une reine
      """

      #On ajoute un pion sur une case précise
      case = self.getCaseAtPosition(pos, in_playable = True)
      self.becomeAPawn(case, player, queen)

   def removeAllPawns(self):
      """
      Supprime tout les pions du damier
      """
      list_remove = []
      #On ajoute les pions des 2 joueurs à la liste des boutons à supprimer
      for btn in self.p1_pawn_index.keys(): list_remove.append(btn)
      for btn in self.p2_pawn_index.keys(): list_remove.append(btn)

      #On supprime tout les pions des 2 joueurs
      for btn in list_remove : self.becomeAnEmptyCase(btn)




   def getPosition(self, btn):
      """
      Permet de trouver la position d'un bouton sur le damier.
      Retourne la position d'un bouton en x et y sous forme de tuple.

      btn (QPushButton) ->  bouton dont on cherche la position
      """

      #On parcourt chaque ligne à la recherche du bouton
      for idx_row, row in enumerate(self.all_cases_index) :
         try :
            idx_col = row.index(btn)
            return (idx_col, idx_row)

         except ValueError : pass

      #En cas de problèmes la 1ère case est retournée
      return (0, 0)

   def getCaseAtPosition(self, pos, in_playable = False):
      """
      Permet de trouver l'id d'une case à une certaine position sur le damier.
      Retourne l'id de la case.

      pos (tuple/list) -> position en x et y de la case actuelle
      """
      x, y = pos
      return self.all_cases_index[y][x]


   def getAllCasesPosition(self):
      """
      Retourne la positionde tout les pions
      """
      p1 = []
      p2 = []
      q1 = []
      q2 = []
      for btn in self.p1_pawn_index :
         p1.append(self.getPosition(btn))
         if btn in self.queen_index :
            q1.append(self.getPosition(btn))

      for btn in self.p2_pawn_index :
         p2.append(self.getPosition(btn))
         if btn in self.queen_index :
            q2.append(self.getPosition(btn))

      return p1, p2, q1, q2


   def getNotationPosition(self, btn):
      """
      Permet de trouver la position sous forme de notation d'un bouton sur le damier.
      Retourne la position d'un bouton en chiffre et lettre en un str.

      btn (QPushButton) ->  bouton dont on cherche la position
      """
      x, y = self.getPosition(btn)
      return chr(x+65) + str(y+1)


   def getPlayer(self, pawn):
      """
      Retourne le numero du joueur auquel appartient le pion.
      (1, 2 ou None si la case est sans pion)

      pawn (QPushButton) -> case (avec un pion de préference) dont on ccherche le propriétaire
      """
      if pawn in self.p1_pawn_index : return 1
      elif pawn in self.p2_pawn_index : return 2
      else : return None

   def isEmpty(self, case):
      """
      Permet de savoir si une case est vide ou non.

      case (QPushButton) -> case dont on veut vérifier la contenance
      """
      if case : return not bool(self.getPlayer(case))
      else : return None


   def isEnemy(self, pawn, p):
      """
      Permet de savoir si un pion est ennemi ou non.
      Retourne True si c'est un ennemi, False sinon

      pawn (QPushButton) -> case dont on veut vérifier l'amitié
      p (int) -> numéro du joueur
      """
      players =  [self.p1_pawn_index, self.p2_pawn_index]
      return pawn in players[p%2]


   def isQueen(self, pawn):
      """
      Permet de savoir si un pion est une dame ou non.
      Retourne True si c'est une dame, False sinon

      pawn (QPushButton) -> case dont on veut vérifier le statut
      """

      return pawn in self.queen_index


   def connectButton(self, btn, func = None):
      """
      Connecte un bouton à une fonction efficacement
      en supprimant le précédent slot connecté.
      Permet aussi de seulement déconnecter un bouton.

      btn (QPushButton) -> bouton à connecter (signal)
      func (function) -> fonction à connecter au bouton (slot)
      """

      #On déconnecte le bouton de sa précédente fonction
      try : btn.clicked.disconnect()
      except TypeError : pass

      #On le connecte à sa nouvelle fonction
      if func : btn.clicked.connect(func)



   def becomeAnEmptyCase(self, btn, c = 1):
      """
      Transforme une bouton en une case vide.

      btn (QPushButton) -> Bouton à transformer en case
      c (int) -> couleur de la case
      """
      styles = [ssd.style_case_empty_light, ssd.style_case_empty_dark]

      if btn:
         #On change son texte, son style, son slot et on le débloque
         btn.setText("")
         btn.setStyleSheet(styles[c])
         self.connectButton(btn, None)
         btn.setEnabled(True)

      #On le supprime du dictionnaire des joueurs
      try : del self.p1_pawn_index[btn]
      except KeyError: pass

      try : del self.p2_pawn_index[btn]
      except KeyError: pass

      try : del self.queen_index[btn]
      except KeyError: pass


   def becomeAPawn(self, btn, p, queen = False):
      """
      Transforme une bouton en un pion.

      btn (QPushButton) -> Bouton à transformer en pion
      p (int) -> numéro du joueur
      queen (bool) -> si le pion est une dame
      """
      styles = [ssd.style_case_occ_dark_p1, ssd.style_case_occ_dark_p2]
      players = [self.p1_pawn_index, self.p2_pawn_index]

      if type(btn) == tuple or type(btn) == list :
         btn = self.getCaseAtPosition(btn)

      #On change son texte, son style et son slot
      if queen :
         btn.setText(ssd.text_queen)
         self.queen_index[btn] = self.getPosition(btn)
      else :
         btn.setText(ssd.text_pawn)
      btn.setStyleSheet(styles[p-1])
      self.connectButton(btn, self.onClickPawn)

      #On oublie pas de l'ajouter dans le dictionnaire du joueur
      players[p-1][btn] = self.getPosition(btn)


   def becomeADiag(self, btn, sens, after_an_eat = False, no_bounds = False):
      """
      Transforme un bouton en une diag (=case de déplacement en diagonale).

      btn (QPushButton) -> Bouton à transformer en diag
      sens (int) -> sens de la case (0:gh / 1:dh / 2:gb / 3:db)
      after_an_eat (bool) -> si c'est une prise
      no_bounds (bool) -> si c'est une dame qui se déplace
      """
      texts = ssd.text_case_aimed_p1 + ssd.text_case_aimed_p2
      styles = [ssd.style_case_empty_aimed_dark, ssd.style_case_empty_eat_aimed_dark]

      #On change son texte, son style et son slot
      btn.setText(texts[sens])
      if not after_an_eat :
         btn.setStyleSheet(styles[0])
      else :
         btn.setStyleSheet(styles[1])
      self.connectButton(btn, self.onClickDiag)

      #On l'ajoute aux boutons courants
      self.currents_btns[1].append(btn)

   def clearAllDiags(self):
      """
      Permet de supprimer tout les diags actuellement affiché
      """
      for btn in self.currents_btns[1]:
         self.becomeAnEmptyCase(btn)


   def findCasesAround(self, case):
      """
      Permet de trouver les cases autour d'une case.
      Retourne les cases trouvées.

      case (QPushButton) -> case dont on cherche les voisins
      """
      cases_around = []

      #On obtient la position de la case
      case_pos = self.getPosition(case)
      case_x, case_y = case_pos[0], case_pos[1]

      #test pour cas des pions aux bords
      noEdges = lambda x,y : True if case_x + x >= 0 and case_x + x <= 9 and\
                                    case_y + y >= 0 and case_y + y <= 9 \
                                    else False

      #On en déduit les cases qui sont aux diagonales
      for y in range(-1,2,2):
         for x in range(-1,2,2):
            try :
               if noEdges(x,y):
                  cases_around.append(self.all_cases_index[case_y + y][case_x + x])
               else : cases_around.append(None)
            except IndexError: cases_around.append(None)

      return cases_around

   def findEatables(self, player, pos_or_pawn):
      """
      Retourne un dictionnaire des cases mengeables
      {id du diags résultant : (orientation, id de la case mangée)}

      player (int) -> numéro du joueur
      pos_or_pawn (tuple/list ou QPushButton) -> position en x et y de la case actuelle
      """
      # {id du diag résultant : (orientation, id de la case mangée)}
      dict_of_diags_after_an_eat = {}

      #On récupère l'id de la case
      if type(pos_or_pawn) == tuple or type(pos_or_pawn) == list :
         main_case = self.getCaseAtPosition(pos_or_pawn)
      else : main_case = pos_or_pawn

      #On récupère les cases alentours
      cases_around =  self.findCasesAround(main_case)

      #On parcours les cases alentours
      for i,eatable_btn in enumerate(cases_around) :
         #Si la case est enemie
         if self.isEnemy(eatable_btn, player) :
            #La case derrière l'ennemi est-elle vide ?
            case_behind_enemy = self.findCasesAround(eatable_btn)[i]
            #Si elle est vide
            if self.isEmpty(case_behind_enemy):
               dict_of_diags_after_an_eat[case_behind_enemy] = (i, eatable_btn)

      return dict_of_diags_after_an_eat


   def onClickPawn(self):
      """
      Permet d'afficher le choix de déplacement possible au joueur.
      """
      main_pawn = self.sender()
      cases_around = self.findCasesAround(main_pawn)
      player = self.getPlayer(main_pawn)

      #On supprimme les précédents diag
      for btn in self.currents_btns[1] : self.becomeAnEmptyCase(btn)

      #On enregistre les boutons courants
      self.currents_btns = [None, [], None, {}]
      self.currents_btns[0] = main_pawn
      self.currents_btns[2] = player

      #On change l'état des cases alentours
      #Cas d'une dame
      if self.isQueen(main_pawn) :

         #A/ on peut s'y déplacer (devant ou derrière, nombres de cases illimitées)
         diags_to_del_if_queen_can_eat = []
         a = False
         for i,btn in enumerate(cases_around):
            potential_diag = btn

            #Temps que la diagonale suivante est libre
            while self.isEmpty(potential_diag):
               self.becomeADiag(potential_diag, i)
               diags_to_del_if_queen_can_eat.append(potential_diag)
               potential_diag = self.findCasesAround(potential_diag)[i]

            #B/ on peut manger un pion adverse
            eating_diag = potential_diag
            #Si on tombe sur un ennemi
            if self.isEnemy(eating_diag, player):
               eating_diag = self.findCasesAround(eating_diag)[i]
               #Temps que la case suivante est libre
               while self.isEmpty(eating_diag):
                  a = True
                  self.currents_btns[3][eating_diag] = potential_diag
                  self.becomeADiag(eating_diag, i, after_an_eat=True, no_bounds=True)
                  eating_diag = self.findCasesAround(eating_diag)[i]

            #On supprime les diag de déplacement
            if a :
               for btn in diags_to_del_if_queen_can_eat : self.becomeAnEmptyCase(btn)

      #Cas d'un pion lambda
      else :


         #A/ on peut s'y déplacer (seulement devant)
         for i,btn in enumerate(cases_around[(player-1)*2:player*2]) :
            #On test si la case est vide et si il n'y a pas de prise prioritaire
            if self.isEmpty(btn) and main_pawn not in self.btns_which_can_take:
               self.becomeADiag(btn, (player-1)*2+i)

         #B/ on peut manger un pion adverse (devant ou derrière)
         if main_pawn in self.btns_which_can_take :
            #On récupère le dico des prises
            dict_of_take = self.findEatables(player, main_pawn)

            #On mets à jour les diag
            for diag in dict_of_take :
               sens = dict_of_take[diag][0]
               self.becomeADiag(diag, sens, after_an_eat=True)
               #On met à jour les boutons mangés
               pawn_eaten = dict_of_take[diag][1]
               self.currents_btns[3][diag] = pawn_eaten



   def onClickDiag(self):
      """
      Permet d'effectuer un déplacement.
      """
      main_pawn = self.sender()
      #Si il y a eu prise
      take = 0
      try :
         pawn_eaten = self.currents_btns[3][main_pawn]
         self.becomeAnEmptyCase(pawn_eaten)
         take = 1
      except KeyError : pass

      #On enregistre le déplacement dans l'historique
      start = self.getNotationPosition(self.currents_btns[0])
      end = self.getNotationPosition(main_pawn)
      self._history_game.append(f"{self.currents_btns[2]}-{start}-{end}-{take}")

      #On remplace le diag par un pion
      y = self.getPosition(main_pawn)[1]
      q = (self.currents_btns[0] in self.queen_index)
      q2 =   (y+self.currents_btns[2]==1) or (y+self.currents_btns[2]==11)
      self.becomeAPawn(main_pawn, self.currents_btns[2], q or q2)

      #On supprime le pion précédent
      self.becomeAnEmptyCase(self.currents_btns[0])

      #Les diags restants retournent à leur état d'origine
      for btn in self.currents_btns[1] :
         #Comme on ne sait pas quel diag a été choisi
         if btn and btn != main_pawn:
            self.becomeAnEmptyCase(btn)

      #Le tour se fini
      self.yourTurn(self.currents_btns[2])


   def getHistory(self):
      """
      Retourne l'historique du jeu.
      """

      return self._history_game


   def blockPlayer(self, p):
      """
      Bloque tous les pions d'un joueur.

      p (QPushButton) -> joueur dont les pions vont être bloqués
      """
      players = [self.p1_pawn_index, self.p2_pawn_index]
      for btn in players[p-1]:
         btn.setEnabled(False)

   def unblockPlayer(self, p):
      """
      Débloque tous les pions d'un joueur.

      p (QPushButton) -> joueur dont les pions vont être débloqués
      """
      players = [self.p1_pawn_index, self.p2_pawn_index]
      for btn in players[p-1]:
         btn.setEnabled(True)

   def blockAllExceptOnes(self, pawns, p1 = True, p2 = True):
      """
      Permet de bloquer tout les pions sauf un.

      pawn (list) -> pions à ne pas bloquer
      p1, p2 (bool) -> joueurs à bloquer (true)
      """
      #On bloque les joueurs
      if p1 : self.blockPlayer(1)
      else : self.unblockPlayer(1)

      if p2 : self.blockPlayer(2)
      else : self.unblockPlayer(2)

      #On débloque les pions
      for pawn in pawns : pawn.setEnabled(True)



   def yourTurn(self, actual_player):
      """
      Marque la fin d'un tour et le début d'un autre si aucune prise n'est possible.

      actual_player (int) -> joueur actuel à bloquer
      """
      players = [self.p1_pawn_index, self.p2_pawn_index]

      #On bloque le joueur actuel
      self.blockPlayer(actual_player)

      #On débloque l'autre
      new_player = (actual_player%2)+1
      self.unblockPlayer(new_player)

      #La liste des boutons courants redevient vide
      self.currents_btns = [None, [], None, {}]

      #On bloque tout les pions qui ne peuvent pas faire de prise
      #si au moins 1 seul le peut
      self.btns_which_can_take = []
      for btn in players[new_player-1]:
         #Si ce bouton peut faire une prise on le débloque
         if self.findEatables(new_player, btn):
            self.btns_which_can_take.append(btn)

      #Si des prises sont possibles
      if self.btns_which_can_take:
         self.blockAllExceptOnes(self.btns_which_can_take)

      #On actualise l'historique
      self.nbTurn+=1
      self.actualizeHistory(self.getHistory())
      #On actualise le nombre de pions des joueurs
      self.label_nbPions_j1.setText(str(self.getNbPawns(1)))
      self.label_nbPions_j2.setText(str(self.getNbPawns(2)))
      #On actualise le joueur actuel
      self.changeActualPlayer(new_player)

      self.n_p = new_player
      #Fin de partie
      g = self.isGameDone()
      if g:
         if g == 1 : self.winnerIs(1)
         elif g == 2 : self.winnerIs(2)
         else : self.winnerIs(0)





   def getNbPawns(self, p):
      """
      Retourne le nombre de pion restant d'un joueur.

      p (int) -> numéro du joueur
      """
      players = [self.p1_pawn_index, self.p2_pawn_index]

      if p==1 or p==2 : return len(players[p-1])

      else : return len(players[0]), len(players[1])

   def getTurn(self):
      """
      Renvoie le nombre de tour
      """
      return self.nbTurn

   def isGameDone(self):
      """
      Permet de savoir si la game est finie
      retourne le gagnant ou None.
      """
      #Test des 3 dames contre une
      q1 = 0
      q2 = 0
      for pawn in self.p1_pawn_index :
         if pawn in self.queen_index:
            q1+=1
      for pawn in self.p2_pawn_index :
         if pawn in self.queen_index:
            q2+=1

      if self.getNbPawns(1) == 0 :
         return 2

      if self.getNbPawns(2) == 0 :
         return 1

      if (q1>=3 and q2<=1) or (q2>=3 and q1<=1) :
         return 3

      else :
         return None


   def actualizeHistory(self, t_h):
      """
      Actualise l'historique

      t_h (list) -> liste de tous les coups d'un seul tour
      """
      if t_h :
         new_text=""
         #On affiche le numéro du tour
         new_text += str(self.nbTurn-1)+". "

         #On insert le contenu d'un tour à l'historique
         new_text += t_h[-1] + " ; "

         self.history.addText(new_text)

   def changeActualPlayer(self, p):
      """
      Change le label d'information du joueur actuel
      et refresh l'historique.
      """
      ssd_color = [ssd.chip_p1, ssd.chip_p2]
      self.label_player.setStyleSheet(ssd_color[p-1])


   def getInfo(self):
      """
      Renvoie les informations importantes du damier
      """
      info = []
      info.append(list(self.p1_pawn_index.values()))
      info.append(list(self.p2_pawn_index.values()))
      info.append(list(self.queen_index.values()))
      info.append(self._history_game)
      info.append(self.nbTurn)
      info.append(self.n_p%2+1)

      return info

   def winnerIs(self, p):
      """
      Affiche un qmessagebox du gagnant
      """
      pl = [t.text_w1, t.text_w2, t.text_null]
      popup = QMessageBox(QMessageBox.Information, "Partie terminée", pl[p-1])
      popup.exec()




class ScrollLayout(QVBoxLayout):
   """
   Layout scrollable
   """
   def __init__(self, title = "", content = ""):
      super().__init__()

      #Titre du scroll
      self.title = QLabel(title)
      #Info
      self.info = QLabel("(joueur - début - fin - prise)")
      self.info.setStyleSheet("font-size : 13px ; font: italic")
      #Contenu du scroll
      self.content = QLabel(content)
      self.content.setWordWrap(True)

      #Le widget
      self.widget = QWidget()

      #Le scroll
      self.scroll = QScrollArea()
      self.scroll.setMinimumSize(450,180)
      self.scroll.setWidget(self.widget)
      #Propriétés du scroll
      self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
      self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
      self.scroll.setWidgetResizable(True)

      #vbox du scroll
      vbox = QVBoxLayout()
      vbox.addWidget(self.content)

      #On ajoute un layout au widget
      self.widget.setLayout(vbox)

      #On ajoute les différents éléments à notre objet
      self.addWidget(self.title)
      self.addWidget(self.scroll)
      self.setAlignment(self.scroll, Qt.AlignCenter)
      self.addWidget(self.info)


   def setTitle(self, new_title):
      self.title.setText(new_title)

   def addText(self, new_text):
      s = self.getText() + "\n" + new_text
      self.content.setText(s)

   def getTitle(self):
      return self.title.text()

   def getText(self):
      return self.content.text()

   def setStyleSheetTitle(self, ss):
      self.title.setStyleSheet(ss)

   def setStyleSheetText(self, ss):
      self.content.setStyleSheet(ss)





