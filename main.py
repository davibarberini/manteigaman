import pygame
import classes as cls
from pygame.locals import QUIT, KEYDOWN, KEYUP, K_LEFT, K_RIGHT, K_UP, K_DOWN, FULLSCREEN, K_f, K_r, K_i, JOYBUTTONDOWN, JOYAXISMOTION \
    , MOUSEBUTTONDOWN, K_ESCAPE, K_p


pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

scr = pygame.display.set_mode((800, 480), FULLSCREEN, 32)

clock = pygame.time.Clock()

jumpSound = pygame.mixer.Sound("assets/jumping.wav")

music = pygame.mixer.music.load("assets/music.mp3")
pygame.mixer.music.play(-1)

paoselected = "paofrances"
cenario = cls.Cenario(scr, paoselected)

def colliderect( obj, mouse, objrender):
    objrect = objrender.get_rect()
    if obj["x"] + objrect.w > mouse[0] > obj["x"] and obj["y"] + objrect.h > mouse[1] > obj["y"]:
        obj["correct"] = (255, 255, 255)
        obj["mcolide"] = True
    else:
        obj["correct"] = (255, 255, 0)
        obj["mcolide"] = False

def paoselect():
    global paoselected
    paoselected = "paofrances"

    arial = pygame.font.SysFont("Arial", 64, True, False)
    pao = {"texto": "Pao", "x": 300, "y": 50, "cor": (0, 0, 0),"correct": (255, 255, 0) ,"mcolide": False}
    baguete = {"texto": "Baguete", "x": 500, "y": 50, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    voltar = {"texto": "Voltar", "x": 0, "y": 420, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    run = True
    while run:
        scr.fill((0, 0, 0))
        paofundo = pygame.image.load("assets/" + paoselected + "/pao.png").convert_alpha()
        paofundoscaled = pygame.transform.scale(paofundo, (60, 120))

        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_f:
                    exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if pao["mcolide"] == True:
                        paoselected = "paofrances"
                    elif baguete["mcolide"] == True:
                        paoselected = "baguete"
                    elif voltar["mcolide"] == True:
                        run = False
        mouse = pygame.mouse.get_pos()

        scr.blit(paofundoscaled, (350, 300))
        scr.blit(paofundoscaled, (400, 300))
        scr.blit(paofundoscaled, (450, 300))
        #selected = arial.render("Selecionado: " + paoselected, True, (255, 255, 0))
        #scr.blit(selected, (200, 300))
        paorender = arial.render(pao["texto"], True, pao["cor"], pao["correct"])
        voltarrender = arial.render(voltar["texto"], True, voltar["cor"], voltar["correct"])
        bagueterender = arial.render(baguete["texto"], True, baguete["cor"], baguete["correct"])

        scr.blit(paorender, (pao["x"], pao["y"]))
        scr.blit(voltarrender, (voltar["x"], voltar["y"]))
        scr.blit(bagueterender, (baguete["x"], baguete["y"]))

        colliderect(pao, mouse, paorender)
        colliderect(voltar, mouse, voltarrender)
        colliderect(baguete, mouse, bagueterender)



        clock.tick(60)
        pygame.display.update()

def gameintro():
    global cenario
    arial = pygame.font.SysFont("Arial", 64, True, False)
    start = {"texto": "Start Game", "x": 200, "y": 100, "cor":(0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    pao = {"texto": "Choose Pao", "x": 200, "y": 300, "cor": (0, 0, 0), "correct": (255, 255, 0), "mcolide": False}
    startrender = arial.render(start["texto"], True, start["cor"])
    paorender = arial.render(pao["texto"], True, pao["cor"])
    startrect = startrender.get_rect()
    paorect = paorender.get_rect()
    intro = True
    while intro:
        scr.fill((0, 0, 0))

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_p:
                    intro = False
                if e.key == K_f:
                    exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if start["mcolide"] == True:
                        intro = False
                        cenario = cls.Cenario(scr, paoselected)
                    elif pao["mcolide"] == True:
                        paoselect()
        mouse = pygame.mouse.get_pos()

        pygame.draw.rect(scr, start["correct"], [start["x"], start["y"],startrect.w, startrect.h], 0)
        pygame.draw.rect(scr, pao["correct"], [pao["x"], pao["y"], paorect.w, paorect.h], 0)
        scr.blit(startrender, (start["x"], start["y"]))
        scr.blit(paorender, (pao["x"], pao["y"]))

        if start["x"] + startrect.w > mouse[0] > start["x"] and start["y"] + startrect.h > mouse[1] > start["y"]:
            start["correct"] = (255, 255, 255)
            start["mcolide"] = True
        else:
            start["correct"] = (255, 255, 0)
            start["mcolide"] = False
        if pao["x"] + paorect.w > mouse[0] > pao["x"] and pao["y"] + paorect.h > mouse[1] > pao["y"]:
            pao["correct"] = (255, 255, 255)
            pao["mcolide"] = True
        else:
            pao["correct"] = (255, 255, 0)
            pao["mcolide"] = False

        clock.tick(60)
        pygame.display.update()

def gameloop():
    run = True
    while run:
        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

        clock.tick(120)

        for e in pygame.event.get():
            if e.type == QUIT:
                run = False
            elif e.type == KEYDOWN:
                if e.key == K_f:
                    run = False
                elif e.key == K_r:
                    cenario.restart()
                elif e.key == K_UP and cenario.p1.pulo <= 2:
                    jumpSound.play()
                    cenario.p1.image = pygame.image.load("assets/" + paoselected + "/pao_jump.png").convert_alpha()
                    cenario.p1.estado = 3
                    cenario.p1.pulo += 1
                    cenario.p1.vely = -6
                elif e.key == K_RIGHT:
                    cenario.p1.velx = 3
                elif e.key == K_LEFT:
                    cenario.p1.velx = -6
                elif e.key == K_ESCAPE:
                        gameintro()
            elif e.type == KEYUP:
                if e.key == K_RIGHT and cenario.p1.velx > 0:
                    cenario.p1.velx = 0
                elif e.key == K_LEFT and cenario.p1.velx < 0:
                    cenario.p1.velx = 0
            elif e.type == JOYBUTTONDOWN:
                if e.button == 0 and cenario.p1.pulo <= 2:
                    jumpSound.play()
                    cenario.p1.image = pygame.image.load("assets/" + paoselected + "/pao_jump.png").convert_alpha()
                    cenario.p1.estado = 3
                    cenario.p1.pulo += 1
                    cenario.p1.vely = -6
                elif e.button == 2:
                    cenario.restart()
                elif e.button == 1:
                    run = False
                elif e.button == 7:
                    gameintro()
            elif e.type == JOYAXISMOTION:
                print(e.value)
                if e.axis == 0:
                    if e.value == 1:
                        cenario.p1.velx = 3
                    elif int(e.value) == -1:
                        cenario.p1.velx = -6
                    else:
                        cenario.p1.velx = 0

        pygame.display.update()
        scr.fill((cenario.weather // 10, cenario.weather // 10, cenario.weather // 10))
        cenario.update()


gameintro()
gameloop()

score = open("score.txt", "r")
highscore = score.read()
score.close()
if cenario.p1.score > int(highscore):
    score = open("score.txt", "w")
    score.write(str(cenario.p1.score))
    score.close()