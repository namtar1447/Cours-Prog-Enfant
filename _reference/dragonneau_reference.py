# ============================================================
# Le Dragonneau — implémentation de RÉFÉRENCE (bloc 2)
# ============================================================
# Ce fichier n'est PAS un fichier d'élève. C'est la cible : l'état
# du jeu à la fin de la leçon 13, avant le port MakeCode (leçon 14).
#
# Contraintes MakeCode Arcade respectées : 160x120 logique, 16 couleurs,
# un seul bouton de jeu, aucun fichier d'image ni de son.
#
# Lancer :  python dragonneau_reference.py
#
#   ESPACE   plonger / se coller à la pente
#   1-4      changer de thème
#   T        changer la FORME des collines
#   F1       ouvrir/fermer le panneau de réglages
#   ↑ ↓      choisir un réglage        ← →   le modifier
#   F5       remettre les réglages d'origine
#   R        recommencer               ÉCHAP  quitter
# ============================================================

import math
import sys

import pygame

# --- Écran ---------------------------------------------------
LARGEUR, HAUTEUR = 160, 120      # résolution logique (= MakeCode Arcade)
ZOOM_FENETRE = 4                 # fenêtre 640x480
X_HEROS = 40                     # le héros reste à cette colonne


# ============================================================
# LES RÉGLAGES — tous modifiables en direct avec F1
# ============================================================
# (valeur, minimum, maximum, pas, explication courte)
DEFAUTS = {
    "GRAVITE":          (0.08, 0.02, 0.40, 0.01, "chute en planant"),
    "GRAVITE_PLONGEON": (0.30, 0.05, 1.20, 0.05, "chute bouton tenu"),
    "ACCEL_DESCENTE":   (0.22, 0.02, 0.60, 0.02, "gain en descente"),
    "FREIN_MONTEE":     (0.28, 0.02, 0.60, 0.02, "perte en montee"),
    "BONUS_PLONGEON":   (2.60, 1.00, 5.00, 0.20, "x accel si bouton en DESCENTE"),
    "MALUS_PLONGEON":   (3.50, 1.00, 5.00, 0.20, "x frein si bouton en MONTEE"),
    "FRICTION":         (0.997, 0.980, 1.000, 0.001, "perte continue"),
    "VX_MAX":           (9.0, 3.0, 16.0, 0.5, "vitesse maximale"),
    "L_COLLINE":        (200, 100, 400, 10, "longueur d'une colline"),
    "D_MIN":            (30, 5, 80, 5, "denivele mini"),
    "D_MAX":            (65, 10, 110, 5, "denivele maxi"),
    "R_DESCENTE":       (0.62, 0.30, 0.90, 0.02, "part en descente"),
    "POINTE":           (2.2, 1.0, 5.0, 0.1, "nettete du sommet"),
    "ZOOM_MIN":         (0.30, 0.15, 1.00, 0.05, "zoom le plus large"),
    "SEUIL_ZOOM":       (50, 0, 150, 5, "altitude SOUS laquelle on ne zoome pas"),
    "HAUTEUR_ZOOM":     (190, 60, 400, 10, "altitude du zoom complet"),
    "SUIVI_SORTIE":     (0.07, 0.02, 0.40, 0.01, "vitesse pour s'eloigner"),
    "SUIVI_RETOUR":     (0.10, 0.02, 0.40, 0.01, "vitesse pour revenir"),
    "MARGE_SOL":        (8, 0, 40, 2, "px de sol garantis a l'ecran"),
    "VISEE_BAS":        (60, 20, 100, 2, "hauteur du heros au sol"),
    "VISEE_HAUT":       (26, 6, 100, 2, "hauteur du heros en vol"),
    "SUIVI_CAMERA":     (0.10, 0.02, 0.50, 0.02, "vitesse de la camera"),
}
ORDRE = list(DEFAUTS)
R = {k: v[0] for k, v in DEFAUTS.items()}     # les valeurs courantes

VX_MIN = 1.2
CRETE = 46                                    # y du sommet des collines


# ============================================================
# LA FORME DES COLLINES
# ============================================================
# On quitte le sol quand  courbure x vx^2 / 2 > gravite, donc au point de
# COURBURE MAXIMALE. Toute la question est : quelle est la PENTE a cet
# endroit ? Si la courbure culmine au sommet (pente 0), on ne decolle pas.
#
#   goutte    sommet lisse, courbure maximale AVANT le sommet  -> saute, et joli
#   tremplin  rampe droite, angle net au sommet                -> saute, mais moche
#   vague     sinus deforme, tout doux                         -> ne saute presque pas
#   arrondi   rampe en puissance                               -> courbure au sommet, mou

