# ============================================================
# Leçon 10 — La caméra qui dézoome
# jeu.py — ton jeu, leçon après leçon
# ============================================================
# OBJECTIF : Tes vols montent à 234 pixels, l'écran en fait 120.
#            Quand tu voles haut, tu ne vois plus où tu vas retomber.
#            Aujourd'hui, la caméra RECULE quand tu montes.
#
#            Et un HUD : ta distance et ta vitesse, en haut de l'écran.
#
# NOUVEAU : ton jeu a maintenant DEUX fichiers. Les collines sont
#           parties dans terrain.py. Garde les deux dans le même dossier.
#
# COMMENT TESTER : Clique sur ▶
#            Puis regarde l'écran et coche la liste « Ça doit faire ça »
#            dans presentation.html.
#
# POUR FERMER : clique le ✕ de la fenêtre, ou appuie sur ÉCHAP
# ============================================================

import pygame

from terrain import hauteur_du_sol, CRETE

# --- Les réglages du jeu ---
LARGEUR, HAUTEUR = 160, 120      # la taille du monde, en pixels
ZOOM_FENETRE = 4                 # la loupe : la fenêtre fait 640 x 480
X_DRAGON = 40                    # le dragonneau reste dans cette colonne
MI_HAUTEUR = 6                   # la moitié du sprite : y est son CENTRE

# --- La chute et la glisse (leçon 09b) ---
GRAVITE = 0.08
GRAVITE_PLONGEON = 0.30
ACCEL_DESCENTE = 0.22
FREIN_MONTEE = 0.28
BONUS_PLONGEON = 2.6
MALUS_PLONGEON = 3.5
FRICTION = 0.997
VX_MIN, VX_MAX = 1.2, 9.0
VITESSE_AILES = 0.15

# --- La caméra qui recule (NOUVEAU) ---
ZOOM_MIN = 0.30                  # le plus loin qu'on puisse reculer
SEUIL_ZOOM = 50                  # sous cette altitude, on ne recule pas du tout
HAUTEUR_ZOOM = 190               # à cette altitude, on a reculé au maximum
SUIVI_SORTIE = 0.07              # vitesse pour s'éloigner
SUIVI_RETOUR = 0.10              # vitesse pour revenir
MARGE_SOL = 8                    # pixels de sol qu'on garde toujours à l'écran
VISEE_BAS = 60                   # sa place à l'écran quand il est au sol
VISEE_HAUT = 26                  # ... et quand il vole très haut
SUIVI_CAMERA = 0.10

COULEUR_CIEL   = (38, 28, 66)
COULEUR_SOL    = (58, 138, 68)
COULEUR_OMBRE  = (32, 92, 48)
COULEUR_DRAGON = (232, 92, 56)
COULEUR_AILE   = (168, 52, 40)
COULEUR_OEIL   = (20, 20, 28)
COULEUR_HUD    = (255, 255, 255)


# ============================================================
# --- EXEMPLE (ne pas modifier) ---
# ============================================================
# Une RAMPE : transformer « entre tant et tant » en « entre 0 et 1 ».
# C'est la recette de tous les effets progressifs d'un jeu.

depart, arrivee = 50, 190
mesure = 120

part = (mesure - depart) / (arrivee - depart)
# part vaut 0.5  →  on est à la moitié du chemin entre 50 et 190

# Et pour ne jamais dépasser 1, même si la mesure explose :
part = min(1.0, part)


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
ecran = pygame.display.set_mode((LARGEUR * ZOOM_FENETRE, HAUTEUR * ZOOM_FENETRE))
pygame.display.set_caption("Le Dragonneau")
surf = pygame.Surface((LARGEUR, HAUTEUR))
horloge = pygame.time.Clock()

POLICE = pygame.font.SysFont("consolas", 8)


def ecrire(surface, message, x, y, couleur=COULEUR_HUD):
    """Écrit un petit texte sur l'écran du jeu."""
    surface.blit(POLICE.render(message, False, couleur), (x, y))


SPRITES = [faire_sprite(DRAGON_AILE_HAUTE),   # SPRITES[0] = aile en haut
           faire_sprite(DRAGON_AILE_BASSE)]   # SPRITES[1] = aile en bas

camera_x = 0.0
y = hauteur_du_sol(0) - MI_HAUTEUR
vy = 0.0
vx = 2.0
animation = 0.0
au_sol_avant = True

