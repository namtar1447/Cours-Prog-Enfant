# ============================================================
# Leçon 12 — terrain.py
# ============================================================
# Le terrain à îles de la leçon 11, RÉGLÉ après comparaison avec Tiny Wings :
# des îles un peu plus longues, et des collines qui se creusent moins
# d'une île à l'autre (avant, elles devenaient des ravins).
#
# Pour rappel, il sait deux choses de plus que celui de la leçon 10 :
#
#   · le monde est découpé en ÎLES
#   · chaque île est un peu plus dure que la précédente
#     (collines plus courtes, creux plus profonds)
#
# Une île se lit de gauche à droite :
#
#   plage      collines ordinaires      grande descente   tremplin   OCÉAN
#   ~~~~/‾‾\__/‾‾\__/‾‾\__/‾‾\__/‾‾\__ \_/‾\_/‾\_/‾\_ ___ / ‾‾‾‾‾~~~~~~~~~~~
#   on sort    le jeu normal            ça descend, les   petite    le grand
#   de l'eau                            bosses s'effacent remontée  saut
#
# Tu n'as rien à modifier ici.
# ============================================================

import math

CRETE = 46                       # hauteur du sommet des collines
R_DESCENTE = 0.62                # part de la colline occupée par la descente
POINTE = 2.2                     # netteté du sommet

NIVEAU_EAU = 108                 # la hauteur de la mer

LONGUEUR_ILE = 5600              # une île fait 5 600 px, soit 560 m
PLAGE = 400                      # la plage par laquelle on arrive sur l'île
OCEAN = 500                      # la mer à franchir au bout
L_REMONTEE = 60                  # la petite remontée qui sert de tremplin
H_REMONTEE = 26                  # de combien elle remonte
FALAISE = 14                     # hauteur du tremplin au-dessus de l'eau
N_DESCENTE = 4                   # collines occupées par la grande descente

ZONE_COLLINES = LONGUEUR_ILE - PLAGE - L_REMONTEE - OCEAN
DEBUT_REMONTEE = PLAGE + ZONE_COLLINES
DEBUT_OCEAN = DEBUT_REMONTEE + L_REMONTEE
PIED = NIVEAU_EAU - FALAISE      # le bas de la grande descente


def numero_ile(x):
    """Sur quelle île se trouve la position x ?"""
    return int(max(0.0, x) // LONGUEUR_ILE)


def est_eau(x):
    """Vrai sur la mer, entre la fin d'une île et la plage de la suivante."""
    return (max(0.0, x) % LONGUEUR_ILE) >= DEBUT_OCEAN


def reglages_ile(i):
    """Les collines de cette île : leur longueur, leur creux, leur nombre.

    La longueur est ajustée pour qu'il en tienne un nombre ENTIER entre la
    plage et le tremplin — sinon la dernière est coupée en plein milieu et
    ça fait une falaise au beau milieu du terrain.
    """
    longueur_voulue = max(120, 200 - 15 * i)
    creux_max = min(70, 50 + 4 * i)
    nombre = max(N_DESCENTE + 3, round(ZONE_COLLINES / longueur_voulue))
    return ZONE_COLLINES / nombre, creux_max, nombre


def profil_colline(t, creux):
    """Le profil habituel : descente en cosinus, remontée « en goutte »."""
    if t < R_DESCENTE:
        u = t / R_DESCENTE
        return creux * (1 - math.cos(math.pi * u)) / 2
    u = (t - R_DESCENTE) / (1 - R_DESCENTE)
    return creux * math.cos(math.pi * u / 2) ** POINTE


def hauteur_du_sol(x):
    """À la position x du monde, le sol est à quelle hauteur ?"""
    x = max(0.0, x)
    ile = numero_ile(x)
    dans_ile = x % LONGUEUR_ILE
    longueur, creux_max, nombre = reglages_ile(ile)

    # ---- 1. la plage : on sort de la mer et on remonte sur l'île ----
    if dans_ile < PLAGE:
        if ile == 0:
            return CRETE          # la toute première île commence sur un plateau
        u = dans_ile / PLAGE
        return NIVEAU_EAU + (CRETE - NIVEAU_EAU) * (1 - math.cos(math.pi * u)) / 2

    # ---- 2. les collines ----
    if dans_ile < DEBUT_REMONTEE:
        dd = dans_ile - PLAGE
        i = int(dd // longueur)
        t = dd % longueur / longueur

        premiere_descente = nombre - N_DESCENTE
        if i < premiere_descente:
            # les collines ordinaires : un creux tiré au sort, toujours le même
            creux = 30 + (creux_max - 30) * ((i * 7919 + ile * 104729) % 1000) / 1000
            return CRETE + profil_colline(t, creux)

        # la GRANDE DESCENTE : la ligne de crête plonge vers la mer, et les
        # bosses s'effacent petit à petit — on finit sur une courbe lisse.
        part = (i - premiere_descente + t) / N_DESCENTE
        base = CRETE + (PIED - CRETE) * (1 - math.cos(math.pi * part)) / 2
        return base + profil_colline(t, 30 * (1 - part) ** 1.5)

    # ---- 3. la petite remontée : le tremplin ----
    if dans_ile < DEBUT_OCEAN:
        u = (dans_ile - DEBUT_REMONTEE) / L_REMONTEE
        return PIED - H_REMONTEE * math.sin(math.pi * u / 2) ** 1.6

    # ---- 4. la mer ----
    return NIVEAU_EAU
