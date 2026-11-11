# ============================================================
# Leçon 11 — themes.py
# ============================================================
# Un THÈME, c'est un dictionnaire de couleurs — exactement les
# dictionnaires de la leçon 05, mais qui servent à peindre un jeu.
#
# Chaque couleur existe en DEUX versions : de jour, et de nuit.
# Pendant la partie, on fabrique la couleur du moment en mélangeant
# les deux, selon l'heure qu'il est.
#
# À la leçon 12, il y en aura quatre, et ils se débloqueront.
# Pour l'instant, un seul : le thème Dragonneau.
#
# Tu n'as rien à modifier ici.
# ============================================================

# Les couleurs ont été choisies pour que le dragonneau et les collines
# restent bien visibles À TOUTE HEURE : la nuit assombrit tout, mais
# jamais au point que deux choses se confondent.

DRAGONNEAU = {
    "nom": "Dragonneau",

    # --- de jour ---
    "ciel":     (134, 187, 243),
    "collines": (70, 151, 78),
    "ombre":    (48, 118, 63),
    "eau":      (53, 129, 195),
    "heros":    (222, 88, 54),
    "aile":     (162, 50, 38),
    "contour":  (25, 24, 37),

    # --- de nuit ---
    "ciel_nuit":     (42, 59, 76),
    "collines_nuit": (15, 32, 16),
    "ombre_nuit":    (5, 13, 7),
    "eau_nuit":      (16, 39, 60),
    "heros_nuit":    (169, 67, 41),
    "aile_nuit":     (121, 37, 29),
    "contour_nuit":  (7, 7, 11),
}


def melanger(couleur_jour, couleur_nuit, part_de_nuit):
    """Fabrique la couleur du moment, comme on mélange de la peinture.

    part_de_nuit = 0.0   → que de la peinture de jour
    part_de_nuit = 0.25  → 3 cuillères de jour pour 1 cuillère de nuit
    part_de_nuit = 0.5   → moitié-moitié
    part_de_nuit = 1.0   → que de la peinture de nuit

    Une couleur, c'est trois nombres (rouge, vert, bleu) : on fait le
    même mélange sur chacun des trois.
    """
    part_de_jour = 1 - part_de_nuit

    rouge = couleur_jour[0] * part_de_jour + couleur_nuit[0] * part_de_nuit
    vert  = couleur_jour[1] * part_de_jour + couleur_nuit[1] * part_de_nuit
    bleu  = couleur_jour[2] * part_de_jour + couleur_nuit[2] * part_de_nuit

    return (round(rouge), round(vert), round(bleu))
