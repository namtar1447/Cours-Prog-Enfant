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

# --- Physique (calibrée par simulation — voir COURS_FORMAT §9.3) ---
GRAVITE          = 0.14
GRAVITE_PLONGEON = 0.50
ACCEL_DESCENTE   = 0.18
FREIN_MONTEE     = 0.23          # > ACCEL_DESCENTE : c'est le coeur du game design
FRICTION         = 0.997
VX_MIN, VX_MAX   = 1.2, 8.0
VX_JAUGE_MAX     = 6.0           # affichage seulement : VX_MAX n'est jamais atteint
SUIVI_CAMERA     = 0.14
HAUTEUR_VISEE    = 60

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
    """Le y du sol à la position x du monde. y = 0 en haut de l'écran."""
    return 76 + 32 * math.sin(x / 38) + 11 * math.sin(x / 17)


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
        self.camera_y = self.y - HAUTEUR_VISEE
        self.au_sol = True
        self.temps_en_vol = 0
        self.meilleur_vol = 0
        self.animation = 0.0

    # --- Le moteur, exactement comme dans COURS_FORMAT §9.3 ---
    def mettre_a_jour(self, bouton_tenu):
        gravite = self.theme["gravite"]
        self.vy += GRAVITE_PLONGEON if bouton_tenu else gravite
        self.y += self.vy

        sol = hauteur_du_sol(self.camera_x)
        if self.y >= sol:
            if not self.au_sol:
                self.meilleur_vol = max(self.meilleur_vol, self.temps_en_vol)
            self.au_sol = True
            self.temps_en_vol = 0
            self.y = sol
            pente = hauteur_du_sol(self.camera_x + 1) - sol
            self.vy = pente * self.vx
            self.vx += pente * (ACCEL_DESCENTE if pente > 0 else FREIN_MONTEE)
            self.vx = max(VX_MIN, min(VX_MAX, self.vx * FRICTION))
        else:
            self.au_sol = False
            self.temps_en_vol += 1

        self.camera_x += self.vx
        self.camera_y += ((self.y - HAUTEUR_VISEE) - self.camera_y) * SUIVI_CAMERA
        self.animation += 0.25 if self.au_sol else 0.12

    def dessiner(self, surf):
        t = self.theme
        surf.blit(self.fond, (0, 0))

        # Le terrain, une colonne verticale par pixel d'écran.
        # Même forme de code qu'en MakeCode Arcade (image.drawLine).
        for ex in range(LARGEUR):
            sy = int(hauteur_du_sol(self.camera_x + ex - X_HEROS) - self.camera_y)
            if sy < HAUTEUR:
                pygame.draw.line(surf, t["collines"], (ex, sy), (ex, HAUTEUR))
                pygame.draw.line(surf, t["ombre"], (ex, sy), (ex, min(sy + 3, HAUTEUR)))

        # Le héros
        img = self.sprites[int(self.animation) % 2]
        ey = int(self.y - self.camera_y)
        surf.blit(img, (X_HEROS - 7, ey - 7))

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