zoom = 1.0                       # 1.0 = taille normale, 0.3 = très reculé
visee = VISEE_BAS                # à quelle hauteur de l'écran on le montre
camera_y = y - visee

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

    # --- 2. CALCULER (déjà écrit — c'est ta leçon 09b) -----
    if bouton:
        vy += GRAVITE_PLONGEON
    else:
        vy += GRAVITE

    y += vy

    hauteur_ici = hauteur_du_sol(camera_x)
    sol = hauteur_ici - MI_HAUTEUR

    if y >= sol:
        y = sol
        pente = hauteur_du_sol(camera_x + 1) - hauteur_ici

        if not au_sol_avant:
            vx = (vx + vy * pente) / (1 + pente * pente)
            vx = max(VX_MIN, min(VX_MAX, vx))

        vy = pente * vx

        if pente > 0:
            accel = ACCEL_DESCENTE * (BONUS_PLONGEON if bouton else 1.0)
        else:
            accel = FREIN_MONTEE * (MALUS_PLONGEON if bouton else 1.0)

        vx = max(VX_MIN, min(VX_MAX, (vx + pente * accel) * FRICTION))

    au_sol_avant = y >= sol
    camera_x += vx
    animation += VITESSE_AILES

    # --- 3. LA CAMÉRA --------------------------------------
    # --- TON TOUR ---

    # TODO 1 : Calcule à quelle hauteur il vole.
    #          On mesure au-dessus de la LIGNE DES CRÊTES (CRETE), pas
    #          au-dessus du sol qui passe dessous : les crêtes, elles,
    #          ne bougent jamais. Et jamais de nombre négatif quand il
    #          est plus bas qu'une crête — donc 0 minimum.
    #          Appelle ta variable `hauteur_de_vol`.
    #          (utilise max)


    # TODO 2 : Transforme cette hauteur en une PART entre 0.0 et 1.0.
    #          · tant qu'il vole sous SEUIL_ZOOM : la part vaut 0.0,
    #            la caméra ne bouge pas du tout
    #          · au-dessus : la part monte jusqu'à 1.0 quand il atteint
    #            HAUTEUR_ZOOM, et ne dépasse jamais 1.0
    #          Appelle ta variable `part`.
    #          (regarde l'EXEMPLE en haut du fichier)


    # TODO 3 : Déduis-en le zoom qu'on VOUDRAIT.
    #          part = 0.0 → zoom 1.0 (taille normale)
    #          part = 1.0 → zoom ZOOM_MIN (le plus reculé)
    #          et tout ce qu'il y a entre les deux, proportionnellement.
    #          Appelle ta variable `confort`.


    # (déjà écrit) On n'y va pas d'un coup : la caméra s'éloigne
    # doucement et revient un peu plus vite.
    if confort < zoom:
        zoom += (confort - zoom) * SUIVI_SORTIE
    else:
        zoom += (confort - zoom) * SUIVI_RETOUR

    # (déjà écrit) Plus il vole haut, plus on le montre haut dans
    # l'écran — pour laisser voir le sol en dessous.
    visee += (VISEE_BAS + (VISEE_HAUT - VISEE_BAS) * part - visee) * SUIVI_CAMERA

    # (déjà écrit) LE GARDE-FOU : le zoom le plus serré qui laisse
    # encore voir MARGE_SOL pixels de sol. Perdre le sol devient
    # impossible, quels que soient les réglages au-dessus.
    plafond = (HAUTEUR - MARGE_SOL - visee) / max(1.0, CRETE - y)
    zoom = max(0.12, min(1.0, plafond, zoom))

    # (déjà écrit) La caméra se DÉDUIT : le dragonneau tombe alors
    # pile à `visee` pixels du haut de l'écran.
    camera_y = y - visee / zoom

    # --- 4. DESSINER ---------------------------------------
    surf.fill(COULEUR_CIEL)

    # TODO 4 : Redessine les collines, mais avec le zoom.
    #          Deux changements par rapport à la leçon 09 :
    #            · pour savoir quel morceau du monde montre une colonne,
    #              il faut DIVISER son écart par le zoom
    #              (reculé = chaque colonne montre plus de monde) ;
    #            · la hauteur trouvée doit être MULTIPLIÉE par le zoom
    #              après avoir enlevé camera_y.
    #          Le reste ne change pas : une ligne verticale par colonne.


    # (déjà écrit) Le dragonneau rapetisse quand la caméra recule.
    image = SPRITES[int(animation) % 2]
    if zoom < 0.85:
        image = pygame.transform.scale(image, (max(5, int(16 * zoom)),
                                               max(4, int(12 * zoom))))
    ecran_y = int((y - camera_y) * zoom)
    surf.blit(image, (X_DRAGON - image.get_width() // 2,
                      ecran_y - image.get_height() // 2))

    # --- 5. LE HUD -----------------------------------------

    # TODO 5 : Affiche la distance parcourue, en haut à gauche.
    #          10 pixels du monde = 1 mètre. Écris un nombre ENTIER
    #          suivi de " m", par exemple "138 m", en (3, 2).
    #          Modèle : ecrire(surf, message, x, y)


    # (déjà écrit) La jauge de vitesse, en haut à droite.
    plein = int(24 * (vx - VX_MIN) / (VX_MAX - VX_MIN))
    pygame.draw.rect(surf, COULEUR_HUD, (LARGEUR - 29, 3, 26, 5), 1)
    if plein > 0:
        pygame.draw.rect(surf, COULEUR_DRAGON, (LARGEUR - 28, 4, plein, 3))

    # --- 6. AFFICHER (déjà écrit) --------------------------
    pygame.transform.scale(surf, ecran.get_size(), ecran)
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
