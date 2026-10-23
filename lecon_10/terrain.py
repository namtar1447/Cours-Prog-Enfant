# ============================================================
# Leçon 10 — terrain.py
# ============================================================
# TON code de la leçon 09, déménagé dans son propre fichier.
#
# Pourquoi ? Parce que jeu.py commence à être long, et que tout ce qui
# est écrit ici ne parle QUE des collines. Un fichier, une idée.
#
# Tu n'as rien à modifier ici. jeu.py s'en sert avec la ligne :
#
#     from terrain import hauteur_du_sol, CRETE
#
# (c'est l'import de la leçon 06, dans sa deuxième forme : on nomme
#  directement ce qu'on veut prendre dans le module)
# ============================================================

import math

L_COLLINE = 200                  # longueur d'une colline, en pixels
CRETE = 46                       # hauteur du sommet (toujours la même)
D_MIN, D_MAX = 30, 65            # le creux le moins et le plus profond
R_DESCENTE = 0.62                # part de la colline occupée par la descente
POINTE = 2.2                     # netteté du sommet


def hauteur_du_sol(x):
    """À la position x du monde, le sol est à quelle hauteur ?"""
    i = int(x // L_COLLINE)
    t = x % L_COLLINE / L_COLLINE

    creux = D_MIN + (D_MAX - D_MIN) * ((i * 7919) % 1000) / 1000

    if t < R_DESCENTE:
        u = t / R_DESCENTE
        return CRETE + creux * (1 - math.cos(math.pi * u)) / 2

    u = (t - R_DESCENTE) / (1 - R_DESCENTE)
    return CRETE + creux * math.cos(math.pi * u / 2) ** POINTE
