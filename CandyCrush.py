import os
import pygame
import csv
from random import randint

os.environ['SDL_VIDEO_CENTERED'] = '1'


# =============================================================================
# BACKEND — toàn bộ logic xử lý trên grille số nguyên (int grid)
# =============================================================================

class BackEnd():

    @staticmethod
    def extrait_information(nom_fich):
        """Đọc file CSV, trả về grille 2D số nguyên."""
        grille = []
        with open(nom_fich, newline="") as f:
            reader = csv.reader(f, delimiter=" ")
            for row in reader:
                grille.append([int(ele) for ele in row])
        return grille

    @staticmethod
    def nb_type_bonbons(g):
        nb = g[0][0]
        for row in g:
            for val in row:
                if val > nb:
                    nb = val
        return nb + 1

    @staticmethod
    def est_valid(g, c):
        x, y = c
        return 0 <= x < len(g) and 0 <= y < len(g[0])

    @staticmethod
    def sont_voisins(g, c1, c2):
        x1, y1 = c1
        x2, y2 = c2
        if BackEnd.est_valid(g, c1) and BackEnd.est_valid(g, c2):
            if abs(x1 - x2) == 1 and y1 == y2:
                return True
            if abs(y1 - y2) == 1 and x1 == x2:
                return True
        return False

    @staticmethod
    def detecter_alignement_hori(g):
        alignements = []
        nb_lignes = len(g)
        nb_colonnes = len(g[0])
        for i in range(nb_lignes):
            k = 0
            while k < nb_colonnes:
                debut = k
                couleur = g[i][k]
                while k < nb_colonnes and g[i][k] == couleur and couleur != -1:
                    k += 1
                if k - debut >= 3:
                    for j in range(debut, k):
                        alignements.append([i, j])
                if k == debut:
                    k += 1
        return alignements

    @staticmethod
    def detecter_alignement_verti(g):
        # BUG FIX #1 : les deux blocs `if` étaient à l'intérieur du while interne
        # → ils doivent être au même niveau que le while interne (après sa fermeture)
        alignements = []
        nb_lignes = len(g)
        nb_colonnes = len(g[0])
        for j in range(nb_colonnes):
            k = 0
            while k < nb_lignes:
                debut = k
                couleur = g[k][j]
                while k < nb_lignes and g[k][j] == couleur and couleur != -1:
                    k += 1
                # ← ngoài vòng while con
                if k - debut >= 3:
                    for i in range(debut, k):
                        alignements.append([i, j])
                if k == debut:
                    k += 1
        return alignements

    @staticmethod
    def detecter_alignement(grille):
        seen = set()
        result = []
        for c in BackEnd.detecter_alignement_hori(grille) + BackEnd.detecter_alignement_verti(grille):
            key = (c[0], c[1])
            if key not in seen:
                seen.add(key)
                result.append(c)
        return result

    @staticmethod
    def echanger(g, c1, c2):
        if BackEnd.sont_voisins(g, c1, c2):
            x1, y1 = c1
            x2, y2 = c2
            g[x1][y1], g[x2][y2] = g[x2][y2], g[x1][y1]

    @staticmethod
    def est_echange_valide(g, c1, c2):
        BackEnd.echanger(g, c1, c2)
        possible = len(BackEnd.detecter_alignement(g)) > 0
        BackEnd.echanger(g, c1, c2)
        return possible

    @staticmethod
    def supprimer_alignements_v2(g, a):
        """
        Supprime tous les bonbons de même valeur qui sont voisins d’un bonbon supprimé (un des 3 bonbons) d’origine, ou un voisins de voisin)
        """
        for c in a:
            x = c[0]
            y = c[1]
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if BackEnd.est_valid(g,[nx,ny]) and [nx,ny] not in a and g[nx][ny] == g[x][y]:
                    a.append([nx,ny])
        for liste in a :
            ligne = liste[0]
            col = liste[1]
            g[ligne][col] = -1
        return g

    @staticmethod
    def genere_grille(g, nb_type_bonbons):
        """Fait tomber les bonbons restants et génère de nouveaux en haut."""
        for j in range(len(g[0])):
            ligne = len(g) - 1
            for i in range(len(g) - 1, -1, -1):
                if g[i][j] != -1:
                    g[ligne][j], g[i][j] = g[i][j], g[ligne][j]
                    ligne -= 1
            for i in range(ligne, -1, -1):
                g[i][j] = randint(0, nb_type_bonbons - 1)

    @staticmethod
    def existe_combinaison(grille):
        nb_lignes = len(grille)
        nb_colonnes = len(grille[0])
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                if j + 1 < nb_colonnes and BackEnd.est_echange_valide(grille, [i, j], [i, j + 1]):
                    return True
                if i + 1 < nb_lignes and BackEnd.est_echange_valide(grille, [i, j], [i + 1, j]):
                    return True
        return False


# =============================================================================
# CONFIG
# =============================================================================

