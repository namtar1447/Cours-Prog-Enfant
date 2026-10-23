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

DRAGONNEAU = {
    "nom": "Dragonneau",

    # --- de jour ---
    "ciel":      (38, 28, 66),
    "collines":  (58, 138, 68),
    "ombre":     (32, 92, 48),
    "eau":       (40, 90, 150),

    # --- de nuit ---
    "ciel_nuit":     (6, 6, 16),
    "collines_nuit": (14, 34, 20),
    "ombre_nuit":    (8, 22, 14),
    "eau_nuit":      (8, 18, 38),
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
