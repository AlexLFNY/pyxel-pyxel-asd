import pyxel
import random

pyxel.init(120,160,fps=30)
pyxel.load("2.pyxres")
Tutorial = True
Color = 0
x = 10
y = 60
xr = 120
holecoord = random.randint(20,120)  ## Coordonnés du trous.
Score = 0
Speed = 2
PR = 0
Player_Speed = 2.5
Collision = 2
Car1 = 0
Car2 = 75
Car3 = 16 ## Pour controler la genération de sprite en fonction des deux différents modèles de voitures.
Car4 = 9
Car5 = 1
Grace = False
Grace_Period_Random1 = random.randint(11,30)  ## Les differentes Grace Period.
Grace_Period_Random2 = random.randint(35,50)
Grace_Period_Random3 = random.randint(55,75)
Grace_Period_Random4 = random.randint(80,100)
Grace_Period_Random5 = random.randint(105,150)
Grace_Timer = 0
Temp_Speed = 0
Temp_Player_Speed = 0
Sound_Timer = 360

def draw():
    global xr, x, y, holecoord, Collision, Color, Score, Speed, PR, Tutorial, Car1, Car2, Car3, Car4, Car5
    if Tutorial == True:  ## Tutoriel.
        pyxel.cls(1)
        pyxel.text(5,5,"How To Play:", 7)
        pyxel.text(8,15,"- Avoid the walls!", 7)
        pyxel.text(8,30,"- Use W / UP to go up", 7)
        pyxel.text(8,45,"- Use S / DOWN to go down", 7)
        pyxel.text(8,60,"- Walls will move faster", 7)
        pyxel.text(5,90,"Press space to start!", 7)
        if pyxel.btnp(pyxel.KEY_SPACE) == True:
            Tutorial = False
            Collision = False

    if Collision == False:  ## Mise en place des murs et de la voiture.
        pyxel.cls(Color)
        pyxel.text(5,8,"Score: " + str(Score),7)
        pyxel.blt(x,y,0,Car1,Car2,Car3,Car4,Car5)
        pyxel.blt(xr,0,0,16,8,8,holecoord,1)
        pyxel.blt(xr,(holecoord + 30),0,16,8,8,160 - (holecoord + 30),1)
    if Collision == True:  ## écran GAME OVER!
        pyxel.cls(0)
        pyxel.text(40, 120, "Play Again", 11)
        pyxel.text(40, 70, "GAME OVER!", 8)
        pyxel.text(33,15,"Your Score: " + str(Score),8)
        pyxel.text(30,40,"Personal Best: " + str(PR),8)
        pyxel.mouse(True)
        if 40 < pyxel.mouse_x < 80 and 120 < pyxel.mouse_y < 126:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):  ## Reset du jeu en entier.
                xr = 120
                y = 60
                holecoord = random.randint(20, 90)
                Collision = False
                pyxel.mouse(False)
                Score = 0
                Speed = 2
                Player_Speed = 2.5
                Color = 0
                if PR >= 50:  ## Nouveau modèle voiture.
                    Car1 = 32
                    Car2 = 84
                    Car3 = 15
                    Car4 = 7
                    Car5 = 0
        return

def update():
    global xr, x, y, holecoord, Collision, Score, Speed, PR, Player_Speed, Color, Grace_Period_Random1, Grace_Period_Random2, Grace_Period_Random3, Grace_Period_Random4, Grace_Period_Random5, Temp_Speed, Temp_Player_Speed, Grace, Grace_Timer, Sound_Timer
    
    if Tutorial:  ## Pour pas que les jeu tourne durant le tutoriel.
        if Sound_Timer == 360:
            pyxel.playm(0, loop = True)

        Sound_Timer -= 1
    
        if Sound_Timer <= 0:
            Sound_Timer = 360
        return
    
    xr -= Speed  ## Make the wall come towards the player.
    
    if pyxel.btn(pyxel.KEY_W) or pyxel.btn(pyxel.KEY_UP):  ## Mouvement du joueur.
        if y > 0:
            y -= Player_Speed

    if pyxel.btn(pyxel.KEY_S) or pyxel.btn(pyxel.KEY_DOWN):  ## Mouvement du joueur.
        if y < 160 - 15:
            y += Player_Speed

    if xr <= -8 and Collision == False:  ## Reset du mur et ajout de score.
        xr = 120
        holecoord = random.randint(20, 120)
        Score += 1
        pyxel.playm(2)

    if Score == 10:  ## Accèlération.
        Speed = 3

    if Score == 30:  ## Accèlération.
        Speed = 3.5
        Player_Speed = 3.5
    
    if Score == 50:  ## Accèlération.
        Speed = 4

    if Score == 100:  ## Accèlération.
        Speed = 5
        Player_Speed = 4.5

    if PR < Score:  ## High score.
            PR = Score

    player_center_x = x + 8
    pipe_center_x = xr + 4
    if abs(player_center_x - pipe_center_x) < (8 + 4):  ## Système de collisions.
        if y < holecoord or (y + 9) > (holecoord + 30):
            pyxel.playm(1)
            Collision = True

    if Score in (
    Grace_Period_Random1,
    Grace_Period_Random2,
    Grace_Period_Random3,
    Grace_Period_Random4,
    Grace_Period_Random5) and Grace == False:  ## Pour vérifier les 5 différentes grace period.
        Grace = True
        Grace_Timer = 60
        Color = 4 ## Change la couleur
        Temp_Speed = Speed
        Speed = Speed / 2  ## Ralenti la vitesse.
        Temp_Player_Speed = Player_Speed
        Player_Speed = Player_Speed / 2
    
    if Grace:  ## To make it 2 seconds long.
        Grace_Timer -= 1
        if Grace_Timer <= 0: ## Return to normal speed.
            Grace = False
            Speed = Temp_Speed
            Player_Speed = Temp_Player_Speed
            Color = 0

pyxel.run(update,draw)
