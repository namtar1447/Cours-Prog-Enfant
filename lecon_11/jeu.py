# ============================================================
# Leçon 11 — Les îles et la tombée de la nuit
# jeu.py — ton jeu, leçon après leçon
# ============================================================
# OBJECTIF : Donner une FIN à ton jeu. La nuit tombe, lentement
#            d'abord, puis de plus en plus vite d'île en île.
#            Quand il fait noir, la partie est terminée.
#
#            Pour la repousser : aller vite, et bien atterrir.
#
# TROIS FICHIERS maintenant : jeu.py, terrain.py et themes.py.
#            Ils doivent rester dans le même dossier.
#
# COMMENT TESTER : Clique sur ▶
#            Puis regarde l'écran et coche la liste « Ça doit faire ça »
#            dans presentation.html.
#
# POUR FERMER : clique le ✕ de la fenêtre, ou appuie sur ÉCHAP
#               (R pour recommencer une partie)
# ============================================================

import pygame

from terrain import hauteur_du_sol, numero_ile, CRETE, NIVEAU_EAU, LONGUEUR_ILE
from themes import DRAGONNEAU, melanger

# --- Les réglages du jeu ---
LARGEUR, HAUTEUR = 160, 120
ZOOM_FENETRE = 4
X_DRAGON = 40
MI_HAUTEUR = 6

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

# --- La caméra (leçon 10) ---
ZOOM_MIN = 0.30
SEUIL_ZOOM = 50
HAUTEUR_ZOOM = 190
SUIVI_SORTIE = 0.07
SUIVI_RETOUR = 0.10
MARGE_SOL = 8
VISEE_BAS = 60
VISEE_HAUT = 26
SUIVI_CAMERA = 0.10

# --- La nuit (NOUVEAU) ---
VITESSE_NUIT = 0.00015           # ce que la nuit gagne à chaque image
FACTEUR_ILE = 0.35               # ... et 35 % de plus par île franchie
BONUS_ATTERRISSAGE = 0.004       # le jour que rend un atterrissage gagnant
DEBUT_ETOILES = 0.6              # à partir de quelle nuit on voit les étoiles

THEME = DRAGONNEAU
COULEUR_DRAGON = (232, 92, 56)
COULEUR_AILE   = (168, 52, 40)
COULEUR_OEIL   = (20, 20, 28)
COULEUR_HUD    = (255, 255, 255)


# ============================================================
# --- EXEMPLE (ne pas modifier) ---
# ============================================================
# MÉLANGER deux nombres selon une part, c'est la recette de tous
# les fondus — couleurs, sons, lumière.

depart, arrivee = 10, 50

part = 0.0
# 10 + (50 - 10) * 0.0  →  10      (tout au départ)

part = 0.25
# 10 + (50 - 10) * 0.25 →  20      (un quart du chemin)

part = 1.0
# 10 + (50 - 10) * 1.0  →  50      (tout à l'arrivée)

# C'est exactement ce que fait melanger() dans themes.py,
# mais sur les trois nombres d'une couleur à la fois.


# ============================================================
# Le dessin du dragonneau (déjà écrit pour toi)
# ============================================================

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
    image = pygame.Surface((16, 12), pygame.SRCALPHA)
    couleurs = {"C": COULEUR_DRAGON, "D": COULEUR_AILE,
                "A": COULEUR_AILE, "O": COULEUR_OEIL}
    for ligne_y, ligne in enumerate(motif):
        for ligne_x, lettre in enumerate(ligne):
            if lettre in couleurs:
                image.set_at((ligne_x, ligne_y), couleurs[lettre])
    return image


# Les étoiles : toujours aux mêmes endroits, calculées une seule fois.
ETOILES = [((i * 6151) % LARGEUR, (i * 3119) % 60) for i in range(40)]


# ============================================================
# Préparation (déjà écrite pour toi)
# ============================================================
pygame.init()
ecran = pygame.display.set_mode((LARGEUR * ZOOM_FENETRE, HAUTEUR * ZOOM_FENETRE))
pygame.display.set_caption("Le Dragonneau")
surf = pygame.Surface((LARGEUR, HAUTEUR))
horloge = pygame.time.Clock()

POLICE = pygame.font.SysFont("consolas", 8)
GROSSE_POLICE = pygame.font.SysFont("consolas", 14, bold=True)


