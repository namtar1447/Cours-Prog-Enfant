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
    """Fabrique la couleur du moment.

    part_de_nuit = 0.0  → la couleur de jour
    part_de_nuit = 1.0  → la couleur de nuit
    part_de_nuit = 0.5  → pile entre les deux
    """
    melange = []
    for jour, nuit in zip(couleur_jour, couleur_nuit):
        melange.append(int(jour + (nuit - jour) * part_de_nuit))
    return tuple(melange)
