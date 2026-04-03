import pyxel
import random
import math

bird_y = 60
speed = 0
pipe_x = 160
pipe_gap = random.randint(20, 70)
score = 0
lives = 3
dead = False
blink = 0
flash = 0
last_lv = 0
orb_x = []
orb_y = []
orb_kind = []
orb_wait = 0
pu = [0, 0, 0, 0, 0]

def get_lv():
    if score >= 100: return (7, 7, 13, "Heaven", 6)
    if score >= 70:  return (6, 5,  3, "Deep Space", 5)
    if score >= 50:  return (8, 3,  9, "Dawn", 4)
    if score >= 35:  return (0, 4,  5, "Night", 3)
    if score >= 20:  return (2, 4,  3, "Sunset", 2)
    if score >= 10:  return (1, 3, 11, "Dusk", 1)
    return (12, 3, 11, "Day", 0)

def restart():
    global bird_y, speed, pipe_x, pipe_gap, score, lives
    global dead, blink, flash, last_lv, orb_x, orb_y, orb_kind, orb_wait
    bird_y = 60
    speed = 0
    pipe_x = 160
    pipe_gap = random.randint(20, 70)
    score = 0
    lives = 3
    dead = False
    blink = 0
    flash = 0
    last_lv = 0
    orb_x = []
    orb_y = []
    orb_kind = []
    orb_wait = 0
    for i in range(5):
        pu[i] = 0

def hit():
    global lives, blink, pipe_x
    if blink > 0:
        return
    if pu[2] > 0:
        pu[2] = 0
        blink = 60
        return
    lives = lives - 1
    blink = 90
    pipe_x = 160

def update():
    global bird_y, speed, pipe_x, pipe_gap, score
    global dead, blink, flash, last_lv, orb_x, orb_y, orb_kind, orb_wait

    if dead:
        if pyxel.btnp(pyxel.KEY_SPACE):
            restart()
        return

    if pyxel.btnp(pyxel.KEY_SPACE):
        speed = -3
    speed = speed + 0.2
    bird_y = bird_y + speed

    move = 1 if pu[4] > 0 else 2
    pipe_x = pipe_x - move

    if pipe_x < -10:
        pipe_x = 160
        pipe_gap = random.randint(20, 70)
        score = score + (2 if pu[3] > 0 else 1)

    lv = get_lv()
    if lv[4] != last_lv:
        flash = 45
        last_lv = lv[4]
    if flash > 0:
        flash = flash - 1

    bsz = 3 if pu[1] > 0 else 6
    gap = 60 if pu[0] > 0 else 40

    if int(pipe_x) < 44 + bsz and 44 < int(pipe_x) + 10:
        if int(bird_y) < pipe_gap or int(bird_y) + bsz > pipe_gap + gap:
            hit()

    if bird_y > 115 - bsz or bird_y < 0:
        hit()
        bird_y = 60
        speed = 0

    for i in range(5):
        if pu[i] > 0:
            pu[i] = pu[i] - 1
    if blink > 0:
        blink = blink - 1

    orb_wait = orb_wait - 1
    if orb_wait <= 0:
        if random.random() < 0.4:
            orb_x.append(164)
            orb_y.append(random.randint(10, 100))
            orb_kind.append(random.randint(0, 4))
        orb_wait = random.randint(120, 240)

    keep_x = []
    keep_y = []
    keep_k = []
    for i in range(len(orb_x)):
        orb_x[i] = orb_x[i] - move
        if orb_x[i] >= -8:
            dx = orb_x[i] - (44 + bsz / 2)
            dy = orb_y[i] - (bird_y + bsz / 2)
            if math.sqrt(dx * dx + dy * dy) < 4 + bsz / 2:
                pu[orb_kind[i]] = 300
            else:
                keep_x.append(orb_x[i])
                keep_y.append(orb_y[i])
                keep_k.append(orb_kind[i])
    orb_x = keep_x
    orb_y = keep_y
    orb_kind = keep_k

    if lives <= 0:
        dead = True

def draw():
    cols  = [5, 10, 7, 9, 12]
    names = ["WIDE", "MINI", "SHLD", "x2", "SLOW"]
    lv = get_lv()
    sky, gc, pc, lv_name, _ = lv[0], lv[1], lv[2], lv[3], lv[4]

    pyxel.cls(7 if flash > 0 and flash % 12 < 6 else sky)
    pyxel.rect(0, 115, 160, 5, gc)

    px = int(pipe_x)
    gap = 60 if pu[0] > 0 else 40
    pyxel.rect(px, 0, 10, pipe_gap, pc)
    pyxel.rect(px, pipe_gap + gap, 10, 120 - pipe_gap - gap, pc)
    pyxel.rect(px - 1, pipe_gap - 4, 12, 4, gc)
    pyxel.rect(px - 1, pipe_gap + gap, 12, 4, gc)

    for i in range(len(orb_x)):
        pyxel.circ(int(orb_x[i]), int(orb_y[i]), 4, cols[orb_kind[i]])
        pyxel.circb(int(orb_x[i]), int(orb_y[i]), 4, 7)

    if blink == 0 or pyxel.frame_count % 6 < 3:
        bsz = 3 if pu[1] > 0 else 6
        bc = 7 if pu[2] > 0 else 10
        pyxel.rect(44, int(bird_y), bsz, bsz, bc)
        pyxel.pset(44 + bsz - 1, int(bird_y) + 1, 0)

    pyxel.text(5, 4, "Score: " + str(score), 7)
    pyxel.text(5, 12, "Lives: " + str(lives), 8)
    pyxel.text(157 - len(lv_name) * 4, 4, lv_name, 7)

    if flash > 20:
        pyxel.text(47, 54, "LEVEL UP!", 10)
        pyxel.text(33, 63, "Now: " + lv_name, 7)

    y_off = 22
    for i in range(5):
        if pu[i] > 0:
            pyxel.text(5, y_off, names[i], cols[i])
            pyxel.rect(5, y_off + 7, int(40 * pu[i] / 300), 2, cols[i])
            y_off = y_off + 12

    if dead:
        pyxel.rect(30, 45, 100, 35, 0)
        pyxel.rectb(30, 45, 100, 35, 7)
        pyxel.text(52, 52, "GAME OVER", 7)
        pyxel.text(45, 62, "Score: " + str(score), 9)
        pyxel.text(38, 72, "SPACE to restart", 6)

pyxel.init(160, 120, title="Flappy Bird", fps=60)
pyxel.run(update, draw)