class Config():
    CSV_PATH = 'exemple_grille.csv'   # ← adaptez ce chemin
    grille_init = BackEnd.extrait_information(CSV_PATH)

    fps = 24
    window_height = 600
    window_width  = 600

    boardwidth  = len(grille_init[0])   # colonnes
    boardheight = len(grille_init)      # lignes

    bonbon_size     = 64
    nb_type_bonbons = BackEnd.nb_type_bonbons(grille_init)
    assert nb_type_bonbons >= 5, "Il faut au moins 5 types de bonbons"

    moverate = 15

    violet = (255,   0, 255)
    bleu   = (170, 190, 255)
    vert   = (114, 199, 177)
    rouge  = (255, 100, 100)
    noir   = (  0,   0,   0)
    marron = ( 85,  65,   0)
    rose   = (255, 192, 203)

    hightlight      = violet
    bgcolor         = noir
    gameovercolor   = rouge
    gameovercolorbg = noir
    scorecolor      = vert
    liste_couleur   = [violet, bleu, vert, rouge, marron, rose]

    xmargin = int((window_width  - bonbon_size * boardwidth)  / 2)
    ymargin = int((window_height - bonbon_size * boardheight) / 2)


# =============================================================================
# GAME STATE — grille stockée en entiers pour les fonctions BackEnd
# =============================================================================

class GameState():
    def __init__(self):
        grille_init = BackEnd.extrait_information(Config.CSV_PATH)
        self.nb_type_bonbons = BackEnd.nb_type_bonbons(grille_init)
        self.score = 0

        # BUG FIX #2 : grille contient des int, PAS des objets Bonbon
        self.grille = [row[:] for row in grille_init]

        # Nettoyer les alignements initiaux
        a = BackEnd.detecter_alignement(self.grille)
        while a:
            BackEnd.supprimer_alignements_v2(self.grille, a)
            BackEnd.genere_grille(self.grille, self.nb_type_bonbons)
            a = BackEnd.detecter_alignement(self.grille)

    def update(self, c1, c2):
        # BUG FIX #3 : on vérifie AVANT d'échanger (est_echange_valide fait le swap/unswap en interne)
        if not BackEnd.sont_voisins(self.grille, c1, c2):
            return
        if not BackEnd.est_echange_valide(self.grille, c1, c2):
            return
        BackEnd.echanger(self.grille, c1, c2)
        a = BackEnd.detecter_alignement(self.grille)
        while a:
            BackEnd.supprimer_alignements_v2(self.grille, a)
            BackEnd.genere_grille(self.grille, self.nb_type_bonbons)
            self.score += len(a)
            a = BackEnd.detecter_alignement(self.grille)


# =============================================================================
# USER INTERFACE
# =============================================================================

