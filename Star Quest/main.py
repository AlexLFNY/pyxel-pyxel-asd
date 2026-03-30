import pyxel
import math

# Platform data: (x, y, width, color)
PLATFORMS = [
    (180, 240, 100, 8),  # Red
    (320, 200, 120, 12), # Blue
    (490, 220, 100, 8),  # Red
    (600, 160, 110, 12), # Blue
]


COINS_POS = [
    [200, 220], [340, 180], [510, 200], # On Platforms
    [620, 140], [100, 300], [400, 300], # On Ground
]

def big_text(x, y, text, col, text_scale=3):

    pyxel.images[1].cls(0)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        pyxel.images[1].text(1 + dx, 1 + dy, text, 0)
    # Main text
    pyxel.images[1].text(1, 1, text, col)
    
    tw = len(text) * 4 + 4 
    pyxel.blt(x, y, 1, 0, 0, tw, 8, 0, scale=text_scale)

def draw_heart(x, y):
    pyxel.circ(x, y, 2, 8)
    pyxel.circ(x + 4, y, 2, 8)
    pyxel.tri(x - 2, y + 1, x + 6, y + 1, x + 2, y + 6, 8)

class Game:
    def __init__(self):
        pyxel.init(720, 360, title="Star Quest")
        try:
            pyxel.load("./my_resource.pyxres")
            pyxel.playm(0,loop =True)
        except:
            pass 

        self.score = 0
        self.lives = 3
        self.has_sword = False
        self.has_key = False
        self.game_over = False
        self.game_won = False
        self.invincible = 0
        self.speed_boost = 0

        self.p_height = 30 
        self.ground_y = 320 
        
        self.reset_player()
        self.key = [140, 300, True]     
        self.sword = [450, 300, True]   
        self.chest = [680, 300]         
        self.shield = [250, 300, True]  
        self.coins = [{"x": c[0], "y": c[1], "active": True} for c in COINS_POS]

        # Enemies 
        self.mushrooms = [
            {"x": 340, "y": 300, "start_x": 340, "dir": 1, "active": True}, 
            {"x": 570, "y": 300, "start_x": 570, "dir": 1, "active": True}, 
        ]
        self.ghosts = [
            {"x": 260, "start_y": 140, "y": 140, "active": True}, 
            {"x": 420, "start_y": 100, "y": 100, "active": True}, 
        ]
        self.bat = {"x": 500.0, "y": 80, "dx": 4.0} 

        pyxel.run(self.update, self.draw)

    def reset_player(self):
        self.player_x = 50.0 
        self.player_y = self.ground_y - self.p_height 
        self.player_dx = 0.0
        self.player_dy = 0.0
        self.jumps_made = 0

    def hit_player(self):
        if self.invincible > 0: return
        self.lives -= 1
        self.invincible = 60
        if self.lives <= 0: self.game_over = True
        else: self.reset_player()

    def update(self):
        if self.game_won or self.game_over: return

        if self.invincible > 0: self.invincible -= 1
        if self.speed_boost > 0: self.speed_boost -= 1

        accel = 3.5 if self.speed_boost > 0 else 2.0
        if pyxel.btn(pyxel.KEY_A): self.player_dx -= accel
        if pyxel.btn(pyxel.KEY_D): self.player_dx += accel
        self.player_dx *= 0.65 
        self.player_x += self.player_dx

        if (pyxel.btnp(pyxel.KEY_SPACE)) and self.jumps_made < 2:
            self.player_dy = -15
            self.jumps_made += 1

        self.player_dy += 2.2 
        self.player_y += self.player_dy

        if self.player_y >= self.ground_y - self.p_height:
            self.player_y = self.ground_y - self.p_height
            self.player_dy = 0
            self.jumps_made = 0

        if self.player_dy > 0:
            for (px, py, pw, pcol) in PLATFORMS:
                if self.player_x + 30 > px and self.player_x + 10 < px + pw:
                    if py - 10 < (self.player_y + self.p_height) < py + 5:
                        self.player_y = py - self.p_height
                        self.player_dy = 0
                        self.jumps_made = 0

        for c in self.coins:
            if c["active"] and abs(self.player_x - c["x"]) < 25 and abs(self.player_y - c["y"]) < 25:
                c["active"] = False; self.score += 10

        if self.key[2] and abs(self.player_x - self.key[0]) < 30 and abs(self.player_y - self.key[1]) < 30:
            self.key[2] = False; self.has_key = True; self.score += 50

        if self.sword[2] and abs(self.player_x - self.sword[0]) < 30 and abs(self.player_y - self.sword[1]) < 30:
            self.sword[2] = False; self.has_sword = True

        if self.shield[2] and abs(self.player_x - self.shield[0]) < 30 and abs(self.player_y - self.shield[1]) < 30:
            self.shield[2] = False; self.speed_boost = 300

        if self.has_key and abs(self.player_x - self.chest[0]) < 40 and abs(self.player_y - self.chest[1]) < 40:
            self.game_won = True

        for m in self.mushrooms:
            if m["active"]:
                m["x"] += m["dir"] * 2
                if abs(m["x"] - m["start_x"]) > 60: m["dir"] *= -1
                if abs(self.player_x - m["x"]) < 25 and abs(self.player_y - m["y"]) < 25:
                    if self.has_sword: m["active"] = False; self.score += 50
                    else: self.hit_player()
        
        for g in self.ghosts:
            g["y"] = g["start_y"] + math.sin(pyxel.frame_count * 0.1) * 40
            if abs(self.player_x - g["x"]) < 30 and abs(self.player_y - g["y"]) < 30:
                self.hit_player()

        self.bat["x"] += self.bat["dx"]
        if self.bat["x"] < 0 or self.bat["x"] > 700: self.bat["dx"] *= -1
        if abs(self.player_x - self.bat["x"]) < 25 and abs(self.player_y - self.bat["y"]) < 25:
            self.hit_player()

    def draw(self):
        pyxel.cls(0)

        # Ground
        for x in range(0, 720, 82):
            pyxel.blt(x, self.ground_y, 0, 48, 0, 82, 16, 0, scale=4)
        
        # Platforms
        for (px, py, pw, pcol) in PLATFORMS:
            pyxel.rect(px, py, pw, 8, pcol) 
            pyxel.rect(px, py + 8, pw, 2, 4) 

        # Items
        if self.key[2]: pyxel.blt(self.key[0], self.key[1], 0, 128, 0, 24, 16, 0, scale=2)
        for c in self.coins:
            if c["active"]: pyxel.blt(c["x"], c["y"], 0, 0, 8, 16, 8, 0, scale=2.5)
        if self.sword[2]: pyxel.blt(self.sword[0], self.sword[1], 0, 168, 0, 16, 16, 0, scale=2.5)
        if self.shield[2]: pyxel.blt(self.shield[0], self.shield[1], 0, 216, 0, 16, 16, 0, scale=2.5)
        pyxel.blt(self.chest[0], self.chest[1], 0, 152, 0, 16, 16, 0, scale=2.5)

        # Enemies
        for m in self.mushrooms:
            if m["active"]: pyxel.blt(m["x"], m["y"], 0, 232, 0, 16, 16, 0, scale=2.5)
        for g in self.ghosts:
            pyxel.blt(g["x"], g["y"], 0, 0, 16, 16, 16, 0, scale=2.5)

        # Bat
        bx, by, flap = int(self.bat["x"]), int(self.bat["y"]), math.sin(pyxel.frame_count * 0.5) * 8
        pyxel.tri(bx, by, bx-15, by-flap, bx-5, by+5, 8)
        pyxel.tri(bx+8, by, bx+23, by-flap, bx+13, by+5, 8)
        pyxel.rect(bx, by, 8, 6, 0)

   
        if self.invincible == 0 or pyxel.frame_count % 4 < 2:
            pyxel.blt(self.player_x, self.player_y + 10, 0, 184, 0, 16, 16, 0, scale=2.5)


        big_text(40, 20, f"SCORE: {self.score}", 7)
        if self.has_key: big_text(40, 50, "KEY READY!", 10)
        
        # Hearts
        for i in range(self.lives):
            draw_heart(650 + i * 20, 25)
        if self.game_won: big_text(240, 160, "YOU WIN!", 10, text_scale=6)
        if self.game_over: big_text(240, 160, "GAME OVER", 8, text_scale=6)

Game()
