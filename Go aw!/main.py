import pyxel
import random
x = 500
y = 500
car_width = 20
car_height = 12
collisions = 0  # compte combien de fois il ya de collisions
game_over = False

liste_voiture = [[120,120,0.5],[240,240,1]]

for i in range(3):
    liste_voiture.append( [random.randint(0,200),random.randint(0,200),random.randint(1,3)] )
def draw_car(x, y, couleur_voiture, couleur_toit):
    # fromation de la voiture et de sa couleur
    pyxel.rect(x, y, 20, 8, couleur_voiture)
   
    # formation toit et sa couleur
    pyxel.rect(x + 6, y - 4, 8, 4, couleur_toit)
   
    # formation des roues
    pyxel.rect(x + 3, y + 8, 5, 3, 0)  
    pyxel.rect(x + 12, y + 8, 5, 3, 0)  

# formation de la voiture et du quadrant
def update():
    global x,y,collisions,game_over
   
    if pyxel.btn(pyxel.KEY_LEFT):
      x -= 5
    if pyxel.btn(pyxel.KEY_RIGHT):
        x += 5
    if pyxel.btn(pyxel.KEY_DOWN):
        y += 5
    if pyxel.btn(pyxel.KEY_UP):
        y -= 5
   
    if pyxel.btnp(pyxel.KEY_SPACE):
        x = start_x
        y = start_y

        for i in range(len(liste_voiture)):
            liste_voiture[i][0] = liste_depart[i][0]
            liste_voiture[i][1] = liste_depart[i][1]
        if game_over:
            collisions = 0
            game_over = False
    if x < 0:
        x = 0
    if x > largeur - car_width:
        x = largeur - car_width
    if y < 4:  # because top of car = y - 4
        y = 4
    if y > hauteur - 12:  # bottom of car = y + 8 + 3 = 11
        y = hauteur - 12
       
#Le ligne au dessous permettent de faire poursuivre ma voiture par la seconde
    for v in liste_voiture:
        if v[0] < x:
         v[0] += v[2]
        if v[0] > x:
         v[0] -= v[2]

        if v[1] < y:
         v[1] += v[2]
        if v[1] > y:
         v[1]-= v[2]

    for v in liste_voiture:
        if v[0] < 0:
            v[0] = 0
        if v[0] > largeur - 20:
            v[0] = largeur - 20
        if v[1] < 4:
            v[1] = 4
        if v[1] > hauteur - 12:
            v[1] = hauteur - 12
       
    for v in liste_voiture:
        if x < v[0] + 20 and x + 20 > v[0]:
            if y < v[1] + 12 and y + 12 > v[1]:
                collisions += 1   #il compte le nombre de collions
                x = 500
                y = 500
                if collisions >= 3:  #Lorsqu'il ya plus de 3 collisions il ya game over qui s'affiche
                    game_over = True
                   
start_x = x
start_y = y

liste_depart = []
for v in liste_voiture:
    liste_depart.append([v[0], v[1], v[2]])
#Les lignes au dessus permettent de limiter les voitures pour

def draw():
    pyxel.cls(7)  # couleur grise
    pyxel.text(200, 20, "Welcome to ESCAPE IT", 12)
    pyxel.text(408, 12, "Vies:", 0)
    pyxel.text(20, 40, "Appuie sur ESPACE pour recommencer", 0)
    pyxel.text(20, 60, "Si vous touchez les voitures 3 fois vous perdez", 0)
   
    vies = 3 - collisions   #Enleve une vie ou coeur a chaque collision
    start_x = largeur - 70
    y_pos = 10

    for i in range(vies):
        draw_heart(start_x + i * 12, y_pos, 8)
    if game_over:
        pyxel.text(250, 250, "GAME OVER", 8)
        pyxel.text(220, 270, "Appuie sur ESPACE pour recommencer", 0)
        return



    draw_car(x, y, 12, 8)  #taille de la voiture avec x= longueur=80, y=largeur=80
def draw_heart(x, y, color):
    # top bumps
    pyxel.rect(x + 1, y, 2, 2, color)
    pyxel.rect(x + 4, y, 2, 2, color)

    # middle
    pyxel.rect(x, y + 2, 8, 2, color)

    # bottom point
    pyxel.rect(x + 1, y + 4, 6, 2, color)
    pyxel.rect(x + 2, y + 6, 4, 2, color)    
    for v in liste_voiture:
        draw_car(v[0],v[1],9,10) #taille de la voiture avec x= longueur=120, y=largeur=120
   

# formation de la taille du quadrant et lancement du jeu
largeur = 500
hauteur = 500
pyxel.init(largeur, hauteur)
pyxel.run(update, draw)