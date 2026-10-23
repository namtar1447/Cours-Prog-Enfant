# ============================================================
# Leçon 11 — terrain.py
# ============================================================
# Ton terrain de la leçon 10, qui apprend deux choses de plus :
#
#   · le monde est découpé en ÎLES de 4 000 pixels
#   · chaque île est un peu plus dure que la précédente
#     (collines plus courtes, creux plus profonds)
#
# Et au bout de chaque île : la mer. Une grande rampe te lance,
# une plage descend vers l'eau, et une autre remonte sur l'île
# suivante.
#
# Tu n'as rien à modifier ici.
# ============================================================

import math

CRETE = 46                       # hauteur du sommet des collines ET du rivage
R_DESCENTE = 0.62                # part de la colline occupée par la descente
POINTE = 2.2                     # netteté du sommet

LONGUEUR_ILE = 4000              # une île fait 4 000 px, soit 400 m
LARGEUR_OCEAN = 240              # la mer au bout de l'île
PLAGE = 80                       # la pente qui descend (et remonte) de la mer
NIVEAU_EAU = 108                 # la hauteur de la mer

LARGEUR_TERRE = LONGUEUR_ILE - LARGEUR_OCEAN


def numero_ile(x):
    """Sur quelle île se trouve la position x ?"""
    return int(max(0.0, x) // LONGUEUR_ILE)


def reglages_ile(i):
    """Les collines de cette île : leur longueur, leur creux, leur nombre.

    La longueur est ajustée pour que les collines tombent JUSTE : il en
    faut un nombre entier entre le début de l'île et la mer, sinon la
    dernière est coupée en plein milieu et ça fait une falaise.
    """
    longueur_voulue = max(120, 200 - 15 * i)
    creux_max = min(110, 65 + 10 * i)
    nombre = max(3, round(LARGEUR_TERRE / longueur_voulue))
    return LARGEUR_TERRE / nombre, creux_max, nombre


def est_eau(x):
    """Vrai seulement sur la mer plate, entre les deux plages."""
    dans_ile = max(0.0, x) % LONGUEUR_ILE
    return LARGEUR_TERRE + PLAGE <= dans_ile < LONGUEUR_ILE - PLAGE


def hauteur_du_sol(x):
    """À la position x du monde, le sol est à quelle hauteur ?"""
    x = max(0.0, x)                  # avant le départ, le plateau continue
    ile = numero_ile(x)
    dans_ile = x % LONGUEUR_ILE
    longueur, creux_max, nombre = reglages_ile(ile)

    # ---- la mer, et ses deux plages ----
    if dans_ile >= LARGEUR_TERRE:
        descente = (dans_ile - LARGEUR_TERRE) / PLAGE
        if descente < 1.0:                               # la plage qui descend
            return CRETE + (NIVEAU_EAU - CRETE) * (1 - math.cos(math.pi * descente)) / 2

        remontee = (dans_ile - (LONGUEUR_ILE - PLAGE)) / PLAGE
        if remontee > 0.0:                               # la plage qui remonte
            return NIVEAU_EAU + (CRETE - NIVEAU_EAU) * (1 - math.cos(math.pi * remontee)) / 2

        return NIVEAU_EAU                                # l'eau, bien plate

    # ---- les collines ----
    i = int(dans_ile // longueur)
    t = dans_ile % longueur / longueur

    # la dernière de l'île est la RAMPE : longue descente, remontée cambrée
    if i == nombre - 1:
        creux = creux_max + 15
        if t < 0.75:
            u = t / 0.75
            return CRETE + creux * (1 - math.cos(math.pi * u)) / 2
        u = (t - 0.75) / 0.25
        return CRETE + creux * math.cos(math.pi * u / 2) ** POINTE

    # les collines ordinaires : un creux tiré au sort, toujours le même
    creux = 30 + (creux_max - 30) * ((i * 7919 + ile * 104729) % 1000) / 1000

    if t < R_DESCENTE:
        u = t / R_DESCENTE
        return CRETE + creux * (1 - math.cos(math.pi * u)) / 2

    u = (t - R_DESCENTE) / (1 - R_DESCENTE)
    return CRETE + creux * math.cos(math.pi * u / 2) ** POINTE
