import pygame
from random import randint

class Cenario(object):
    def __init__(self, scr, paoselected):
        self.paoselected = paoselected
        if paoselected == "croissant":
            self.p1 = Player(scr, (0,255,0), [150, 240, 50, 25], 5, self.paoselected)
        else:
            self.p1 = Player(scr, (0, 255, 0), [150, 240, 25, 50], 5, self.paoselected)
        self.scr = scr
        self.font = pygame.font.SysFont("assets/Vineta", 25, True, False)
        self.image = pygame.image.load("assets/boca.png").convert_alpha()
        self.manteigas = []
        self.plataformas = []
        self.velx = 6
        self.count = 0
        self.count_manteiga = 0
        self.count_plataforma = 0
        self.velw = -1
        self.weather = 2550
        score = open("score.txt", "r")
        self.highscore = score.read()
        score.close()
        self.biteSound = pygame.mixer.Sound("assets/bite.wav")
        self.bite = False

    def update(self):
        #score = self.font.render("Pontos : " + str(self.p1.score), True, (255 - self.weather // 10, 255 - self.weather // 10, 255 - self.weather // 10))
        score2 = self.font.render("Pontos : " + str(self.p1.score), True,(255, 255, 0))
        highscore = self.font.render("HighScore : " + str(self.highscore), True, (0, 0, 255))

        for plataforma in self.plataformas:
            plataforma.draw()
            plataforma.rect[0] -= self.velx
            if plataforma.rect[0] < -100:
                self.plataformas.remove(plataforma)
            plataforma_Rect = pygame.Rect(plataforma.rect)
            p1_Rect = pygame.Rect(self.p1.rect)
            if pygame.Rect.colliderect(p1_Rect, plataforma_Rect):
                self.p1.rect[0] = plataforma_Rect.left - self.p1.rect[2]

        self.scr.blit(self.image, (-20, 0))

        for manteiga in self.manteigas:
            manteiga.draw()
            manteiga.rect[0] -= self.velx
            if manteiga.rect[0] < -100:
                self.manteigas.remove(manteiga)
            manteiga_Rect = pygame.Rect(manteiga.rect)
            p1_Rect = pygame.Rect(self.p1.rect)
            if pygame.Rect.colliderect(p1_Rect, manteiga_Rect):
                self.manteigas.remove(manteiga)
                self.p1.alive = False

        self.p1.draw()
        #self.scr.blit(score, (500, 50))
        self.scr.blit(score2, (503, 50))
        self.scr.blit(highscore, (550, 0))

        pygame.draw.rect(self.scr, (200, 200, 0), [0, 550, 1000, 25], 0)

        if len(self.manteigas) < 10 and self.count_manteiga > 120:
            self.manteigas.append(Enemy(self.scr, (200, 200, 0), [1000, randint(50, 430), 50, 25], "assets/manteiga.png"))
            self.count_manteiga = 0
            if self.p1.alive:
                self.p1.score += 1

        if len(self.plataformas) < 10 and self.count_plataforma > randint(240, 480):
            altura = randint(200, 400)
            self.plataformas.append(Enemy(self.scr, (200, 200, 0), [1000, 600 - altura, 25, altura], "assets/plataforma.png"))
            self.count_plataforma = 0



        if self.count > 3000:
            self.velx += 1
            self.count = 0

        if self.count % 70 == 0 and not self.p1.estado == 3:
            if self.p1.estado == 1:
                self.p1.image = pygame.image.load("assets/" + self.paoselected + "/pao_andando2.png").convert_alpha()
                self.p1.estado = 2
            elif self.p1.estado == 2:
                self.p1.image = pygame.image.load("assets/" + self.paoselected + "/pao_andando1.png").convert_alpha()
                self.p1.estado = 1

        self.weather += self.velw
        if self.weather < 50:
            self.velw = 1
        elif self.weather > 2500:
            self.velw = -1

        if self.p1.rect[0] + self.p1.velx > 525 - self.p1.rect[2]:
            self.p1.velx = 0
        if self.p1.rect[0] + self.p1.velx < 0:
            self.p1.alive = False
            if not self.bite:
                self.biteSound.play()
                self.bite = True
            self.image = pygame.image.load("assets/bocafechada1.png").convert_alpha()
            self.image = pygame.image.load("assets/bocafechada.png").convert_alpha()

        if self.p1.rect[1] + self.p1.vely > 463 - self.p1.rect[3]:
            self.p1.pulo = 0
            self.p1.vely = 0
            if self.p1.estado == 3:
                self.p1.image = pygame.image.load("assets/" + self.paoselected + "/pao_andando1.png").convert_alpha()
                self.p1.estado = 1

        self.count_manteiga += 1
        self.count_plataforma += 1
        self.count += 1
        self.p1.update()
        pygame.draw.rect(self.scr, (255, 255, 0), [0, 460, 800, 20], 0)

    def restart(self):
        global manteigas, plataformas, weather
        score = open("score.txt", "r")
        highscore = score.read()
        score.close()
        if self.p1.score > int(highscore):
            score = open("score.txt", "w")
            score.write(str(self.p1.score))
            score.close()
        score = open("score.txt", "r")
        self.highscore = score.read()
        self.image = pygame.image.load("assets/boca.png").convert_alpha()
        self.bite = False
        self.p1.alive = True
        self.p1.rect[0] = 150
        self.p1.score = 0
        self.manteigas = []
        self.plataformas = []
        self.weather = 2550
        self.velx = 6

class Player(object):
    def __init__(self, scr, color, rect ,vely, paoselected):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.vely = vely
        self.paoselected = paoselected
        self.velx = 0
        self.image = pygame.image.load("assets/" + self.paoselected + "/pao_andando1.png").convert_alpha()
        self.width = 0
        self.alive = True
        self.score = 0
        self.pulo = 0
        self.estado = 1

    def draw(self):
        if self.alive:
            pygame.draw.rect(self.scr, self.color, self.rect, self.width)
            self.scr.blit(self.image, (self.rect[0], self.rect[1]))

    def update(self):
        if self.alive:
            self.rect[1] += self.vely
            self.vely += 0.15
            self.rect[0] += self.velx

class Enemy(object):
    def __init__(self, scr, color, rect, image):
        self.scr = scr
        self.color = color
        self.rect = rect
        self.image = pygame.image.load(image).convert_alpha()
        self.width = 0

    def draw(self):
        #pygame.draw.rect(self.scr, self.color, self.rect, self.width)
        self.scr.blit(self.image, (self.rect[0], self.rect[1]))