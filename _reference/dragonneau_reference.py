# ============================================================
# Le Dragonneau — implémentation de RÉFÉRENCE (bloc 2)
# ============================================================
# Ce fichier n'est PAS un fichier d'élève. C'est la cible : l'état
# du jeu à la fin de la leçon 12, avant le port MakeCode (leçon 13).
# Il sert à trois choses :
#   1. montrer où on s'en va,
#   2. vérifier que les constantes de COURS_FORMAT.md section 9 tiennent,
#   3. servir de corrigé au père.
#
# Contraintes MakeCode Arcade respectées : 160x120 logique, 16 couleurs,
# un seul bouton de jeu, aucun fichier d'image ni de son.
#
# Lancer :  python dragonneau_reference.py
#   ESPACE  plonger        1-4  changer de thème
#   R       recommencer    ÉCHAP  quitter
# ============================================================

import math
import sys

import pygame

# --- Écran ---------------------------------------------------
LARGEUR, HAUTEUR = 160, 120      # résolution logique (= MakeCode Arcade)
ZOOM = 4                         # fenêtre 640x480
X_HEROS = 40                     # le héros reste à cette colonne

# --- Terrain : des collines-TREMPLINS (voir COURS_FORMAT §9.3) ---
L_COLLINE        = 200           # longueur d'une colline
R_DESCENTE       = 0.68          # part occupée par la descente
CRETE            = 46            # y du sommet (constant : les collines se raccordent)
D_MIN, D_MAX     = 30, 65        # dénivelé, tiré au sort par colline

# --- Physique (calibrée par simulation — voir COURS_FORMAT §9.3) ---
GRAVITE          = 0.14
GRAVITE_PLONGEON = 0.80
ACCEL_DESCENTE   = 0.22
FREIN_MONTEE     = 0.28          # > ACCEL_DESCENTE : c'est le coeur du game design
FRICTION         = 0.997
VX_MIN, VX_MAX   = 1.2, 9.0
VX_JAUGE_MAX     = 7.0           # affichage seulement : VX_MAX n'est jamais atteint
SUIVI_CAMERA     = 0.14
HAUTEUR_VISEE    = 60

# --- Zoom arrière : obligatoire, les vols dépassent l'écran (§9.4) ---
ZOOM_MIN         = 0.45
HAUTEUR_ZOOM     = 80            # altitude à laquelle le zoom est complètement ouvert
SUIVI_ZOOM       = 0.12

# --- Thèmes --------------------------------------------------
THEMES = [
    {"nom": "Dragonneau",
     "ciel": (38, 28, 66), "ciel2": (92, 52, 90),
     "collines": (58, 138, 68), "ombre": (32, 92, 48),
     "heros": (232, 92, 56), "heros2": (170, 58, 34),
     "gravite": 0.14},
    {"nom": "Ski",
     "ciel": (28, 44, 86), "ciel2": (96, 140, 190),
     "collines": (238, 244, 252), "ombre": (168, 190, 220),
     "heros": (240, 80, 70), "heros2": (170, 46, 42),
     "gravite": 0.14},
    {"nom": "Lune",
     "ciel": (8, 8, 20), "ciel2": (40, 36, 64),
     "collines": (150, 148, 158), "ombre": (92, 90, 102),
     "heros": (238, 238, 238), "heros2": (150, 150, 160),
     "gravite": 0.08},           # un thème peut changer le GAMEPLAY
    {"nom": "Dauphin",
     "ciel": (20, 60, 110), "ciel2": (88, 170, 210),
     "collines": (30, 110, 170), "ombre": (18, 72, 120),
     "heros": (190, 225, 240), "heros2": (110, 165, 195),
     "gravite": 0.14},
]

# --- Sprite du héros -----------------------------------------
# Dessiné en toutes lettres plutôt que chargé d'un fichier : zéro octet
# de flash sur la console, et Adam peut le modifier caractère par caractère.
#   C = corps    D = corps foncé    A = aile    O = oeil    . = transparent
DRAGON_AILE_HAUTE = [
    "......AAAA......",
    ".....AAAAAA.....",
    "....AAAAAAA.....",
    "....AAAAAA.D.D..",
    "......CCCCCCCC..",
    "D....CCCCCCCCC..",
    "DD..CCCCCCCOCCC.",
    ".DDCCCCCCCCCCCCC",
    "..DCCCCCCCCCCC..",
    "...DCCCCCCCC....",
    "....DDDDDD......",
    "................",
]
DRAGON_AILE_BASSE = [
    "................",
    "................",
    "................",
    "......CC...D.D..",
    "......CCCCCCCC..",
    "D....CCCCCCCCC..",
    "DD..CCCCCCCOCCC.",
    ".DDCCCCCCCCCCCCC",
    "..DCCCCAAACCCC..",
    "...DCCAAAAAA....",
    "....DAAAAAA.....",
    ".....AAAA.......",
]


