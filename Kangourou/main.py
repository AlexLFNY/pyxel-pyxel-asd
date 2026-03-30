import pyxel
# On importe la bibliothèque Pyxel.
# C’est elle qui permet de créer des jeux rétro avec des graphismes simples.

import random
# On importe le module random.
# Il sert à générer des nombres aléatoires, par exemple pour faire apparaître les cactus à des moments différents.


pyxel.init(500,200)
# On crée la fenêtre du jeu.
# Elle fait 500 pixels de large et 200 pixels de haut.

pyxel.load("kangourou.pyxres")
# On charge un fichier de ressources.
# Ce fichier contient les images (sprites) du kangourou et du cactus.


blob=0
# Variable compteur.
# Elle sert à mesurer le temps entre deux apparitions de cactus.

liste = [ [100],[250],[340]]
# Liste contenant les cactus.
# Chaque cactus est représenté par une liste avec sa position en x.
# Ici, on commence avec 3 cactus déjà placés.

apparition = random.randint(30,80)
# On choisit un nombre aléatoire entre 30 et 80.
# Ce nombre représente le nombre d’images avant qu’un nouveau cactus apparaisse.


gravite = 0.4
# Force de gravité.
# Elle fait redescendre le kangourou après un saut.

force_saut = -6
# Force du saut.
# La valeur est négative car dans Pyxel, monter correspond à diminuer y.

velocite_y = 0
# Vitesse verticale actuelle du kangourou.
# Elle change pendant le saut.

au_sol = True
# Indique si le kangourou est au sol.
# Permet d’empêcher de sauter dans les airs.


game_over = False
# Variable qui indique si la partie est terminée.

score = 0
# Score du joueur.
# Il augmente avec le temps de survie.

vitesse = 3
# Vitesse des cactus.
# Elle va augmenter progressivement pour rendre le jeu plus difficile.



def reset_game():
# Cette fonction sert à recommencer la partie sans fermer la fenêtre.

    global liste, blob, apparition, y1, velocite_y, au_sol, game_over, score, vitesse
    # On indique qu’on va modifier des variables globales.

    liste = [[500]]
    # On recrée une liste avec un seul cactus placé à droite de l’écran.

    blob = 0
    # On remet le compteur à zéro.

    apparition = random.randint(30,90)
    # On choisit un nouveau temps aléatoire avant le prochain cactus.

    y1 = 150
    # On remet le kangourou au niveau du sol.

    velocite_y = 0
    # On remet sa vitesse verticale à zéro.

    au_sol = True
    # Le kangourou est de nouveau au sol.

    score = 0
    # On remet le score à zéro.

    vitesse = 3
    # On remet la vitesse normale.

    game_over = False
    # On relance la partie.



def update():
# Cette fonction est appelée à chaque image du jeu.
# Elle gère toute la logique (mouvement, collisions, score…)

    global blob, apparition, velocite_y, au_sol, x1, y1, game_over, score, vitesse
    # Permet de modifier les variables globales.

    if game_over:
    # Si la partie est terminée

        if pyxel.btnp(pyxel.KEY_E):
        # Si le joueur appuie sur la touche E (une seule fois)

            reset_game()
            # On relance la partie

        return
        # On arrête la fonction pour que le jeu reste figé


    score += 1
    # Le score augmente à chaque image.
    # Plus le joueur survit longtemps, plus le score est élevé.

    if score % 200 == 0:
    # Tous les 200 points

        vitesse += 0.5
        # On augmente la vitesse pour rendre le jeu plus difficile


    blob += 1
    # On augmente le compteur

    if blob == apparition:
    # Si on atteint le moment d’apparition

        liste.append([500])
        # On ajoute un nouveau cactus à droite

        blob = 0
        # On remet le compteur à zéro

        apparition = random.randint(30,90)
        # On choisit un nouveau délai aléatoire


    for cactus in liste:
    # Pour chaque cactus

        cactus[0] -= vitesse
        # On le déplace vers la gauche (effet de déplacement du jeu)


    if y1 == 150:
    # Si le kangourou est au sol

        au_sol = True
        # Il peut sauter


    if pyxel.btn(pyxel.KEY_UP) and au_sol:
    # Si on appuie sur la flèche du haut et qu’il est au sol

        velocite_y = force_saut
        # On applique la vitesse de saut

        au_sol = False
        # Il n’est plus au sol


    if not au_sol:
    # Si le kangourou est en l’air

        y1 += velocite_y
        # On modifie sa position verticale

        velocite_y += gravite
        # On applique la gravité


    for cactus in liste:
    # On vérifie la collision avec chaque cactus

        kangourou_gauche = x1
        kangourou_droite = x1 + 22
        kangourou_haut = y1
        kangourou_bas = y1 + 28
        # On définit les bords du kangourou

        cactus_gauche = cactus[0]
        cactus_droite = cactus[0] + 18
        cactus_haut = y2
        cactus_bas = y2 + 21
        # On définit les bords du cactus

        if (kangourou_droite > cactus_gauche and
            kangourou_gauche < cactus_droite and
            kangourou_bas > cactus_haut and
            kangourou_haut < cactus_bas):
        # Si les deux rectangles se touchent

            game_over = True
            # Alors la partie se termine



x1 = 15
# Position horizontale du kangourou

y1 = 150
# Position verticale du kangourou

y2 = 150
# Position verticale des cactus (le sol)



def draw():
# Cette fonction dessine tout à l’écran

    pyxel.cls(1)
    # Efface l’écran avec la couleur noire
    pyxel.rect(0,165,500,35,3)  # rectangle vert = herbe

    pyxel.blt(x1,y1, 0,1,2,11,14,scale=2, colkey=0)
    # Dessine le kangourou à sa position

    pyxel.text(10,10,"Score : " + str(score),7)
    # Affiche le score en haut à gauche

    for cactus in liste:
    # Pour chaque cactus

        pyxel.blt(cactus[0],y2,0 ,1, 19,12,14,scale=1.5, colkey=0)
        # On dessine le cactus


    if game_over:
    # Si la partie est terminée

        pyxel.text(220,80,"GAME OVER",8)
        # Affiche GAME OVER

        pyxel.text(200,100,"APPUYE SUR E",7)
        # Indique comment rejouer

        pyxel.text(200,120,"SCORE : " + str(score),10)
        # Affiche le score final


pyxel.run(update,draw)
# Lance la boucle du jeu :
# Pyxel appelle en continu update() puis draw()

