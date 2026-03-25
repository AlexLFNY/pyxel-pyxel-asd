import pyxel

pyxel.init(300, 250)
pyxel.load("cartes.pyxres")

# La carte à afficher — retourne=False = face cachée, True = face visible
carte = {'couleur': 'heart', 'valeur': 1, 'retourne': False}

def draw_card(carte, x, y):
    ''' carte: la carte à afficher
        x,y : position sur écran
    '''
    hauteur = 150
    longueur = 100

    # Carte retournée (dos visible)
    if not carte.get('retourne', True):
        pyxel.rect(x, y, longueur, hauteur, 1)
        pyxel.rectb(x, y, longueur, hauteur, 0)
        pyxel.rectb(x+4, y+4, longueur-8, hauteur-8, 7)
        return

    couleur = carte['couleur']
    couleur_x, couleur_y = 0, 0
    if couleur == "heart":
        couleur_x, couleur_y = 0, 48
    elif couleur == "diamond":
        couleur_x, couleur_y = 48, 24
    elif couleur == "club":
        couleur_x, couleur_y = 24, 24
    elif couleur == "spade":
        couleur_x, couleur_y = 24, 48

    color_border = 8 if couleur in ["heart", "diamond"] else 0
    number = carte['valeur']

    pyxel.rect(x, y, longueur, hauteur, 7)
    pyxel.rectb(x, y, longueur, hauteur, color_border)
    pyxel.rectb(x+12, y+12, longueur-24, hauteur-24, color_border)

    label = {1: 'A', 11: 'J', 12: 'Q', 13: 'K'}.get(number, str(number))
    pyxel.text(x+2, y+2, label, color_border)
    pyxel.text(x+longueur-6, y+hauteur-7, label, color_border)

    pyxel.blt(x, y+8, 0, couleur_x, couleur_y, 16, 16, scale=0.4)

    middle_x = x + longueur / 2 - 8
    middle_y = y + hauteur / 2 - 8
    if number == 1:
        pyxel.blt(middle_x, middle_y, 0, couleur_x, couleur_y, 16, 16, 7, scale=2)

def update():
    if pyxel.btnp(pyxel.KEY_SPACE):
        carte['retourne'] = not carte['retourne']
    if pyxel.btnp(pyxel.KEY_Q):
        pyxel.quit()

def draw():
    pyxel.cls(3)
    etat = "face visible" if carte['retourne'] else "face cachee"
    pyxel.text(80, 10, f"CARTE [{etat}]", 7)
    pyxel.text(70, 220, "ESPACE = retourner  Q = quitter", 7)
    draw_card(carte, 100, 30)

pyxel.run(update, draw)