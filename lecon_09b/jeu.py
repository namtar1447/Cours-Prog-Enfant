# ============================================================
# Leçon 09b — Glisser, décoller, atterrir
# jeu.py — ton jeu, leçon après leçon
# ============================================================
# OBJECTIF : Le rebond disparaît. Le dragonneau SUIT la pente :
#            il prend de la vitesse en descendant, décolle au sommet
#            des bosses, et son atterrissage décide de la suite.
#
#            C'est la leçon où ton jeu devient un vrai jeu.
#
# COMMENT TESTER : Clique sur ▶
#            Puis regarde l'écran et coche la liste « Ça doit faire ça »
#            dans presentation.html.
#
# POUR FERMER : clique le ✕ de la fenêtre, ou appuie sur ÉCHAP
# ============================================================

import math
import pygame

# --- Les réglages du jeu (tu peux y toucher à la fin) ---
LARGEUR, HAUTEUR = 160, 120      # la taille du monde, en pixels
ZOOM = 4                         # la loupe : la fenêtre fait 640 x 480
X_DRAGON = 40                    # le dragonneau reste dans cette colonne
MI_HAUTEUR = 6                   # la moitié du sprite : y est son CENTRE

# --- Les collines ---
L_COLLINE = 200                  # longueur d'une colline, en pixels
CRETE = 46                       # hauteur du sommet (toujours la même)
D_MIN, D_MAX = 30, 65            # le creux le moins et le plus profond
R_DESCENTE = 0.62                # part de la colline occupée par la descente
POINTE = 2.2                     # netteté du sommet

# --- La chute ---
GRAVITE = 0.08                   # chute en planant (plus légère qu'avant)
GRAVITE_PLONGEON = 0.30          # chute quand ESPACE est tenu

# --- La glisse (tout le jeu est là) ---
ACCEL_DESCENTE = 0.22            # ce qu'une descente donne comme vitesse
FREIN_MONTEE = 0.28              # ce qu'une montée coûte (plus que la descente !)
BONUS_PLONGEON = 2.6             # x l'accélération si ESPACE est tenu EN DESCENTE
MALUS_PLONGEON = 3.5             # x le freinage      si ESPACE est tenu EN MONTÉE
FRICTION = 0.997                 # il perd un tout petit peu de vitesse sans arrêt
VX_MIN, VX_MAX = 1.2, 9.0        # jamais plus lent que ça, jamais plus rapide

VITESSE_AILES = 0.15             # combien le compteur d'ailes avance par tour

# --- La caméra ---
VISEE = 60                       # à quelle hauteur de l'écran on veut le voir
SUIVI = 0.12                     # à quelle vitesse la caméra le rattrape

COULEUR_CIEL   = (38, 28, 66)
COULEUR_SOL    = (58, 138, 68)
COULEUR_DRAGON = (232, 92, 56)
COULEUR_AILE   = (168, 52, 40)
COULEUR_OEIL   = (20, 20, 28)


# ============================================================
# --- EXEMPLE (ne pas modifier) ---
# ============================================================
# Une PENTE, c'est une différence de hauteur sur un pas de 1 pixel.
# Rien de plus. Rappel : y grandit vers le BAS.

hauteur_ici_exemple = 100
hauteur_un_pas_plus_loin = 101.5

pente_exemple = hauteur_un_pas_plus_loin - hauteur_ici_exemple
# pente_exemple vaut 1.5  ->  POSITIF  ->  le sol DESCEND
# si c'était -1.5         ->  NÉGATIF  ->  le sol MONTE
# si c'était 0            ->  c'est plat


# ============================================================
# LES COLLINES (déjà écrit — c'est ta leçon 09)
# ============================================================

