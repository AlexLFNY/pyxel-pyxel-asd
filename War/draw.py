import pyxel

def draw_card(carte, x, y):
    hauteur = 150
    longueur = 100

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
