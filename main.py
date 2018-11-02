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

paoselected = ["paofrances", "baguete", "croissant", "paodeforma", "paoretro", "torrada"]
select = 0
cenario = cls.Cenario(scr, paoselected[select])

def colliderect( obj, mouse, objrender):
    objrect = objrender.get_rect()
    if obj["x"] + objrect.w > mouse[0] > obj["x"] and obj["y"] + objrect.h > mouse[1] > obj["y"]:
        obj["correct"] = (0, 0, 0)
        obj["mcolide"] = True
    else:
        obj["correct"] = (255, 255, 0)
        obj["mcolide"] = False

def paoselect():
    global paoselected, select
    paoselected = ["paofrances", "baguete", "croissant", "paodeforma", "paoretro", "torrada"]
    arial = pygame.font.SysFont("Arial", 64, True, False)
    rectalpha = pygame.Surface((90, 90))
    rectalpha.set_alpha(160)
    rectalpha.fill((255, 255, 255))
    esquerda = {"texto": "<", "x": 200, "y": 300, "cor": (255, 255, 255),"correct": (255, 255, 0) ,"mcolide": False}
    direita = {"texto": ">", "x": 600, "y": 300, "cor": (255, 255, 255), "correct": (255, 255, 0), "mcolide": False}
    voltar = {"texto": "Voltar", "x": 0, "y": 420, "cor": (255, 255, 255), "correct": (255, 255, 0), "mcolide": False}
    run = True
    while run:
        scr.fill((255, 255, 255))
        paofundo = pygame.image.load("assets/" + paoselected[select] + "/pao_surprise.png").convert_alpha()
        paofundoscaled = pygame.transform.scale(paofundo, (60, 120))

        if select + 1 >= len(paoselected):
            paofundodireita = pygame.image.load("assets/" + paoselected[len(paoselected) - select] + "/pao.png")
        else:
            paofundodireita = pygame.image.load("assets/" + paoselected[select + 1] + "/pao.png")

        if select - 1 < 0:
            paofundoesquerda = pygame.image.load("assets/" + paoselected[len(paoselected) - 1] + "/pao.png")
        else:
            paofundoesquerda = pygame.image.load("assets/" + paoselected[select - 1] + "/pao.png")

        paofundodireita_scaled = pygame.transform.scale(paofundodireita, (40, 80))
        paofundoesquerda_scaled = pygame.transform.scale(paofundoesquerda, (40, 80))

        for e in pygame.event.get():
            if e.type == QUIT:
                exit()
            elif e.type == KEYDOWN:
                if e.key == K_f:
                    exit()
            elif e.type == MOUSEBUTTONDOWN:
                if e.button == 1:
                    if esquerda ["mcolide"] == True:
                        select -= 1
                        if select < 0:
                            select = len(paoselected) - 1
                    elif direita["mcolide"] == True:
                        select += 1
                        if select >= len(paoselected):
                            select = 0
                    elif voltar["mcolide"] == True:
                        run = False

        mouse = pygame.mouse.get_pos()

        scr.blit(paofundoesquerda_scaled, (350, 300))
        scr.blit(rectalpha, (350, 300))
        scr.blit(paofundodireita_scaled, (475, 300))
        scr.blit(rectalpha, (475, 300))
        scr.blit(paofundoscaled, (400, 300))
        #selected = arial.render("Selecionado: " + paoselected, True, (255, 255, 0))
        #scr.blit(selected, (200, 300))
        direitarender = arial.render(direita["texto"], True, direita["cor"], direita["correct"])
        voltarrender = arial.render(voltar["texto"], True, voltar["cor"], voltar["correct"])
        esquerdarender = arial.render(esquerda["texto"], True, esquerda["cor"], esquerda["correct"])

        scr.blit(direitarender, (direita["x"], direita["y"]))
        scr.blit(voltarrender, (voltar["x"], voltar["y"]))
        scr.blit(esquerdarender, (esquerda["x"], esquerda["y"]))

        colliderect(direita, mouse, direitarender)
        colliderect(voltar, mouse, voltarrender)
        colliderect(esquerda, mouse, esquerdarender)



        clock.tick(60)
        pygame.display.update()

def gameintro():
    global cenario
    arial = pygame.font.SysFont("Arial", 64, True, False)
    start = {"texto": "Start Game", "x": 200, "y": 100, "cor":(255, 255, 255), "correct": (255, 255, 0), "mcolide": False}
    pao = {"texto": "Choose Pao", "x": 200, "y": 300, "cor": (255, 255, 255), "correct": (255, 255, 0), "mcolide": False}
    intro = True
    while intro:
        scr.fill((255, 255, 255))

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
                        cenario = cls.Cenario(scr, paoselected[select])
                    elif pao["mcolide"] == True:
                        paoselect()

        mouse = pygame.mouse.get_pos()

        startrender = arial.render(start["texto"], True, start["cor"], start["correct"])
        paorender = arial.render(pao["texto"], True, pao["cor"], pao["correct"])

        scr.blit(startrender, (start["x"], start["y"]))
        scr.blit(paorender, (pao["x"], pao["y"]))

        colliderect(start, mouse, startrender)
        colliderect(pao, mouse, paorender)

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
                    cenario.p1.image = pygame.image.load("assets/" + paoselected[select] + "/pao_jump.png").convert_alpha()
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
                    cenario.p1.image = pygame.image.load("assets/" + paoselected[select] + "/pao_jump.png").convert_alpha()
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