# ============================================================
# Leçon 12 — terrain.py
# ============================================================
# Le terrain à îles de la leçon 11, REFAIT après comparaison avec
# Tiny Wings et deux essais du père :
#
#   · le départ est un court plateau
#   · chaque île commence par une DESCENTE (on y atterrit en douceur)
#   · elle finit par une TRÈS LONGUE descente bosselée, qui plonge loin
#   · puis une bosse arrondie, d'où part le grand saut
#   · le saut par-dessus la mer réussit toujours (voir partie.py)
#
# Comme dans Tiny Wings, chaque île repart de la même hauteur : la mer est
# le repère fixe. La grande descente peut donc plonger très bas sans que le
# monde « glisse » vers le bas d'une île à l'autre.
#
# Une île se lit de gauche à droite :
#
#   rive  collines ordinaires     la grande descente bosselée    bosse  MER
#   /‾‾\__/‾‾\__/‾‾\__/‾‾\__/‾‾\_
#                                \_^_^_^_^_
#                                          \_^_^_^_^_
#                                                    \_______/‾\___~~~~~~
#
# Tu n'as rien à modifier ici.
# ============================================================

import math

CRETE = 46                       # hauteur du sommet des collines
R_DESCENTE = 0.62                # part de la colline occupée par la descente
POINTE = 2.2                     # netteté du sommet

LONGUEUR_ILE = 7600              # une île fait 7 600 px, soit 760 m
PLATEAU = 100                    # le plat du tout début de la partie
RIVE = 80                        # la rive qui sort de l'eau, au début d'une île
OCEAN = 500                      # la mer à franchir au bout

L_DESCENTE = 1700                # la grande descente de fin d'île…
PIED = 226                       # … jusqu'où elle plonge
N_BOSSES = 22                    # ses petites bosses, qui s'effacent
H_BOSSES = 14                    # la hauteur des premières bosses

L_TREMPLIN = 200                 # la bosse de la fin d'île
H_TREMPLIN = 60                  # de combien elle remonte
NIVEAU_EAU = PIED + 20           # la mer, sous le pied de la descente

ZONE_COLLINES = LONGUEUR_ILE - RIVE - L_DESCENTE - L_TREMPLIN - OCEAN
DEBUT_DESCENTE = RIVE + ZONE_COLLINES
DEBUT_TREMPLIN = DEBUT_DESCENTE + L_DESCENTE
SOMMET_TREMPLIN = DEBUT_TREMPLIN + 0.6 * L_TREMPLIN
DEBUT_OCEAN = DEBUT_TREMPLIN + L_TREMPLIN


def numero_ile(x):
    """Sur quelle île se trouve la position x ?"""
    return int(max(0.0, x) // LONGUEUR_ILE)


def position_dans_ile(x):
    """Combien de pixels depuis le début de l'île."""
    return max(0.0, x) % LONGUEUR_ILE


def est_eau(x):
    """Vrai sur la mer, entre la fin d'une île et la rive de la suivante."""
    return position_dans_ile(x) >= DEBUT_OCEAN


def dans_la_descente(x):
    """Vrai sur la grande descente de fin d'île."""
    return DEBUT_DESCENTE <= position_dans_ile(x) < DEBUT_TREMPLIN


def dans_le_tremplin(x):
    """Vrai sur la bosse de fin d'île, d'où part le grand saut."""
    return DEBUT_TREMPLIN <= position_dans_ile(x) < DEBUT_OCEAN


def apres_le_sommet(x):
    """Vrai si on a dépassé le haut du tremplin."""
    return position_dans_ile(x) >= SOMMET_TREMPLIN


def reglages_ile(i):
    """Les collines de cette île : leur longueur, leur creux, leur nombre.

    La longueur est ajustée pour qu'il en tienne un nombre ENTIER — sinon la
    dernière est coupée en plein milieu et ça fait une falaise.
    """
    longueur_voulue = max(150, 200 - 8 * i)
    creux_max = min(70, 50 + 4 * i)
    nombre = max(3, round(ZONE_COLLINES / longueur_voulue))
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

    # ---- 1. le début : un court plateau, ou la rive qui sort de l'eau ----
    if dans_ile < RIVE:
        if ile == 0:
            return CRETE
        u = dans_ile / RIVE
        return NIVEAU_EAU + (CRETE - NIVEAU_EAU) * (1 - math.cos(math.pi * u)) / 2

    # ---- 2. les collines ordinaires ----
    if dans_ile < DEBUT_DESCENTE:
        dd = dans_ile - RIVE
        if ile == 0:
            dd -= PLATEAU - RIVE         # le plateau du départ
            if dd < 0:
                return CRETE
        i = int(dd // longueur)
        t = dd % longueur / longueur
        # un creux tiré au sort, toujours le même pour la même colline
        creux = 30 + (creux_max - 30) * ((i * 7919 + ile * 104729) % 1000) / 1000
        return CRETE + profil_colline(t, creux)

    # ---- 3. la grande descente : elle plonge, ses bosses s'effacent ----
    if dans_ile < DEBUT_TREMPLIN:
        part = (dans_ile - DEBUT_DESCENTE) / L_DESCENTE
        base = CRETE + (PIED - CRETE) * (1 - math.cos(math.pi * part)) / 2
        bosse = (part * N_BOSSES) % 1.0
        return base + profil_colline(bosse, H_BOSSES * (1 - part) ** 1.5)

    # ---- 4. le tremplin : il monte, s'arrondit, et redescend dans l'eau ----
    if dans_ile < DEBUT_OCEAN:
        u = (dans_ile - DEBUT_TREMPLIN) / L_TREMPLIN
        haut = PIED - H_TREMPLIN
        if u < 0.6:
            return PIED - H_TREMPLIN * math.sin(math.pi / 2 * u / 0.6) ** 1.6
        v = (u - 0.6) / 0.4
        return haut + (NIVEAU_EAU - haut) * (1 - math.cos(math.pi * v)) / 2

    # ---- 5. la mer ----
    return NIVEAU_EAU


def fond_des_vallees(x):
    """Le plus bas que descend le terrain un peu plus loin — pour la caméra.

    Dans la grande descente, on regarde 300 px devant : la caméra montre
    la pente qui arrive, sans reculer d'un coup jusqu'au fond.
    """
    if position_dans_ile(x) >= DEBUT_DESCENTE - 300:
        return max(hauteur_du_sol(x + 300), CRETE + reglages_ile(numero_ile(x))[1])
    return CRETE + reglages_ile(numero_ile(x))[1]