def _forme_goutte(u):
    return math.cos(math.pi * u / 2) ** R["POINTE"]

def _forme_tremplin(u):
    return 1 - u

def _forme_vague(u):
    return (1 + math.cos(math.pi * u)) / 2

def _forme_arrondi(u):
    return (1 - u) ** max(1.05, R["POINTE"] / 2)

FORMES = [("goutte", _forme_goutte), ("tremplin", _forme_tremplin),
          ("vague", _forme_vague), ("arrondi", _forme_arrondi)]
i_forme = 0


def hauteur_du_sol(x):
    """Le y du sol à la position x du monde. y = 0 en haut de l'écran."""
    L = R["L_COLLINE"]
    i = int(x // L)
    d_min, d_max = R["D_MIN"], max(R["D_MIN"], R["D_MAX"])
    d = d_min + (d_max - d_min) * ((i * 7919) % 1000) / 1000
    t = (x % L) / L
    r = R["R_DESCENTE"]
    if t < r:                                       # la descente, longue et douce
        return CRETE + d * (1 - math.cos(math.pi * t / r)) / 2
    u = (t - r) / (1 - r)                           # la remontée, selon la forme choisie
    return CRETE + d * FORMES[i_forme][1](u)


# --- Thèmes --------------------------------------------------
THEMES = [
    {"nom": "Dragonneau",
     "ciel": (38, 28, 66), "ciel2": (92, 52, 90),
     "collines": (58, 138, 68), "ombre": (32, 92, 48),
     "heros": (232, 92, 56), "heros2": (170, 58, 34)},
    {"nom": "Ski",
     "ciel": (28, 44, 86), "ciel2": (96, 140, 190),
     "collines": (238, 244, 252), "ombre": (168, 190, 220),
     "heros": (240, 80, 70), "heros2": (170, 46, 42)},
    {"nom": "Lune",
     "ciel": (8, 8, 20), "ciel2": (40, 36, 64),
     "collines": (150, 148, 158), "ombre": (92, 90, 102),
     "heros": (238, 238, 238), "heros2": (150, 150, 160)},
    {"nom": "Dauphin",
     "ciel": (20, 60, 110), "ciel2": (88, 170, 210),
     "collines": (30, 110, 170), "ombre": (18, 72, 120),
     "heros": (190, 225, 240), "heros2": (110, 165, 195)},
]

# --- Sprite du héros -----------------------------------------
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
    surf = pygame.Surface((len(motif[0]), len(motif)), pygame.SRCALPHA)
    couleurs = {"C": theme["heros"], "D": theme["heros2"],
                "A": theme["heros2"], "O": (20, 20, 28)}
    for y, ligne in enumerate(motif):
        for x, c in enumerate(ligne):
            if c in couleurs:
                surf.set_at((x, y), couleurs[c])
    return surf


POLICE = None


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
        self.visee = R["VISEE_BAS"]
        self.camera_y = self.y - R["VISEE_BAS"]
        self.au_sol = True
        self.temps_en_vol = 0
        self.meilleur_vol = 0
        self.animation = 0.0
        self.gain_atterrissage = 0.0
        self.eclat = 0
        self.vx_max_vu = 0.0
        self.hauteur_max_vue = 0.0
        self.plafond_actif = False

    # --- Le moteur --------------------------------------------
    def mettre_a_jour(self, bouton_tenu):
        self.vy += R["GRAVITE_PLONGEON"] if bouton_tenu else R["GRAVITE"]
        self.y += self.vy

        sol = hauteur_du_sol(self.camera_x)
        if self.y >= sol:
            self.y = sol
            pente = hauteur_du_sol(self.camera_x + 1) - sol

            if not self.au_sol:
                # ATTERRISSAGE : seule la vitesse PARALLELE au sol survit.
                # Aligné sur une descente -> on gagne. De travers -> on perd.
                self.meilleur_vol = max(self.meilleur_vol, self.temps_en_vol)
                avant = self.vx
                self.vx = (self.vx + self.vy * pente) / (1 + pente * pente)
                self.vx = max(VX_MIN, min(R["VX_MAX"], self.vx))
                self.gain_atterrissage = self.vx - avant
                self.eclat = 12 if self.gain_atterrissage > 0.15 else 0

            self.au_sol = True
            self.temps_en_vol = 0
            self.vy = pente * self.vx

            # LE BOUTON AGIT AUSSI AU SOL — c'est là qu'est le jeu :
            #   tenir en DESCENTE -> on se colle à la pente, on accélère fort
            #   tenir en MONTEE   -> on s'écrase dans la côte, on freine fort
            if pente > 0:
                accel = R["ACCEL_DESCENTE"] * (R["BONUS_PLONGEON"] if bouton_tenu else 1.0)
            else:
                accel = R["FREIN_MONTEE"] * (R["MALUS_PLONGEON"] if bouton_tenu else 1.0)
            self.vx = max(VX_MIN, min(R["VX_MAX"], (self.vx + pente * accel) * R["FRICTION"]))
        else:
            self.au_sol = False
            self.temps_en_vol += 1

        self.vx_max_vu = max(self.vx_max_vu, self.vx)
        self.hauteur_max_vue = max(self.hauteur_max_vue, sol - self.y)

        # --- Zoom : deux règles superposées ---------------------
        # 1. le CONFORT : rien tant qu'on vole bas (SEUIL_ZOOM), puis une
        #    rampe douce. C'est ce réglage-là qui donne la sensation.
        # 2. le PLAFOND DE SÉCURITÉ : le zoom maximal qui garde encore le
        #    sol à l'écran. Appliqué APRÈS le lissage, donc la perte du sol
        #    devient impossible quels que soient les réglages de confort.
        # L'altitude se mesure par rapport à la LIGNE DES CRÊTES (constante),
        # jamais par rapport au sol sous le héros : à grande vitesse ce sol
        # balaie tout le dénivelé d'une colline, l'« altitude » tremblerait de
        # 65 px sans que le dragonneau bouge, et la caméra copierait ce tremblement.
        hauteur_de_vol = max(0.0, CRETE - self.y)
        if hauteur_de_vol <= R["SEUIL_ZOOM"]:
            k = 0.0
        else:
            k = min(1.0, (hauteur_de_vol - R["SEUIL_ZOOM"]) /
                    max(1.0, R["HAUTEUR_ZOOM"] - R["SEUIL_ZOOM"]))

        confort = 1.0 - (1.0 - R["ZOOM_MIN"]) * k
        suivi = R["SUIVI_SORTIE"] if confort < self.zoom else R["SUIVI_RETOUR"]
        self.zoom += (confort - self.zoom) * suivi

        # C'est la VISÉE qu'on lisse, pas la caméra. La caméra s'en déduit
        # ensuite exactement : le héros est donc toujours pile à `visee` pixels
        # du haut de l'écran, sans retard et sans dérive possible.
        visee_cible = R["VISEE_BAS"] + (R["VISEE_HAUT"] - R["VISEE_BAS"]) * k
        self.visee += (visee_cible - self.visee) * R["SUIVI_CAMERA"]

        # Le plafond devient une formule fermée : on veut que la ligne des
        # crêtes tombe au-dessus du bas de l'écran, soit
        #     (CRETE - y) * zoom + visee  <=  HAUTEUR - MARGE_SOL
        plafond = (HAUTEUR - R["MARGE_SOL"] - self.visee) / max(1.0, CRETE - self.y)
        self.zoom = max(0.12, min(1.0, plafond, self.zoom))
        self.plafond_actif = plafond < 1.0 and self.zoom >= plafond - 1e-9

        self.camera_x += self.vx
        self.camera_y = self.y - self.visee / self.zoom
        self.animation += 0.25 if self.au_sol else 0.12
        if self.eclat > 0:
            self.eclat -= 1

    # --- Le dessin --------------------------------------------
    def dessiner(self, surf, bouton_tenu=False):
        t = self.theme
        surf.blit(self.fond, (0, 0))

        z = self.zoom
        for ex in range(LARGEUR):
            monde_x = self.camera_x + (ex - X_HEROS) / z
            sy = int((hauteur_du_sol(monde_x) - self.camera_y) * z)
            if sy < HAUTEUR:
                pygame.draw.line(surf, t["collines"], (ex, sy), (ex, HAUTEUR))
                pygame.draw.line(surf, t["ombre"], (ex, sy),
                                 (ex, min(sy + max(1, int(3 * z)), HAUTEUR)))

        img = self.sprites[int(self.animation) % 2]
        if z < 0.85:
            img = pygame.transform.scale(img, (max(5, int(16 * z)), max(4, int(12 * z))))
        ey = int((self.y - self.camera_y) * z)
        surf.blit(img, (X_HEROS - img.get_width() // 2, ey - img.get_height() // 2))

        if self.eclat > 0:
            pygame.draw.circle(surf, (255, 255, 255), (X_HEROS, ey), 10 - self.eclat // 2, 1)

        # HUD
        self.texte(surf, f"{int(self.camera_x / 10)} m", 3, 2, (255, 255, 255))
        plein = int(24 * (self.vx - VX_MIN) / max(0.1, R["VX_MAX"] - VX_MIN))
        plein = max(0, min(24, plein))
        pygame.draw.rect(surf, (255, 255, 255), (LARGEUR - 29, 3, 26, 5), 1)
        if plein > 0:
            pygame.draw.rect(surf, t["heros"], (LARGEUR - 28, 4, plein, 3))
        if bouton_tenu:
            pente = hauteur_du_sol(self.camera_x + 1) - hauteur_du_sol(self.camera_x)
            if self.au_sol:
                bon = pente > 0
                self.texte(surf, "COLLE !" if bon else "FREINE",
                           LARGEUR // 2 - 16, 12,
                           (166, 227, 161) if bon else (243, 139, 168))

    def texte(self, surf, s, x, y, couleur):
        surf.blit(POLICE.render(s, False, couleur), (x, y))


# ============================================================
# Panneau de réglages
# ============================================================
def dessiner_panneau(ecran, i_sel, jeu):
    lignes = len(ORDRE) + 3
    h = lignes * 14 + 10
    fond = pygame.Surface((330, h))
    fond.set_alpha(232)
    fond.fill((16, 16, 26))
    ecran.blit(fond, (6, 6))
    pygame.draw.rect(ecran, (124, 106, 247), (6, 6, 330, h), 1)

    gros = pygame.font.SysFont("consolas", 13)
    y = 12
    ecran.blit(gros.render(f"REGLAGES   forme des collines : {FORMES[i_forme][0]}  (T)",
                           True, (247, 162, 106)), (14, y))
    y += 18
    for i, cle in enumerate(ORDRE):
        actif = (i == i_sel)
        coul = (255, 255, 255) if actif else (150, 150, 170)
        if actif:
            pygame.draw.rect(ecran, (44, 40, 78), (10, y - 1, 322, 14))
        val = R[cle]
        txt = f"{'>' if actif else ' '} {cle:<17} {val:>7.3f}   {DEFAUTS[cle][4]}"
        ecran.blit(gros.render(txt, True, coul), (14, y))
        y += 14
    y += 4
    ecran.blit(gros.render(f"vx max {jeu.vx_max_vu:.1f}   vol max {jeu.meilleur_vol} img"
                           f"   altitude max {jeu.hauteur_max_vue:.0f} px"
                           f"   zoom {jeu.zoom:.2f}"
                           + ("  [PLAFOND]" if jeu.plafond_actif else ""),
                           True, (166, 227, 161)), (14, y))
    y += 14
    ecran.blit(gros.render("F1 fermer   ^v choisir   <> modifier   F5 defaut",
                           True, (108, 112, 134)), (14, y))


def main():
    global POLICE, i_forme
    pygame.init()
    POLICE = pygame.font.SysFont("consolas", 8)
    ecran = pygame.display.set_mode((LARGEUR * ZOOM_FENETRE, HAUTEUR * ZOOM_FENETRE))
    pygame.display.set_caption("Le Dragonneau — référence")
    surf = pygame.Surface((LARGEUR, HAUTEUR))
    horloge = pygame.time.Clock()
    jeu = Jeu()
    panneau, i_sel = False, 0

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type != pygame.KEYDOWN:
                continue
            if e.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            elif e.key == pygame.K_r:
                jeu.recommencer()
            elif e.key == pygame.K_F1:
                panneau = not panneau
            elif e.key == pygame.K_F5:
                for k, v in DEFAUTS.items():
                    R[k] = v[0]
                jeu.recommencer()
            elif e.key == pygame.K_t:
                i_forme = (i_forme + 1) % len(FORMES)
                jeu.recommencer()
            elif pygame.K_1 <= e.key <= pygame.K_4:
                jeu.changer_theme(e.key - pygame.K_1)
            elif panneau and e.key in (pygame.K_UP, pygame.K_DOWN):
                i_sel = (i_sel + (1 if e.key == pygame.K_DOWN else -1)) % len(ORDRE)
            elif panneau and e.key in (pygame.K_LEFT, pygame.K_RIGHT):
                cle = ORDRE[i_sel]
                _, mini, maxi, pas, _ = DEFAUTS[cle]
                signe = 1 if e.key == pygame.K_RIGHT else -1
                R[cle] = round(max(mini, min(maxi, R[cle] + signe * pas)), 4)

        touches = pygame.key.get_pressed()
        bouton = touches[pygame.K_SPACE]
        jeu.mettre_a_jour(bouton)
        jeu.dessiner(surf, bouton)

        pygame.transform.scale(surf, ecran.get_size(), ecran)
        if panneau:
            dessiner_panneau(ecran, i_sel, jeu)
        pygame.display.flip()
        horloge.tick(60)


if __name__ == "__main__":
    main()
