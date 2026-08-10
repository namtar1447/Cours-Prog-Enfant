# ============================================================
# Leçon 07 — Le Dragonneau prend vie
# jeu.py — ton jeu, leçon après leçon
# ============================================================
# OBJECTIF : Faire tomber le dragonneau et le faire rebondir sur le sol.
#            C'est le tout début de ton jeu : tu vas garder ce fichier
#            et l'agrandir jusqu'à la leçon 13.
#
# COMMENT TESTER : Clique sur ▶
#            Puis regarde l'écran et coche la liste « Ça doit faire ça »
#            dans presentation.html. Dans un jeu, c'est l'œil qui teste.
#
# POUR FERMER : clique le ✕ de la fenêtre, ou appuie sur ÉCHAP
# ============================================================

import pygame

# --- Les réglages du jeu (tu peux y toucher à la fin) ---
LARGEUR, HAUTEUR = 160, 120      # la taille du monde, en pixels
ZOOM = 4                         # la loupe : la fenêtre fait 640 x 480
X_DRAGON = 40                    # le dragonneau reste dans cette colonne
SOL_PLAT = 100                   # la hauteur du sol
GRAVITE = 0.14                   # combien la vitesse augmente à chaque tour
REBOND = 0.6                     # ce qu'il reste de vitesse après un rebond

COULEUR_CIEL   = (38, 28, 66)
COULEUR_SOL    = (58, 138, 68)
COULEUR_OMBRE  = (32, 92, 48)
COULEUR_DRAGON = (232, 92, 56)


# ============================================================
# --- EXEMPLE (ne pas modifier) ---
# ============================================================
# Voici comment une valeur peut en faire bouger une autre.
# Une bille roule : sa vitesse s'ajoute à sa position, encore et encore.

position_bille = 0
vitesse_bille = 3

position_bille += vitesse_bille      # position vaut maintenant 3
position_bille += vitesse_bille      # position vaut maintenant 6
position_bille += vitesse_bille      # position vaut maintenant 9

# Dans ton jeu, ce sera pareil — sauf que la vitesse va CHANGER.


# ============================================================
# Préparation (déjà écrite pour toi)
# ============================================================
pygame.init()
ecran = pygame.display.set_mode((LARGEUR * ZOOM, HAUTEUR * ZOOM))
pygame.display.set_caption("Le Dragonneau")
surf = pygame.Surface((LARGEUR, HAUTEUR))
horloge = pygame.time.Clock()

# Où est le dragonneau, et à quelle vitesse il descend
y = 10.0
vy = 0.0

en_marche = True
while en_marche:

    # --- 1. ÉCOUTER (déjà écrit) ---------------------------
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_marche = False
        if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE:
            en_marche = False

    # --- 2. CALCULER ---------------------------------------
    # --- TON TOUR ---

    # TODO 1 : Fais augmenter la vitesse de chute d'un cran.
    #          À chaque tour de boucle, le dragonneau doit tomber
    #          un peu plus vite que le tour d'avant.
    #          (utilise la variable GRAVITE)


    # TODO 2 : Fais descendre le dragonneau selon sa vitesse.
    #          Attention : c'est la position qui bouge ici, pas la vitesse.


    # TODO 3 : Empêche-le de traverser le sol.
    #          Quand il est arrivé au sol ou plus bas, repose-le
    #          exactement sur le sol.
    #          (une seule ligne suffit pour l'instant — le rebond arrive après)


    # TODO 4 : Ajoute le rebond, juste en dessous du TODO 3.
    #          Une fois posé sur le sol, il doit repartir vers le HAUT,
    #          mais moins vite qu'il n'est arrivé.
    #          (utilise la variable REBOND — et souviens-toi de ce que
    #           fait un signe moins sur une vitesse)


    # (déjà écrit) Quand les rebonds deviennent minuscules, on l'arrête net.
    # Sans ça, il tremblote sur place pour toujours.
    if y >= SOL_PLAT and -0.4 < vy < 0:
        vy = 0.0

    # --- 3. DESSINER ---------------------------------------
    surf.fill(COULEUR_CIEL)
    pygame.draw.rect(surf, COULEUR_SOL, (0, SOL_PLAT, LARGEUR, HAUTEUR - SOL_PLAT))
    pygame.draw.rect(surf, COULEUR_OMBRE, (0, SOL_PLAT, LARGEUR, 3))

    # TODO 5 : Dessine le dragonneau.
    #          Pour l'instant c'est un simple rond de 6 pixels de rayon,
    #          de la couleur COULEUR_DRAGON, dans la colonne X_DRAGON,
    #          à la hauteur où il se trouve.
    #          Modèle : pygame.draw.circle(surf, couleur, (x, y), rayon)
    #          Attention : pygame veut des nombres entiers pour la position.


    # --- 4. AFFICHER (déjà écrit) --------------------------
    pygame.transform.scale(surf, ecran.get_size(), ecran)
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
