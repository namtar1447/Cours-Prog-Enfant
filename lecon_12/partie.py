# ============================================================
# Leçon 12 — partie.py
# ============================================================
# TON JEU DES LEÇONS 07 À 11, rangé dans des fonctions.
#
#   nouvelle_partie()                  une partie toute neuve
#   avancer(jeu, bouton, gravite)      une image de jeu : la chute, la
#                                      glisse, l'atterrissage, la nuit,
#                                      la caméra
#   dessiner_partie(surf, jeu, theme)  le ciel, les collines, le
#                                      dragonneau et le HUD
#   distance(jeu)                      combien de mètres parcourus
#
# C'est le code que tu as écrit et complété leçon après leçon. Il est
# seulement RANGÉ dans des fonctions, comme à la leçon 04 — pour que
# jeu.py reste court, et qu'on y voie ce qui est nouveau.
#
# Tu n'as rien à modifier ici.
# ============================================================

import random

import pygame

from terrain import hauteur_du_sol, numero_ile, est_eau, CRETE, NIVEAU_EAU
from themes import melanger

# --- L'écran ---
LARGEUR, HAUTEUR = 160, 120
X_DRAGON = 40
MI_HAUTEUR = 6

# --- La chute et la glisse (leçon 09b) ---
# La gravité quand on plane n'est plus ici : c'est le THÈME qui la donne.
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
ZOOM_PLANCHER = 0.06             # le plus loin possible, pour les vols très hauts
SEUIL_ZOOM = 50
HAUTEUR_ZOOM = 190
SUIVI_SORTIE = 0.07
SUIVI_RETOUR = 0.10
MARGE_SOL = 8
VISEE_BAS = 60
VISEE_HAUT = 26
SUIVI_CAMERA = 0.10

# --- La nuit (leçon 11) ---
VITESSE_NUIT = 0.00015
FACTEUR_ILE = 0.35
BONUS_ATTERRISSAGE = 0.004
DEBUT_ETOILES = 0.6

NIVEAUX_NUIT = 8                 # en combien d'étapes le dragonneau s'assombrit
COULEUR_HUD    = (255, 255, 255)
COULEUR_PLAQUE = (14, 14, 24)    # derrière le texte, pour qu'il reste lisible
COULEUR_SOLEIL = (255, 214, 102)


# ============================================================
# Le dessin du dragonneau
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


def faire_sprite(motif, theme, part_de_nuit):
    """Dessine le dragonneau aux couleurs du thème, avec un contour d'un pixel."""
    couleurs = {
        "C": melanger(theme["heros"], theme["heros_nuit"], part_de_nuit),
        "D": melanger(theme["aile"], theme["aile_nuit"], part_de_nuit),
        "A": melanger(theme["aile"], theme["aile_nuit"], part_de_nuit),
        "O": melanger(theme["contour"], theme["contour_nuit"], part_de_nuit),
    }
    contour = melanger(theme["contour"], theme["contour_nuit"], part_de_nuit)

    image = pygame.Surface((18, 14), pygame.SRCALPHA)

    for ligne_y, ligne in enumerate(motif):
        for ligne_x, lettre in enumerate(ligne):
            if lettre not in couleurs:
                continue
            for decale_y in (-1, 0, 1):
                for decale_x in (-1, 0, 1):
                    image.set_at((ligne_x + 1 + decale_x, ligne_y + 1 + decale_y), contour)

    for ligne_y, ligne in enumerate(motif):
        for ligne_x, lettre in enumerate(ligne):
            if lettre in couleurs:
                image.set_at((ligne_x + 1, ligne_y + 1), couleurs[lettre])

    return image


# Les sprites de chaque thème, préparés UNE fois, la première fois qu'on
# en a besoin (dans plusieurs clartés : on ne redessine pas 200 pixels à
# chaque image).
_SPRITES = {}


def sprites_du_theme(theme):
    if theme["nom"] not in _SPRITES:
        _SPRITES[theme["nom"]] = [
            [faire_sprite(motif, theme, niveau / (NIVEAUX_NUIT - 1))
             for motif in (DRAGON_AILE_HAUTE, DRAGON_AILE_BASSE)]
            for niveau in range(NIVEAUX_NUIT)]
    return _SPRITES[theme["nom"]]