class UserInterface():
    def __init__(self):
        pygame.init()

        self.gameState = GameState()

        # BUG FIX #5 : basic_font était une variable locale → maintenant self.basic_font
        self.basic_font = pygame.font.Font(None, 36)   # remplacez None par 'kenpixel.ttf' si dispo

        # BUG FIX #4 : utiliser les dimensions de fenêtre, pas les dimensions du plateau
        self.window = pygame.display.set_mode((Config.window_width, Config.window_height))
        pygame.display.set_caption("Candy Crush")

        self.clock   = pygame.time.Clock()
        self.running = True

        # BUG FIX #6 : centre du cercle = (bonbon_size//2, bonbon_size//2), PAS (0, 0)
        self.bonbons_liste = []
        center = (Config.bonbon_size // 2, Config.bonbon_size // 2)
        radius = Config.bonbon_size // 2 - 2
        for i in range(Config.nb_type_bonbons):
            surface = pygame.Surface((Config.bonbon_size, Config.bonbon_size), pygame.SRCALPHA)
            pygame.draw.circle(surface, Config.liste_couleur[i], center, radius)
            self.bonbons_liste.append(surface)

        self.first_select      = None
        self.lastX             = None
        self.lastY             = None
        self.cliked            = None
        self.click_continue      = None
        self.click_continue_rect = None   # BUG FIX #11 : stocker comme attribut d'instance

        # grille_cor[x][y] : x = colonne, y = ligne → Rect pixel
        self.grille_cor = []
        for x in range(Config.boardwidth):
            self.grille_cor.append([])
            for y in range(Config.boardheight):
                rect = pygame.Rect(
                    Config.xmargin + x * Config.bonbon_size,
                    Config.ymargin + y * Config.bonbon_size,
                    Config.bonbon_size,
                    Config.bonbon_size
                )
                self.grille_cor[x].append(rect)

    # -------------------------------------------------------------------------

    def checkForGemClick(self, pos):
        # BUG FIX #8 : retourner les coordonnées de la grille [col, row], PAS la position pixel
        for x in range(Config.boardwidth):
            for y in range(Config.boardheight):
                if self.grille_cor[x][y].collidepoint(pos[0], pos[1]):
                    return [x, y]
        return None

    def processInput(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # BUG FIX #13 : K_ESCAPE est une constante de touche, pas un type d'événement
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.lastX, self.lastY = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.pos == (self.lastX, self.lastY):
                    clicked = self.checkForGemClick(event.pos)
                    if clicked:
                        if self.first_select is None:
                            self.first_select = clicked
                        else:
                            self.cliked = clicked
                else:
                    # BUG FIX #7 : suppression du `self` en trop dans l'appel
                    self.first_select = self.checkForGemClick([self.lastX, self.lastY])
                    self.cliked       = self.checkForGemClick(list(event.pos))
                    if not self.first_select or not self.cliked:
                        self.first_select = None
                        self.cliked       = None

    def update(self, c1, c2):
        if c1 is not None and c2 is not None:
            # grille_cor utilise [col, row] mais BackEnd attend [row, col]
            c1_be = [c1[1], c1[0]]
            c2_be = [c2[1], c2[0]]
            self.gameState.update(c1_be, c2_be)
            self.first_select = None
            self.cliked       = None

        if not BackEnd.existe_combinaison(self.gameState.grille):
            self.running = False

    def drawBoard(self):
        for x in range(Config.boardwidth):
            for y in range(Config.boardheight):
                pygame.draw.rect(self.window, Config.bgcolor, self.grille_cor[x][y])
                # BUG FIX #9 : grille est row-major → grille[row][col] = grille[y][x]
                couleur_idx = self.gameState.grille[y][x]
                if couleur_idx != -1:
                    self.window.blit(self.bonbons_liste[couleur_idx], self.grille_cor[x][y])

    def drawScore(self):
        # BUG FIX #10 : self.window au lieu de pygame.DISPLAYSURF ; typo bottomleft corrigé
        score_surf = self.basic_font.render(str(self.gameState.score), True, Config.scorecolor)
        score_rect = score_surf.get_rect()
        score_rect.bottomleft = (10, Config.window_height - 6)   # ← "bottomleft" (corrigé)
        self.window.blit(score_surf, score_rect)
    
    def move(self,bonbon, new_pos, progress):
        movex = new_pos[0] - bonbon[0]
        movey = new_pos[1] - bonbon[1]
        progress *= 0.01
        if (bonbon[1] == Config.row_above_board):
            bonbon[1] = -1
        pixelx = Config.xmargin + (bonbon[0] * Config.bonbon_size)
        pixely = Config.ymargin + (bonbon[1] * Config.bonbon_size)
        return pixelx + movex, pixely + movey, pygame.Rect((pixelx + movex, pixely + movey, Config.bonbon_size, Config.bonbon_size))

    def renderHightlight(self, x, y):
        pygame.draw.rect(self.window, Config.hightlight, self.grille_cor[x][y], 4)
    
    def renderAnimateMoving(self,bonbons,points_text=0):
        progress = 0
        bonbon_0 = bonbons[0]
        bonbon_1 = bonbons[1]
        if bonbon_0 == None or bonbon_1 == None:
            pass
        else:
            while progress < 100: 
                    self.window.fill(Config.bgcolor)
                    self.drawBoard()
                    bonbon_0[0],bonbon_0[1],bonbon_0_image = self.move(bonbon_0,bonbon_1,progress)
                    self. window.blit(bonbon_0, bonbon_0_image)
                    bonbon_1[0],bonbon_1[1],bonbon_1_image = self.move(bonbon_1,bonbon_0,progress)
                    self. window.blit(bonbon_1, bonbon_1_image)
                    self.drawScore()
                    """
                    for pointText in points_text:
                        pointsSurf = self.basic_font.render(str(pointText['points']), 1, Config.scorecolor)
                        pointsRect = pointsSurf.get_rect()
                        pointsRect.center = (pointText['x'], pointText['y'])
                        pygame.DISPLAYSURF.blit(pointsSurf, pointsRect)
                    """
                    pygame.display.update()
                    self.clock.tick(Config.fps)
                    progress += Config.moverate

    def render(self):
        self.window.fill(Config.bgcolor)
        self.drawBoard()

        if self.first_select is not None:
            self.renderHightlight(self.first_select[0], self.first_select[1])

        if not self.running:
            # BUG FIX #11 : click_continue_rect stocké comme self.click_continue_rect
            if self.click_continue is None:
                self.click_continue = self.basic_font.render(
                    'Final Score: %s  (Click to continue)' % self.gameState.score,
                    True, Config.gameovercolor, Config.gameovercolorbg
                )
                self.click_continue_rect = self.click_continue.get_rect()
                self.click_continue_rect.center = (Config.window_width // 2, Config.window_height // 2)
            self.window.blit(self.click_continue, self.click_continue_rect)

        # BUG FIX #11 : drawScore() sans argument
        bonbons = [self.first_select,self.cliked]
        if len(bonbons) == 2:
            self.renderAnimateMoving(bonbons)
        self.drawScore()
        pygame.display.update()

    def run(self):
        while self.running:
            self.processInput()
            self.update(self.first_select, self.cliked)
            self.render()
            self.clock.tick(Config.fps)


# =============================================================================

if __name__ == '__main__':
    ui = UserInterface()
    ui.run()
    pygame.quit()