from PyQt5.QtCore import QSize
#Objets Dames
th = 1
with open('theme.txt', 'r') as f:
   th = int(f.read())
   if th>2 : th=0

def darkening(c_hsv, n=15):
   """
   assombri une couleur en hsv.
   """
   new_hsv = c_hsv[:len(c_hsv)-3] + str(int(c_hsv[-3:-1])-n) + "%"
   return new_hsv

def setTheme(s):
   """
   Change le theme
   """
   if s == 'blue' :
      with open('theme.txt', 'w') as f:
         f.write(str(0))

   elif s == 'red' :
      with open('theme.txt', 'w') as f:
         f.write(str(1))

   elif s == 'pink' :
      with open('theme.txt', 'w') as f:
         f.write(str(2))




#Repères
style_mark_edges = "color : black ; font-size : 35px ; font: italic large Times New Roman"

#Cases vides
cl = ["189,100%,95%", "30,85%,90%", "332,70%,97%"][th]
cd = ["219,75%,69%", "356,100%,81%", "291,80%,92%"][th]
style_case_empty_light = f"background-color : hsv({cl})"
style_case_empty_dark = f"background-color : hsv({cd})"

#Cases occupÃ©es ('•' / '♕')

text_pawn = '•'
text_queen = '♕'
style_case_occ_dark_p1 = "QPushButton:enabled {"+\
                         f"{style_case_empty_dark} ; color : white ; font-size : 50px"+\
                        "} QPushButton:disabled {background-color: " +\
                        f"hsv({darkening(cd)}) ; "+\
                           "font-size : 50px ; color : white}"
style_case_occ_dark_p2 = "QPushButton:enabled {"+\
                         f"{style_case_empty_dark} ; color : black ; font-size : 50px"+\
                        "} QPushButton:disabled {background-color: " +\
                        f"hsv({darkening(cd)}) ; "+\
                           "font-size : 50px ; color : black}"

#Cases pointÃ©es ('◸', '◹' / '◺', '◿')
text_case_aimed_p1 = ['◸', '◹']
text_case_aimed_p2 = ['◺' , '◿']
ca = ["#81d5ab", "#4ecdc4", "#f2f1ef"][th]
cea = ["#ff4747", "#4d13d1", "#f0ff00"][th]
style_case_empty_aimed_dark = f"{style_case_empty_dark} ; color : {ca} ; font-size : 40px"

style_case_empty_eat_aimed_dark = "QPushButton:enabled {"+\
                                 f"{style_case_empty_dark} ; color : {cea} ; font-size : 40px"+\
                                 "} QPushButton:disabled {"+\
                                 f"{style_case_empty_dark} ;color : {cea} ; font-size : 40px ;" + "}"


#Page
color_background = ["#d8e9f5", "#f7ab79","#f1828d"][th]
bar_color = ["#295e83","#e54e07","#db0a5b"][th]

#Historique
style_title_history = "color : black ; font-size : 25px "
style_history = "color : black ; font-size : 22px"

cbr = ["#b74ea5","#b74ea5","#5333ed"][th]
who_plays_color = "font :italic 30px ; font-stlye : bold"
who_plays_color2 = "color : black ; font-size : 25px "
nb_btn_restants = f"color : {cbr} ; font-size : 25px "
chip_p1 = "color : white ; font-size : 100px"
chip_p2 = "color : black ; font-size : 100px"

crb = ["#2a729b","#e21f00","#f1828d"][th]
style_return_button = f"background-color : {crb}; color:white"

#Boutons
#Générale
size_general_button = QSize(150, 50)
maw, mah = 600, 50
miw, mih = 600, 50
cbe = ["#2a729b","#e9482e","#674172"][th]
cbd = ["#618699","#e58d7f","#d5b8ff"][th]
style_general_buttonE = f"background-color : {cbe} ; color : white ; font-size : 20px ; "+\
                        "border-radius: 10px ; border-style: solid; border-width:1px; "+\
                        f"max-width:{maw}px ; max-height:{mah}px ; min-width:{miw}px ; min-height:{mih}px"
style_general_buttonD = f"background-color : {cbd} ; color : white ; font-size : 20px ; "+\
                        "border-radius: 10px ; border-style: solid; border-width:1px; "+\
                        f"max-width:{maw}px ; max-height:{mah}px ; min-width:{miw}px ; min-height:{mih}px"


style_general_button = "QPushButton:enabled {"+\
                        f"{style_general_buttonE}"+\
                        "} QPushButton:disabled {"+\
                        f"{style_general_buttonD}"