def hauteur_du_sol(x):
    i = int(x // L_COLLINE)
    t = x % L_COLLINE / L_COLLINE

    creux = D_MIN + (D_MAX - D_MIN) * ((i * 7919) % 1000) / 1000

    if t < R_DESCENTE:
        u = t / R_DESCENTE
        return CRETE + creux * (1 - math.cos(math.pi * u)) / 2

    u = (t - R_DESCENTE) / (1 - R_DESCENTE)
    return CRETE + creux * math.cos(math.pi * u / 2) ** POINTE


# ============================================================
# Le dessin du dragonneau (déjà écrit pour toi)
# ============================================================
# C = corps    D = corps foncé    A = aile    O = oeil    . = rien

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

# Le dragonneau démarre posé sur la première colline.
camera_x = 0.0
y = hauteur_du_sol(0) - MI_HAUTEUR
vy = 0.0
vx = 2.0                         # NOUVEAU : sa vitesse horizontale change
animation = 0.0

camera_y = y - VISEE
au_sol_avant = True              # était-il au sol au tour d'avant ?

en_marche = True
while en_marche:

    # --- 1. ÉCOUTER (déjà écrit) ---------------------------
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_marche = False
        if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE:
            en_marche = False

    touches = pygame.key.get_pressed()
    bouton = touches[pygame.K_SPACE]

    # --- 2. CALCULER ---------------------------------------

    # (déjà écrit) La chute, comme avant.
    if bouton:
        vy += GRAVITE_PLONGEON
    else:
        vy += GRAVITE

    y += vy

    # (déjà écrit) Le sol sous lui, et la hauteur où il se pose.
    hauteur_ici = hauteur_du_sol(camera_x)
    sol = hauteur_ici - MI_HAUTEUR

    if y >= sol:
        y = sol

        # --- TON TOUR ---

        # TODO 1 : Calcule la pente du sol, ici.
        #          C'est la hauteur du sol UN PIXEL PLUS LOIN, moins la
        #          hauteur du sol ici (tu l'as déjà : hauteur_ici).
        #          Appelle ta variable `pente`.
        #          (regarde l'EXEMPLE en haut du fichier)


        if not au_sol_avant:
            # Il vient tout juste de retomber : c'est un ATTERRISSAGE.

            # TODO 2 : La formule la plus importante du jeu.
            #          Quand il touche le sol, seule la part de sa vitesse
            #          qui va DANS LE SENS DU SOL continue. Le reste part
            #          dans le choc.
            #          Écris :  vx = (vx + vy * pente) / (1 + pente * pente)
            #          Retomber bien aligné sur une descente le RELANCE ;
            #          s'écraser dans une côte lui casse tout.


            # (déjà écrit) Jamais plus lent que VX_MIN, jamais plus vite
            # que VX_MAX — sinon un très bel atterrissage l'enverrait
            # à des vitesses impossibles à jouer.
            vx = max(VX_MIN, min(VX_MAX, vx))

        # TODO 3 : Fais-le SUIVRE la pente.
        #          Il ne rebondit plus : il glisse. Sa vitesse de descente
        #          devient simplement sa vitesse horizontale multipliée
        #          par la pente.


        # TODO 4 : Le bouton agit AUSSI au sol — c'est là qu'est le jeu.
        #          Range dans `accel` de combien la pente change sa vitesse :
        #            · en DESCENTE (pente > 0) → ACCEL_DESCENTE,
        #              et BONUS_PLONGEON fois plus si le bouton est tenu
        #            · en MONTÉE (sinon)       → FREIN_MONTEE,
        #              et MALUS_PLONGEON fois plus si le bouton est tenu


        # (déjà écrit) On applique, sans jamais sortir des bornes.
        vx = max(VX_MIN, min(VX_MAX, (vx + pente * accel) * FRICTION))

    # (déjà écrit) On retient s'il était au sol, pour reconnaître le
    # prochain atterrissage.
    au_sol_avant = y >= sol

    # TODO 5 : Fais avancer le monde.
    #          Ce n'est plus une vitesse fixe comme à la leçon 09 :
    #          c'est SA vitesse à lui, vx.


    # (déjà écrit) La caméra rattrape, comme à la leçon 09.
    camera_y += (y - VISEE - camera_y) * SUIVI

    # (déjà écrit) Les ailes battent.
    animation += VITESSE_AILES

    # --- 3. DESSINER (déjà écrit — c'est ta leçon 09) ------
    surf.fill(COULEUR_CIEL)

    for colonne in range(LARGEUR):
        monde_x = camera_x + colonne - X_DRAGON
        sy = int(hauteur_du_sol(monde_x) - camera_y)
        pygame.draw.line(surf, COULEUR_SOL, (colonne, sy), (colonne, HAUTEUR))

    image = SPRITES[int(animation) % 2]
    surf.blit(image, (X_DRAGON - 8, int(y - camera_y) - MI_HAUTEUR))

    # --- 4. AFFICHER (déjà écrit) --------------------------
    pygame.transform.scale(surf, ecran.get_size(), ecran)
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