def faire_sprite(motif, theme):
    """Transforme un motif texte en Surface pygame, aux couleurs du thème."""
    h = len(motif)
    w = len(motif[0])
    surf = pygame.Surface((w, h), pygame.SRCALPHA)
    couleurs = {
        "C": theme["heros"],
        "D": theme["heros2"],
        "A": theme["heros2"],
        "O": (20, 20, 28),
    }
    for y, ligne in enumerate(motif):
        for x, c in enumerate(ligne):
            if c in couleurs:
                surf.set_at((x, y), couleurs[c])
    return surf


POLICE = None    # initialisée dans main()


def hauteur_du_sol(x):
    """Le y du sol à la position x du monde. y = 0 en haut de l'écran.

    Chaque colline est un TREMPLIN : longue descente douce en cosinus,
    puis rampe droite qui casse net au sommet. C'est l'angle du sommet
    qui projette le dragonneau — une colline arrondie ne décolle pas.
    """
    i = int(x // L_COLLINE)
    d = D_MIN + (D_MAX - D_MIN) * ((i * 7919) % 1000) / 1000
    t = (x % L_COLLINE) / L_COLLINE
    if t < R_DESCENTE:
        u = t / R_DESCENTE
        return CRETE + d * (1 - math.cos(math.pi * u)) / 2
    u = (t - R_DESCENTE) / (1 - R_DESCENTE)
    return CRETE + d * (1 - u)


class Jeu:
    def __init__(self, i_theme=0):
        self.i_theme = i_theme
        self.theme = THEMES[i_theme]
        self.recommencer()
        self.refaire_sprites()

    def refaire_sprites(self):
        self.sprites = [faire_sprite(DRAGON_AILE_HAUTE, self.theme),
                        faire_sprite(DRAGON_AILE_BASSE, self.theme)]
        self.fond = self.faire_ciel()

    def faire_ciel(self):
        """Dégradé vertical pré-calculé une seule fois."""
        s = pygame.Surface((1, HAUTEUR))
        c1, c2 = self.theme["ciel"], self.theme["ciel2"]
        for y in range(HAUTEUR):
            t = y / HAUTEUR
            s.set_at((0, y), tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
        return pygame.transform.scale(s, (LARGEUR, HAUTEUR))

    def changer_theme(self, i):
        self.i_theme = i % len(THEMES)
        self.theme = THEMES[self.i_theme]
        self.refaire_sprites()

    def recommencer(self):
        self.camera_x = 0.0
        self.y = hauteur_du_sol(0)
        self.vy = 0.0
        self.vx = 2.0
        self.zoom = 1.0
        self.camera_y = self.y - HAUTEUR_VISEE
        self.au_sol = True
        self.temps_en_vol = 0
        self.meilleur_vol = 0
        self.animation = 0.0
        self.gain_atterrissage = 0.0
        self.eclat = 0

    # --- Le moteur, exactement comme dans COURS_FORMAT §9.3 ---
    def mettre_a_jour(self, bouton_tenu):
        gravite = self.theme["gravite"]
        self.vy += GRAVITE_PLONGEON if bouton_tenu else gravite
        self.y += self.vy

        sol = hauteur_du_sol(self.camera_x)
        if self.y >= sol:
            self.y = sol
            pente = hauteur_du_sol(self.camera_x + 1) - sol

            if not self.au_sol:
                # ATTERRISSAGE — la ligne la plus importante du jeu.
                # Seule la vitesse PARALLELE au sol survit à l'impact.
                # Aligné sur une descente -> on gagne. De travers -> on perd tout.
                self.meilleur_vol = max(self.meilleur_vol, self.temps_en_vol)
                avant = self.vx
                self.vx = (self.vx + self.vy * pente) / (1 + pente * pente)
                self.vx = max(VX_MIN, min(VX_MAX, self.vx))
                self.gain_atterrissage = self.vx - avant
                self.eclat = 12 if self.gain_atterrissage > 0.15 else 0

            self.au_sol = True
            self.temps_en_vol = 0
            self.vy = pente * self.vx
            self.vx += pente * (ACCEL_DESCENTE if pente > 0 else FREIN_MONTEE)
            self.vx = max(VX_MIN, min(VX_MAX, self.vx * FRICTION))
        else:
            self.au_sol = False
            self.temps_en_vol += 1

        # Zoom arrière selon l'altitude : sans lui, on ne voit plus le sol
        # au sommet d'un vol — donc on ne peut plus viser son atterrissage.
        hauteur_de_vol = max(0.0, sol - self.y)
        zoom_vise = 1.0 - (1.0 - ZOOM_MIN) * min(1.0, hauteur_de_vol / HAUTEUR_ZOOM)
        self.zoom += (zoom_vise - self.zoom) * SUIVI_ZOOM

        self.camera_x += self.vx
        self.camera_y += ((self.y - HAUTEUR_VISEE / self.zoom) - self.camera_y) * SUIVI_CAMERA
        self.animation += 0.25 if self.au_sol else 0.12
        if self.eclat > 0:
            self.eclat -= 1

    def dessiner(self, surf):
        t = self.theme
        surf.blit(self.fond, (0, 0))

        # Le terrain, une colonne verticale par pixel d'écran.
        # Même forme de code qu'en MakeCode Arcade (image.drawLine).
        z = self.zoom
        for ex in range(LARGEUR):
            monde_x = self.camera_x + (ex - X_HEROS) / z
            sy = int((hauteur_du_sol(monde_x) - self.camera_y) * z)
            if sy < HAUTEUR:
                pygame.draw.line(surf, t["collines"], (ex, sy), (ex, HAUTEUR))
                pygame.draw.line(surf, t["ombre"], (ex, sy),
                                 (ex, min(sy + max(1, int(3 * z)), HAUTEUR)))

        # Le héros — il rapetisse avec le zoom (sur la console : 2 tailles de sprite)
        img = self.sprites[int(self.animation) % 2]
        if z < 0.75:
            img = pygame.transform.scale(img, (max(6, int(16 * z)), max(5, int(12 * z))))
        ey = int((self.y - self.camera_y) * z)
        surf.blit(img, (X_HEROS - img.get_width() // 2, ey - img.get_height() // 2))

        # Éclat blanc quand l'atterrissage a fait GAGNER de la vitesse
        if self.eclat > 0:
            pygame.draw.circle(surf, (255, 255, 255), (X_HEROS, ey), 10 - self.eclat // 2, 1)

        # HUD : distance + jauge de vitesse
        distance = int(self.camera_x / 10)
        self.texte(surf, f"{distance} m", 3, 3, (255, 255, 255))
        remplissage = int(24 * (self.vx - VX_MIN) / (VX_JAUGE_MAX - VX_MIN))
        remplissage = max(0, min(24, remplissage))
        pygame.draw.rect(surf, (255, 255, 255), (LARGEUR - 29, 4, 26, 5), 1)
        if remplissage > 0:
            pygame.draw.rect(surf, t["heros"], (LARGEUR - 28, 5, remplissage, 3))
        if not self.au_sol and self.temps_en_vol > 25:
            self.texte(surf, "SUPER VOL !", 48, 20, (255, 232, 120))

    def texte(self, surf, s, x, y, couleur):
        img = POLICE.render(s, False, couleur)
        surf.blit(img, (x, y))


def main():
    global POLICE
    pygame.init()
    POLICE = pygame.font.SysFont("consolas", 8)
    ecran = pygame.display.set_mode((LARGEUR * ZOOM, HAUTEUR * ZOOM))
    pygame.display.set_caption("Le Dragonneau — référence")
    surf = pygame.Surface((LARGEUR, HAUTEUR))
    horloge = pygame.time.Clock()
    jeu = Jeu()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if e.key == pygame.K_r:
                    jeu.recommencer()
                if pygame.K_1 <= e.key <= pygame.K_4:
                    jeu.changer_theme(e.key - pygame.K_1)

        touches = pygame.key.get_pressed()
        jeu.mettre_a_jour(touches[pygame.K_SPACE])
        jeu.dessiner(surf)

        pygame.transform.scale(surf, ecran.get_size(), ecran)
        pygame.display.flip()
        horloge.tick(60)


if __name__ == "__main__":
    main()