def ecrire(surface, message, x, y, couleur=COULEUR_HUD, police=POLICE):
    surface.blit(police.render(message, False, couleur), (x, y))


SPRITES = [faire_sprite(DRAGON_AILE_HAUTE), faire_sprite(DRAGON_AILE_BASSE)]


def nouvelle_partie():
    """Remet tout à zéro. Appelé au début, et quand on appuie sur R."""
    depart_y = hauteur_du_sol(0) - MI_HAUTEUR
    return {
        "camera_x": 0.0, "y": depart_y, "vy": 0.0, "vx": 2.0,
        "animation": 0.0, "au_sol_avant": True,
        "zoom": 1.0, "visee": float(VISEE_BAS), "camera_y": depart_y - VISEE_BAS,
        "heure": 0.0, "finie": False,
    }


jeu = nouvelle_partie()

en_marche = True
while en_marche:

    # --- 1. ÉCOUTER (déjà écrit) ---------------------------
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            en_marche = False
        if evenement.type == pygame.KEYDOWN:
            if evenement.key == pygame.K_ESCAPE:
                en_marche = False
            if evenement.key == pygame.K_r:
                jeu = nouvelle_partie()

    touches = pygame.key.get_pressed()
    bouton = touches[pygame.K_SPACE]

    # On sort les valeurs du dictionnaire pour écrire du code lisible.
    camera_x, y, vy, vx = jeu["camera_x"], jeu["y"], jeu["vy"], jeu["vx"]
    zoom, visee, heure = jeu["zoom"], jeu["visee"], jeu["heure"]

    if not jeu["finie"]:

        # --- 2. CALCULER (déjà écrit — leçon 09b) ----------
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

            if not jeu["au_sol_avant"]:
                avant = vx                       # sa vitesse juste avant le choc
                vx = (vx + vy * pente) / (1 + pente * pente)
                vx = max(VX_MIN, min(VX_MAX, vx))

                # --- TON TOUR ---

                # TODO 1 : Récompense les beaux atterrissages.
                #          Si sa vitesse a AUGMENTÉ pendant le choc
                #          (compare avec `avant`), rends-lui un peu de
                #          jour : enlève BONUS_ATTERRISSAGE fois ce qu'il
                #          vient de gagner, à `heure`.
                #          Et jamais en dessous de 0.0.
                #          (utilise max)


            vy = pente * vx

            if pente > 0:
                accel = ACCEL_DESCENTE * (BONUS_PLONGEON if bouton else 1.0)
            else:
                accel = FREIN_MONTEE * (MALUS_PLONGEON if bouton else 1.0)

            vx = max(VX_MIN, min(VX_MAX, (vx + pente * accel) * FRICTION))

        jeu["au_sol_avant"] = y >= sol
        camera_x += vx
        jeu["animation"] += VITESSE_AILES

        # --- 3. LA NUIT ------------------------------------

        # TODO 2 : Trouve sur quelle île il se trouve.
        #          terrain.py sait déjà le faire : numero_ile(x).
        #          Appelle ta variable `ile`.


        # TODO 3 : Fais avancer la nuit.
        #          À chaque image, `heure` gagne VITESSE_NUIT —
        #          mais FACTEUR_ILE de plus par île déjà franchie.
        #          Île 0 : vitesse normale.
        #          Île 1 : 1 + 0.35 fois plus vite. Île 2 : 1 + 0.70. …


        # TODO 4 : Termine la partie quand il fait complètement nuit.
        #          `heure` vaut 1.0 ou plus → range True dans
        #          jeu["finie"].


    # --- 4. LA CAMÉRA (déjà écrit — leçon 10) --------------
    hauteur_de_vol = max(0.0, CRETE - y)
    if hauteur_de_vol <= SEUIL_ZOOM:
        part = 0.0
    else:
        part = min(1.0, (hauteur_de_vol - SEUIL_ZOOM) / (HAUTEUR_ZOOM - SEUIL_ZOOM))

    confort = 1.0 - (1.0 - ZOOM_MIN) * part
    if confort < zoom:
        zoom += (confort - zoom) * SUIVI_SORTIE
    else:
        zoom += (confort - zoom) * SUIVI_RETOUR

    visee += (VISEE_BAS + (VISEE_HAUT - VISEE_BAS) * part - visee) * SUIVI_CAMERA
    plafond = (HAUTEUR - MARGE_SOL - visee) / max(1.0, CRETE - y)
    zoom = max(0.12, min(1.0, plafond, zoom))
    camera_y = y - visee / zoom

    # On range tout dans le dictionnaire avant de dessiner.
    jeu.update(camera_x=camera_x, y=y, vy=vy, vx=vx,
               zoom=zoom, visee=visee, camera_y=camera_y, heure=heure)

    # --- 5. DESSINER ---------------------------------------

    # TODO 5 : Fabrique les couleurs du moment.
    #          Pour chacune des quatre, mélange la version de jour et la
    #          version de nuit du THEME, selon `heure`.
    #          Modèle : melanger(THEME["ciel"], THEME["ciel_nuit"], heure)
    #          Appelle-les : couleur_ciel, couleur_sol, couleur_ombre,
    #          couleur_eau.
    #          (les clés de nuit sont : ciel_nuit, collines_nuit,
    #           ombre_nuit, eau_nuit)


    surf.fill(couleur_ciel)

    # (déjà écrit) Les étoiles, quand la nuit est bien avancée.
    if heure > DEBUT_ETOILES:
        force = (heure - DEBUT_ETOILES) / (1.0 - DEBUT_ETOILES)
        couleur_etoile = melanger(couleur_ciel, (255, 255, 255), force)
        for etoile_x, etoile_y in ETOILES:
            surf.set_at((etoile_x, etoile_y), couleur_etoile)

    # (déjà écrit) Le décor, colonne par colonne — leçon 10, plus l'eau.
    for colonne in range(LARGEUR):
        monde_x = camera_x + (colonne - X_DRAGON) / zoom
        hauteur = hauteur_du_sol(monde_x)
        sy = int((hauteur - camera_y) * zoom)
        if sy >= HAUTEUR:
            continue
        if hauteur >= NIVEAU_EAU - 0.5:
            pygame.draw.line(surf, couleur_eau, (colonne, sy), (colonne, HAUTEUR))
        else:
            pygame.draw.line(surf, couleur_sol, (colonne, sy), (colonne, HAUTEUR))
            pygame.draw.line(surf, couleur_ombre, (colonne, sy),
                             (colonne, sy + max(1, int(3 * zoom))))

    # (déjà écrit) Le dragonneau.
    image = SPRITES[int(jeu["animation"]) % 2]
    if zoom < 0.85:
        image = pygame.transform.scale(image, (max(5, int(16 * zoom)),
                                               max(4, int(12 * zoom))))
    ecran_y = int((y - camera_y) * zoom)
    surf.blit(image, (X_DRAGON - image.get_width() // 2,
                      ecran_y - image.get_height() // 2))

    # --- 6. LE HUD (déjà écrit) ----------------------------
    ecrire(surf, f"{int(camera_x / 10)} m", 3, 2)
    ecrire(surf, f"ile {numero_ile(camera_x) + 1}", 3, 11)

    plein = int(24 * (vx - VX_MIN) / (VX_MAX - VX_MIN))
    pygame.draw.rect(surf, COULEUR_HUD, (LARGEUR - 29, 3, 26, 5), 1)
    if plein > 0:
        pygame.draw.rect(surf, COULEUR_DRAGON, (LARGEUR - 28, 4, plein, 3))

    # la jauge de nuit : elle se remplit, et c'est le compte à rebours
    pygame.draw.rect(surf, COULEUR_HUD, (LARGEUR - 29, 11, 26, 5), 1)
    nuit_pleine = int(24 * min(1.0, heure))
    if nuit_pleine > 0:
        pygame.draw.rect(surf, (90, 90, 160), (LARGEUR - 28, 12, nuit_pleine, 3))

    if jeu["finie"]:
        ecrire(surf, "LA NUIT", 48, 40, (255, 255, 255), GROSSE_POLICE)
        ecrire(surf, "T'A RATTRAPE", 34, 56, (255, 255, 255), GROSSE_POLICE)
        ecrire(surf, f"{int(camera_x / 10)} m  -  R pour rejouer", 26, 78)

    # --- 7. AFFICHER (déjà écrit) --------------------------
    pygame.transform.scale(surf, ecran.get_size(), ecran)
    pygame.display.flip()
    horloge.tick(60)

pygame.quit()
