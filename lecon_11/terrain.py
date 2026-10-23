# ============================================================
# Leçon 11 — terrain.py
# ============================================================
# Ton terrain de la leçon 10, qui apprend deux choses de plus :
#
#   · le monde est découpé en ÎLES de 4 000 pixels
#   · chaque île est un peu plus dure que la précédente
#     (collines plus courtes, creux plus profonds)
#
# Et à la fin de chaque île : l'OCÉAN. Une grande rampe te lance,
# puis 240 pixels d'eau plate à traverser avant l'île suivante.
#
# Tu n'as rien à modifier ici.
# ============================================================

import math

CRETE = 46                       # hauteur du sommet des collines
R_DESCENTE = 0.62                # part de la colline occupée par la descente
POINTE = 2.2                     # netteté du sommet

LONGUEUR_ILE = 4000              # une île fait 4 000 px, soit 400 m
LARGEUR_OCEAN = 240              # l'eau à traverser au bout de chaque île
NIVEAU_EAU = 108                 # la hauteur de la mer


def numero_ile(x):
    """Sur quelle île se trouve la position x ?"""
    return int(x // LONGUEUR_ILE)


def reglages_ile(i):
    """Plus on avance, plus les collines sont courtes et creuses."""
    longueur_colline = max(120, 200 - 15 * i)
    creux_max = min(110, 65 + 10 * i)
    return longueur_colline, creux_max


def hauteur_du_sol(x):
    """À la position x du monde, le sol est à quelle hauteur ?"""
    ile = numero_ile(x)
    dans_ile = x % LONGUEUR_ILE
    longueur_colline, creux_max = reglages_ile(ile)

    debut_ocean = LONGUEUR_ILE - LARGEUR_OCEAN

    # 1. l'océan : tout plat, et bas
    if dans_ile >= debut_ocean:
        return NIVEAU_EAU

    # 2. la dernière colline avant l'eau : une rampe de lancement
    #    (descente très longue, remontée courte et cambrée)
    if dans_ile >= debut_ocean - longueur_colline:
        t = (dans_ile - (debut_ocean - longueur_colline)) / longueur_colline
        creux = creux_max + 15
        if t < 0.75:
            u = t / 0.75
            return CRETE + creux * (1 - math.cos(math.pi * u)) / 2
        u = (t - 0.75) / 0.25
        return CRETE + creux * math.cos(math.pi * u / 2) ** POINTE

    # 3. les collines ordinaires de l'île
    i = int(dans_ile // longueur_colline)
    creux = 30 + (creux_max - 30) * ((i * 7919 + ile * 104729) % 1000) / 1000
    t = dans_ile % longueur_colline / longueur_colline

    if t < R_DESCENTE:
        u = t / R_DESCENTE
        return CRETE + creux * (1 - math.cos(math.pi * u)) / 2

    u = (t - R_DESCENTE) / (1 - R_DESCENTE)
    return CRETE + creux * math.cos(math.pi * u / 2) ** POINTE
