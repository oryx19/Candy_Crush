import os
import pygame
from pygame import Rect
from pygame.math import Vector2
import csv
from random import randint
import matplotlib.pyplot as plt

os.environ['SDL_VIDEO_CENTERED'] = '1'

class BackEnd():
    @staticmethod
    def extrait_information(nom_fich):
        """Lecture ligne par ligne du fichier csv contenant les informations du calendrier.
        Entrée :
            - nom_fich (str) : nom du fichier (avec son extension) au format Année;Mois;Jour;H_deb;H_fin;Matiere;Type;Intervenant;Salle, et dont la première ligne correspond aux titres des colonnes. Les évènements n’apparaissent pas nécessairement de manière triés dans le fichier.
        Sortie :
            - (list de list de str) : calendrier sous la forme de liste d’évènements (list de str).
        """
        c = []
        with open(nom_fich, newline="") as f:
            reader = csv.reader(f, delimiter = " ")
            next(reader) # passer la première ligne qui contient les titres des colonnes
            for row in reader:
                c.append([int(x) for x in row])
        y = len(c)
        x = len(c[0])
        maximum = c[0][0]
        for ele in c:
            for ele2 in ele:
                if ele2 > maximum:
                    maximum = ele2
        return c,x,y,maximum+1
    
    @staticmethod
    def check_valid(g,x1,y1):
        temp = False
        nb_col = len(g[0])
        nb_ligne = len(g)
        if  0 <= x1 and x1 < nb_col and 0 <= y1 and y1 < nb_ligne:
            temp = True
        return temp
    
    @staticmethod
    def saisir(g):
        x1 = int(input("Entrez la coordonnée x1 : "))
        y1 = int(input("Entrez la coordonnée y1 : "))
        x2 = int(input("Entrez la coordonnée x2 : "))
        y2 = int(input("Entrez la coordonnée y2 : "))
        while not BackEnd.check_valid(g,x1,y1) or not BackEnd.check_valid(g,x2,y2):
            print("Les coordonnées saisies sont incorrectes")
            x1 = int(input("Entrez la coordonnée x1 : "))
            y1 = int(input("Entrez la coordonnée y1 : "))
            x2 = int(input("Entrez la coordonnée x2 : "))
            y2 = int(input("Entrez la coordonnée y2 : "))
        return x1,y1,x2,y2
    
    @staticmethod
    def check_neighbors(x1,y1,x2,y2):
        temp = False
        if (abs(x1-x2) > 1) or (abs(y1-y2) > 1):
            temp = True
        return temp

    @staticmethod
    def switch(g,x1,y1,x2,y2):
        """
        Prendre en parametre deux coordonnees et verifier si elles sont voisines.
        """
        nb_ligne = len(g) #nếu có ít nhất 3 viên kẹo giống nhau nằm thẳng hàng (theo chiều ngang hoặc chiều dọc)👉 thì 3 viên kẹo đó sẽ bị xóa.
        nb_col = len(g[0])
        if BackEnd.check_neighbors(x1,y1,x2,y2):
            print("Les cases choisies ne sont pas voisines")
        elif BackEnd.check_valid(g,x1,y1) and BackEnd.check_valid(g,x2,y2):
            temp = g[y1][x1]
            g[y1][x1] = g[y2][x2]
            g[y2][x2] = temp

    @staticmethod
    def check_match_horizontal_v2(g):
        temp = False
        for i in range(len(g)):
            x_debut = 0
            check = 1
            for j in range(1,len(g[i])):
                if  g[i][x_debut] == g[i][j] and g[i][j] != -1:
                    check += 1
                elif g[i][x_debut] != g[i][j] and check >= 3:
                    temp = True
                    liste = []
                    for k in range(check):
                        liste.append([i,x_debut+k])
                    add = False
                    while add == False:
                        add = True
                        delta = [-1,1]
                        for ele in liste:
                            for step in delta:
                                if BackEnd.check_valid(g,ele[0],ele[1]+step) and g[ele[0]][ele[1]+step] == g[i][x_debut]:
                                    liste.append([ele[0],ele[1]+step])
                                    add = False
                                if BackEnd.check_valid(g,ele[0]+step,ele[1]) and g[ele[0]+step][ele[1]] == g[i][x_debut]:
                                    liste.append([ele[0]+step,ele[1]])
                                    add = False
                    for ele in liste:
                        g[ele[0]][ele[1]] = -1
                    check = 1
                    x_debut = j
                else:
                    check = 1
                    x_debut = j
                if check >= 3:
                    temp = True
                    liste = []
                    for k in range(check):
                        liste.append([i,x_debut+k])
                        add = False
                    while add == False:
                        add = True
                        delta = [-1,1]
                    for ele in liste:
                        for step in delta:
                            if BackEnd.check_valid(g,ele[0],ele[1]+step) and g[ele[0]][ele[1]+step] == g[i][x_debut]:
                                liste.append([ele[0],ele[1]+step])
                                add = False
                            if BackEnd.check_valid(g,ele[0]+step,ele[1]) and g[ele[0]+step][ele[1]] == g[i][x_debut]:
                                liste.append([ele[0]+step,ele[1]])
                                add = False
                    for ele in liste:
                        g[ele[0]][ele[1]] = -1
        return temp

class GameState():
    def __init__(self):
        self.worldSize = Vector2(16,10)
        self.tankPos = Vector2(0,0)

    def update(self,moveTankCommand):
        self.tankPos += moveTankCommand

        if self.tankPos.x < 0:
            self.tankPos.x = 0
        elif self.tankPos.x >= self.worldSize.x:
            self.tankPos.x = self.worldSize.x - 1

        if self.tankPos.y < 0:
            self.tankPos.y = 0
        elif self.tankPos.y >= self.worldSize.y:
            self.tankPos.y = self.worldSize.y - 1

class UserInterface():
    def __init__(self):
        pygame.init()

        # Game state
        self.gameState = GameState()

        # Rendering properties
        self.cellSize = Vector2(64,64)

        # Window
        windowSize = self.gameState.worldSize.elementwise() * self.cellSize
        self.window = pygame.display.set_mode((int(windowSize.x),int(windowSize.y)))
        pygame.display.set_caption("Demo")
        self.moveTankCommand = Vector2(0,0)

        # Loop properties
        self.clock = pygame.time.Clock()
        self.running = True

    def processInput(self):
        self.moveTankCommand = Vector2(0,0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    self.moveTankCommand.x = 1
                elif event.key == pygame.K_LEFT:
                    self.moveTankCommand.x = -1
                elif event.key == pygame.K_DOWN:
                    self.moveTankCommand.y = 1
                elif event.key == pygame.K_UP:
                    self.moveTankCommand.y = -1

    def update(self):
        self.gameState.update(self.moveTankCommand)

    def render(self):
        self.window.fill((0,0,0))

        # Tank base
        spritePoint = self.gameState.tankPos.elementwise()*self.cellSize
        texturePoint = Vector2(1,0).elementwise()*self.cellSize
        textureRect = Rect(int(texturePoint.x), int(texturePoint.y), int(self.cellSize.x),int(self.cellSize.y))
        self.window.blit(self.unitsTexture,spritePoint,textureRect)

        pygame.display.update()    

    def run(self):
        while self.running:
            self.processInput()
            self.update()
            self.render()
            self.clock.tick(60)

userInterface = UserInterface()
userInterface.run()

pygame.quit()