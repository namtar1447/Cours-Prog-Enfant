# ============================================================
# Leçon 09 — Le terrain-tremplin
# jeu.py — ton jeu, leçon après leçon
# ============================================================
# OBJECTIF : Faire disparaître le sol plat. À la place : de vraies
#            collines, calculées par une formule, qui défilent sous
#            le dragonneau.
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

# --- Le mouvement ---
VITESSE = 1.5                    # de combien le monde avance à chaque tour
GRAVITE = 0.14                   # chute normale, ailes ouvertes
GRAVITE_PLONGEON = 0.40          # chute quand ESPACE est tenu
REBOND = 0.6                     # ce qu'il reste de vitesse après un rebond
REBOND_MINI = 2.4                # le plus petit rebond possible
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
# Deux opérations qui découpent un nombre en « quel morceau » et
# « où dans le morceau ». C'est tout ce qu'il faut pour des collines
# qui se répètent sans fin.

longueur = 10

print(23 // longueur)     # affiche 2   → on est dans le 3e morceau (0, 1, 2)
print(23 %  longueur)     # affiche 3   → et à 3 pas de son début

# En divisant ce reste par la longueur, on obtient un nombre entre
# 0.0 (tout au début du morceau) et 1.0 (tout à la fin).

print(23 % longueur / longueur)      # affiche 0.3


# ============================================================
# LES COLLINES
# ============================================================
# hauteur_du_sol(x) répond à UNE question : « à la position x du
# monde, le sol est à quelle hauteur ? »
#
#   x = 0        le tout début du monde
#   x = 350      350 pixels plus loin, quelque part dans la 2e colline
#
# Le dragonneau ne bouge jamais horizontalement : c'est le monde qui
# défile. On demandera donc cette hauteur 160 fois par image — une
# fois par colonne de l'écran.

def hauteur_du_sol(x):

    # TODO 1 : Trouve le NUMÉRO de la colline où se trouve x.
    #          Les collines font toutes L_COLLINE de long et se suivent :
    #          0 à 199 → colline 0, 200 à 399 → colline 1, et ainsi de suite.
    #          Appelle ta variable `i`, et garde un nombre entier.


    # TODO 2 : Trouve OÙ ON EN EST dans cette colline, entre 0.0 et 1.0.
    #          0.0 = tout au début de la colline, 1.0 = tout à la fin.
    #          Appelle ta variable `t`.
    #          (regarde l'EXEMPLE en haut du fichier)


    # (déjà écrit) Le creux de CETTE colline. Le calcul a l'air bizarre,
    # mais il donne toujours le même résultat pour la même colline :
    # ce sont des dés qui tombent toujours pareil.
    creux = D_MIN + (D_MAX - D_MIN) * ((i * 7919) % 1000) / 1000

    # (déjà écrit) La descente : longue, douce, en cosinus.
    if t < R_DESCENTE:
        u = t / R_DESCENTE
        return CRETE + creux * (1 - math.cos(math.pi * u)) / 2

    # (déjà écrit) La remontée « en goutte » : le sommet est arrondi,
    # mais ça tourne le plus fort JUSTE AVANT le sommet. C'est ce
    # détail qui fera décoller le dragonneau à la leçon 09b.
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

# Le dragonneau : sa hauteur, sa vitesse de chute, ses ailes
y = 10.0
vy = 0.0
animation = 0.0

# La caméra : où elle regarde dans le monde
camera_x = 0.0
camera_y = 0.0

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

    # (déjà écrit) La gravité et la chute, comme à la leçon 08.
    if bouton:
        vy += GRAVITE_PLONGEON
    else:
        vy += GRAVITE

    y += vy

    # --- TON TOUR ---

    # TODO 3 : Fais avancer le monde.
    #          Le dragonneau reste dans sa colonne : c'est la caméra
    #          qui doit avancer, de VITESSE, à chaque tour de boucle.


    # (déjà écrit) Le sol n'est plus plat : sa hauteur dépend d'où on
    # est dans le monde. Le rebond, lui, ne change pas.
    sol = hauteur_du_sol(camera_x) - MI_HAUTEUR   # y est son CENTRE

    if y >= sol:
        y = sol
        vy = -vy * REBOND
        if vy > -REBOND_MINI:
            vy = -REBOND_MINI

    # TODO 4 : Fais suivre la caméra, en hauteur.
    #          On veut voir le dragonneau à VISEE pixels du haut de
    #          l'écran : la caméra devrait donc être à `y - VISEE`.
    #          Mais si elle y va d'un coup, tout l'écran saute à chaque
    #          rebond. Alors elle ne parcourt qu'une PART du chemin qui
    #          lui reste, à chaque tour : la part SUIVI.
    #          Modèle : camera_y += (cible - camera_y) * SUIVI


    # (déjà écrit) Les ailes battent, comme à la leçon 08.
    animation += VITESSE_AILES

    # --- 3. DESSINER ---------------------------------------
    surf.fill(COULEUR_CIEL)

    # TODO 5 : Dessine les collines, colonne par colonne.
    #          Pour CHAQUE colonne de l'écran, de 0 à LARGEUR - 1 :
    #            · trouve à quel endroit du MONDE elle correspond —
    #              la colonne X_DRAGON montre camera_x, celle d'à côté
    #              montre un pixel plus loin, et ainsi de suite ;
    #            · demande la hauteur du sol là-bas, et enlève camera_y
    #              pour passer du monde à l'écran ;
    #            · trace une ligne verticale de cette hauteur jusqu'en
    #              bas de l'écran.
    #          Modèle : pygame.draw.line(surf, couleur, (x, y1), (x, y2))
    #          pygame veut des entiers pour la hauteur : int(...)


    # (déjà écrit) Le dragonneau, comme à la leçon 08 — mais sa hauteur
    # à l'écran dépend maintenant de la caméra.
    image = SPRITES[int(animation) % 2]
    surf.blit(image, (X_DRAGON - 8, int(y - camera_y) - 6))

    # --- 4. AFFICHER (déjà écrit) --------------------------
    pygame.transform.scale(surf, ecran.get_size(), ecran)
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
