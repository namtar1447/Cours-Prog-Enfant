# ============================================================
# Leçon 12 — terrain.py
# ============================================================
# Le terrain à îles de la leçon 11, REFAIT après comparaison avec
# Tiny Wings et un essai du père :
#
#   · le départ est un court plateau
#   · chaque île commence par une DESCENTE (on y atterrit en douceur)
#   · la grande descente de fin d'île plonge vraiment
#   · le tremplin est une bosse arrondie, pas une falaise
#   · le saut par-dessus la mer réussit toujours (voir partie.py)
#
# Une île se lit de gauche à droite :
#
#        rive   collines ordinaires      grande descente  tremplin   MER
#   ~~~~/‾‾\__/‾‾\__/‾‾\__/‾‾\__/‾‾\__\_/‾\_/‾\__          _/‾‾\_~~~~~~~~~~
#                                               \________/
#
# Tu n'as rien à modifier ici.
# ============================================================

import math

CRETE = 46                       # hauteur du sommet des collines
R_DESCENTE = 0.62                # part de la colline occupée par la descente
POINTE = 2.2                     # netteté du sommet

NIVEAU_EAU = 108                 # la hauteur de la mer

LONGUEUR_ILE = 5600              # une île fait 5 600 px, soit 560 m
PLATEAU = 100                    # le plat du tout début de la partie
RIVE = 80                        # la rive qui sort de l'eau, au début d'une île
OCEAN = 500                      # la mer à franchir au bout
L_TREMPLIN = 200                 # la bosse de la fin d'île
H_TREMPLIN = 60                  # de combien elle remonte
PIED = 130                       # le fond de la grande descente
N_DESCENTE = 3                   # collines occupées par la grande descente

ZONE_COLLINES = LONGUEUR_ILE - RIVE - L_TREMPLIN - OCEAN
DEBUT_TREMPLIN = RIVE + ZONE_COLLINES
SOMMET_TREMPLIN = DEBUT_TREMPLIN + 0.6 * L_TREMPLIN
DEBUT_OCEAN = DEBUT_TREMPLIN + L_TREMPLIN


def numero_ile(x):
    """Sur quelle île se trouve la position x ?"""
    return int(max(0.0, x) // LONGUEUR_ILE)


def est_eau(x):
    """Vrai sur la mer, entre la fin d'une île et la rive de la suivante."""
    return (max(0.0, x) % LONGUEUR_ILE) >= DEBUT_OCEAN


def dans_le_tremplin(x):
    """Vrai sur la bosse de fin d'île, d'où part le grand saut."""
    return DEBUT_TREMPLIN <= (max(0.0, x) % LONGUEUR_ILE) < DEBUT_OCEAN


def apres_le_sommet(x):
    """Vrai si on a dépassé le haut du tremplin."""
    return (max(0.0, x) % LONGUEUR_ILE) >= SOMMET_TREMPLIN


def reglages_ile(i):
    """Les collines de cette île : leur longueur, leur creux, leur nombre.

    La longueur est ajustée pour qu'il en tienne un nombre ENTIER — sinon la
    dernière est coupée en plein milieu et ça fait une falaise.
    """
    longueur_voulue = max(150, 200 - 8 * i)
    creux_max = min(70, 50 + 4 * i)
    nombre = max(N_DESCENTE + 3, round(ZONE_COLLINES / longueur_voulue))
    return ZONE_COLLINES / nombre, creux_max, nombre


def fond_des_vallees(x):
    """Le plus bas que descend le terrain par ici — pour la caméra."""
    if (max(0.0, x) % LONGUEUR_ILE) >= DEBUT_TREMPLIN - 3 * 200:
        return PIED
    return CRETE + reglages_ile(numero_ile(x))[1]


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

    # ---- 1. le début : un court plateau, ou la rive qui sort de l'eau ----
    if dans_ile < RIVE:
        if ile == 0:
            return CRETE
        u = dans_ile / RIVE
        return NIVEAU_EAU + (CRETE - NIVEAU_EAU) * (1 - math.cos(math.pi * u)) / 2

    # ---- 2. les collines, puis la grande descente ----
    if dans_ile < DEBUT_TREMPLIN:
        dd = dans_ile - RIVE
        if ile == 0:
            dd -= PLATEAU - RIVE         # le plateau du départ
            if dd < 0:
                return CRETE
        i = int(dd // longueur)
        t = dd % longueur / longueur

        premiere_descente = nombre - N_DESCENTE
        if i < premiere_descente:
            # les collines ordinaires : un creux tiré au sort, toujours le même
            creux = 30 + (creux_max - 30) * ((i * 7919 + ile * 104729) % 1000) / 1000
            return CRETE + profil_colline(t, creux)

        # la GRANDE DESCENTE : la ligne de crête plonge, et les bosses
        # s'effacent petit à petit — on finit sur une courbe lisse.
        part = min(1.0, (i - premiere_descente + t) / N_DESCENTE)
        base = CRETE + (PIED - CRETE) * (1 - math.cos(math.pi * part)) / 2
        return base + profil_colline(t, 30 * (1 - part) ** 1.5)

    # ---- 3. le tremplin : il monte, s'arrondit, et redescend dans l'eau ----
    if dans_ile < DEBUT_OCEAN:
        u = (dans_ile - DEBUT_TREMPLIN) / L_TREMPLIN
        haut = PIED - H_TREMPLIN
        if u < 0.6:
            return PIED - H_TREMPLIN * math.sin(math.pi / 2 * u / 0.6) ** 1.6
        v = (u - 0.6) / 0.4
        return haut + (NIVEAU_EAU - haut) * (1 - math.cos(math.pi * v)) / 2

    # ---- 4. la mer ----
    return NIVEAU_EAU