# Les étoiles : tirées au hasard une fois, toujours les mêmes.
_hasard = random.Random(7)
ETOILES = [(_hasard.randrange(LARGEUR), _hasard.randrange(74),
            _hasard.uniform(0.35, 1.0)) for _ in range(44)]


# ============================================================
# Le texte du HUD
# ============================================================
_POLICES = {}


def police(taille=8, gras=False):
    """Les polices sont créées la première fois qu'on en a besoin."""
    if (taille, gras) not in _POLICES:
        _POLICES[(taille, gras)] = pygame.font.SysFont("consolas", taille, bold=gras)
    return _POLICES[(taille, gras)]


def ecrire(surface, message, x, y, couleur=COULEUR_HUD, taille=8, gras=False):
    """Le texte, avec son ombre : lisible sur un ciel clair comme sur la nuit."""
    p = police(taille, gras)
    surface.blit(p.render(message, False, COULEUR_PLAQUE), (x + 1, y + 1))
    surface.blit(p.render(message, False, couleur), (x, y))


def ecrire_centre(surface, message, y, couleur=COULEUR_HUD, taille=8, gras=False):
    """Pareil, mais centré dans l'écran."""
    largeur = police(taille, gras).size(message)[0]
    ecrire(surface, message, (LARGEUR - largeur) // 2, y, couleur, taille, gras)


# ============================================================
# Une partie
# ============================================================

def nouvelle_partie():
    """Une partie toute neuve : tout est rangé dans un dictionnaire."""
    depart_y = hauteur_du_sol(0) - MI_HAUTEUR
    return {
        "camera_x": 0.0, "y": depart_y, "vy": 0.0, "vx": 2.0,
        "animation": 0.0, "au_sol_avant": True,
        "zoom": 1.0, "visee": float(VISEE_BAS), "camera_y": depart_y - VISEE_BAS,
        "heure": 0.0, "soleil": 0, "attente": 0,
    }


def distance(jeu):
    """La distance parcourue, en mètres (10 pixels = 1 mètre)."""
    return int(jeu["camera_x"] / 10)


def avancer(jeu, bouton, gravite):
    """Une image de jeu. `gravite` : celle du thème, quand on plane."""
    camera_x, y, vy, vx = jeu["camera_x"], jeu["y"], jeu["vy"], jeu["vx"]
    zoom, visee, heure = jeu["zoom"], jeu["visee"], jeu["heure"]

    # --- La chute (leçon 07 et 08) ---
    if bouton:
        vy += GRAVITE_PLONGEON
    else:
        vy += gravite

    y += vy

    # --- La glisse et l'atterrissage (leçon 09b) ---
    hauteur_ici = hauteur_du_sol(camera_x)
    sol = hauteur_ici - MI_HAUTEUR

    if y >= sol:
        y = sol
        pente = hauteur_du_sol(camera_x + 1) - hauteur_ici

        if not jeu["au_sol_avant"]:
            avant = vx
            vx = (vx + vy * pente) / (1 + pente * pente)
            vx = max(VX_MIN, min(VX_MAX, vx))

            # Un bel atterrissage rend un peu de jour (leçon 11)
            gain = vx - avant
            if gain > 0:
                heure -= gain * BONUS_ATTERRISSAGE
                jeu["soleil"] = 45
            if heure < 0.0:
                heure = 0.0

        vy = pente * vx

        if pente > 0:
            accel = ACCEL_DESCENTE * (BONUS_PLONGEON if bouton else 1.0)
        else:
            accel = FREIN_MONTEE * (MALUS_PLONGEON if bouton else 1.0)

        vx = max(VX_MIN, min(VX_MAX, (vx + pente * accel) * FRICTION))

    jeu["au_sol_avant"] = y >= sol
    camera_x += vx
    jeu["animation"] += VITESSE_AILES

    # --- La nuit (leçon 11) ---
    ile = numero_ile(camera_x)
    fois_plus_vite = 1 + FACTEUR_ILE * ile
    heure += VITESSE_NUIT * fois_plus_vite

    if jeu["soleil"] > 0:
        jeu["soleil"] -= 1

    # --- La caméra (leçon 10) ---
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

    reference = NIVEAU_EAU if est_eau(camera_x) else CRETE
    plafond = (HAUTEUR - MARGE_SOL - visee) / max(1.0, reference - y)
    zoom = max(ZOOM_PLANCHER, min(1.0, plafond, zoom))
    camera_y = y - visee / zoom

    jeu.update(camera_x=camera_x, y=y, vy=vy, vx=vx,
               zoom=zoom, visee=visee, camera_y=camera_y, heure=heure)


def dessiner_partie(surf, jeu, theme, hud=True):
    """Le paysage, le dragonneau et (si hud=True) le HUD, aux couleurs du thème."""
    camera_x, camera_y, y = jeu["camera_x"], jeu["camera_y"], jeu["y"]
    zoom, vx = jeu["zoom"], jeu["vx"]

    # La part de nuit ne dépasse jamais 1.0, même si la partie continue
    # après la nuit noire : sinon les couleurs sortiraient de 0–255.
    nuit = min(1.0, jeu["heure"])

    couleur_ciel  = melanger(theme["ciel"], theme["ciel_nuit"], nuit)
    couleur_sol   = melanger(theme["collines"], theme["collines_nuit"], nuit)
    couleur_ombre = melanger(theme["ombre"], theme["ombre_nuit"], nuit)
    couleur_eau   = melanger(theme["eau"], theme["eau_nuit"], nuit)

    surf.fill(couleur_ciel)

    if nuit > DEBUT_ETOILES:
        force = (nuit - DEBUT_ETOILES) / (1.0 - DEBUT_ETOILES)
        for etoile_x, etoile_y, eclat in ETOILES:
            surf.set_at((etoile_x, etoile_y),
                        melanger(couleur_ciel, (255, 255, 255), force * eclat))

    for colonne in range(LARGEUR):
        monde_x = camera_x + (colonne - X_DRAGON) / zoom
        sy = int((hauteur_du_sol(monde_x) - camera_y) * zoom)
        if sy >= HAUTEUR:
            continue
        if est_eau(monde_x):
            pygame.draw.line(surf, couleur_eau, (colonne, sy), (colonne, HAUTEUR))
        else:
            pygame.draw.line(surf, couleur_sol, (colonne, sy), (colonne, HAUTEUR))
            pygame.draw.line(surf, couleur_ombre, (colonne, sy),
                             (colonne, sy + max(1, int(3 * zoom))))

    niveau = min(NIVEAUX_NUIT - 1, int(nuit * NIVEAUX_NUIT))
    image = sprites_du_theme(theme)[niveau][int(jeu["animation"]) % 2]
    if zoom < 0.85:
        image = pygame.transform.scale(image, (max(6, int(18 * zoom)),
                                               max(5, int(14 * zoom))))
    ecran_y = int((y - camera_y) * zoom)
    surf.blit(image, (X_DRAGON - image.get_width() // 2,
                      ecran_y - image.get_height() // 2))

    if not hud:
        return

    # --- Le HUD ---
    ecrire(surf, f"{distance(jeu)} m", 3, 2)
    ecrire(surf, f"ile {numero_ile(camera_x) + 1}", 3, 11)
    if jeu["soleil"] > 0:
        ecrire(surf, "+ jour !", 3, 20, COULEUR_SOLEIL)

    pygame.draw.rect(surf, COULEUR_PLAQUE, (LARGEUR - 30, 2, 28, 15))

    plein = int(24 * (vx - VX_MIN) / (VX_MAX - VX_MIN))
    pygame.draw.rect(surf, COULEUR_HUD, (LARGEUR - 29, 3, 26, 5), 1)
    if plein > 0:
        pygame.draw.rect(surf, theme["heros"], (LARGEUR - 28, 4, plein, 3))

    pygame.draw.rect(surf, COULEUR_HUD, (LARGEUR - 29, 11, 26, 5), 1)
    nuit_pleine = int(24 * nuit)
    if nuit_pleine > 0:
        pygame.draw.rect(surf, (120, 124, 196), (LARGEUR - 28, 12, nuit_pleine, 3))
