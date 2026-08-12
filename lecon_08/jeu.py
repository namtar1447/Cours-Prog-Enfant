# ============================================================
# Leçon 08 — Le bouton unique
# jeu.py — ton jeu, leçon après leçon
# ============================================================
# OBJECTIF : Le rond devient un vrai dragonneau qui bat des ailes,
#            et la barre d'ESPACE le fait plonger.
#
# COMMENT TESTER : Clique sur ▶
#            Puis regarde l'écran et coche la liste « Ça doit faire ça »
#            dans presentation.html.
#
# POUR FERMER : clique le ✕ de la fenêtre, ou appuie sur ÉCHAP
# ============================================================

import pygame

# --- Les réglages du jeu (tu peux y toucher à la fin) ---
LARGEUR, HAUTEUR = 160, 120      # la taille du monde, en pixels
ZOOM = 4                         # la loupe : la fenêtre fait 640 x 480
X_DRAGON = 40                    # le dragonneau reste dans cette colonne
SOL_PLAT = 100                   # la hauteur du sol
PLAFOND = 10                     # il ne monte pas plus haut que ça

GRAVITE = 0.14                   # chute normale, ailes ouvertes
GRAVITE_PLONGEON = 0.40          # chute quand ESPACE est tenu
REBOND = 0.6                     # ce qu'il reste de vitesse après un rebond
REBOND_MINI = 2.4                # le plus petit rebond possible
VITESSE_AILES = 0.15             # combien le compteur d'ailes avance par tour

COULEUR_CIEL   = (38, 28, 66)
COULEUR_SOL    = (58, 138, 68)
COULEUR_OMBRE  = (32, 92, 48)
COULEUR_DRAGON = (232, 92, 56)
COULEUR_AILE   = (168, 52, 40)
COULEUR_OEIL   = (20, 20, 28)


# ============================================================
# --- EXEMPLE (ne pas modifier) ---
# ============================================================
# Comment UN SEUL compteur qui monte tout droit fait clignoter
# deux images à tour de rôle.

compteur = 0.0
compteur += 0.5      # 0.5  →  int(0.5) = 0  →  0 % 2 = 0
compteur += 0.5      # 1.0  →  int(1.0) = 1  →  1 % 2 = 1
compteur += 0.5      # 1.5  →  int(1.5) = 1  →  1 % 2 = 1
compteur += 0.5      # 2.0  →  int(2.0) = 2  →  2 % 2 = 0

# Le compteur ne redescend jamais, mais le résultat fait 0, 1, 1, 0, 0, 1...
# Plus le pas est petit, plus l'image reste longtemps la même.


# ============================================================
# Le dessin du dragonneau (déjà écrit pour toi)
# ============================================================
# C = corps    D = corps foncé    A = aile    . = rien (transparent)
# O = oeil

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


def faire_sprite(motif):
    """Transforme un dessin en lettres en une vraie image de 16 x 12."""
    image = pygame.Surface((16, 12), pygame.SRCALPHA)
    couleurs = {"C": COULEUR_DRAGON, "D": COULEUR_AILE,
                "A": COULEUR_AILE, "O": COULEUR_OEIL}
    for ligne_y, ligne in enumerate(motif):
        for ligne_x, lettre in enumerate(ligne):
            if lettre in couleurs:
                image.set_at((ligne_x, ligne_y), couleurs[lettre])
    return image


# ============================================================
# Préparation (déjà écrite pour toi)
# ============================================================
pygame.init()
ecran = pygame.display.set_mode((LARGEUR * ZOOM, HAUTEUR * ZOOM))
pygame.display.set_caption("Le Dragonneau")
surf = pygame.Surface((LARGEUR, HAUTEUR))
horloge = pygame.time.Clock()

SPRITES = [faire_sprite(DRAGON_AILE_HAUTE),   # SPRITES[0] = aile en haut
           faire_sprite(DRAGON_AILE_BASSE)]   # SPRITES[1] = aile en bas

# Où est le dragonneau, à quelle vitesse il descend, où en sont ses ailes
y = 10.0
vy = 0.0
animation = 0.0

en_marche = True
while en_marche:

    # --- 1. ÉCOUTER ----------------------------------------
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_marche = False
        if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE:
            en_marche = False

    # (déjà écrit) La liste de TOUTES les touches, à cet instant précis.
    touches = pygame.key.get_pressed()

    # --- TON TOUR ---

    # TODO 1 : Range dans une variable si la barre d'ESPACE est tenue
    #          en ce moment.
    #          Dans la liste `touches`, la case de la barre d'espace
    #          s'appelle pygame.K_SPACE.
    #          Appelle ta variable `bouton` — la suite s'en sert.


    # --- 2. CALCULER ---------------------------------------

    # TODO 2 : Fais augmenter la vitesse de chute — mais pas du même cran
    #          selon que le bouton est tenu ou non.
    #          Bouton tenu : il plonge lourd. Bouton relâché : il plane.
    #          (les deux crans existent déjà en haut du fichier)


    # (déjà écrit) La position suit la vitesse, comme à la leçon 07.
    y += vy

    # (déjà écrit) Le sol est un trampoline : il ne s'arrête jamais tout
    # à fait, sinon on ne verrait plus l'effet du bouton.
    if y >= SOL_PLAT:
        y = SOL_PLAT
        vy = -vy * REBOND
        if vy > -REBOND_MINI:
            vy = -REBOND_MINI

    # (déjà écrit) Le haut du monde l'arrête net.
    if y < PLAFOND:
        y = PLAFOND
        vy = 0.0

    # TODO 3 : Fais avancer le compteur des ailes d'un cran,
    #          à chaque tour de boucle.
    #          (utilise VITESSE_AILES)


    # --- 3. DESSINER ---------------------------------------
    surf.fill(COULEUR_CIEL)
    pygame.draw.rect(surf, COULEUR_SOL, (0, SOL_PLAT, LARGEUR, HAUTEUR - SOL_PLAT))
    pygame.draw.rect(surf, COULEUR_OMBRE, (0, SOL_PLAT, LARGEUR, 3))

    # TODO 4 : Choisis laquelle des deux images de SPRITES il faut montrer
    #          à ce tour-ci, en te servant du compteur des ailes.
    #          Regarde l'EXEMPLE en haut du fichier.
    #          Appelle ta variable `image`.


    # TODO 5 : Colle cette image sur le dessin.
    #          Modèle : surf.blit(image, (gauche, haut))
    #          Attention : blit veut le coin EN HAUT À GAUCHE, pas le centre.
    #          L'image fait 16 de large et 12 de haut, et le dragonneau
    #          doit être centré sur (X_DRAGON, y).
    #          Écris aussi int(y) : un pixel, ça ne se coupe pas en deux
    #          — et la console de la leçon 14 refuse les virgules.


    # --- 4. AFFICHER (déjà écrit) --------------------------
    pygame.transform.scale(surf, ecran.get_size(), ecran)
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
