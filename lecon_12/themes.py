# ============================================================
# Leçon 12 — themes.py
# ============================================================
# QUATRE thèmes maintenant, rangés dans une LISTE : THEMES.
# Chaque thème est un DICTIONNAIRE (leçon 05), avec :
#
#   "nom"       ce qu'on affiche dans le menu
#   "distance"  le record qu'il faut avoir pour le débloquer
#   "gravite"   la gravité quand on plane — un thème peut changer le jeu,
#               pas seulement les couleurs !
#   les couleurs, de jour et de nuit, comme à la leçon 11
#
# Pour lire une valeur :   THEMES[0]["nom"]       → "Dragonneau"
#                          THEMES[3]["gravite"]   → 0.037
#
# Tu n'as rien à modifier ici.
# ============================================================

# Les couleurs ont été choisies pour que tout reste bien visible À TOUTE
# HEURE, dans les quatre thèmes : le ciel et les collines ne se confondent
# jamais, et le dragonneau garde son contour.

DRAGONNEAU = {
    "nom": "Dragonneau",
    "distance": 0,               # débloqué dès le début
    "gravite": 0.06,

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

SKI = {
    "nom": "Ski",
    "distance": 900,
    "gravite": 0.06,

    # --- de jour : neige, ciel bleu, lac gelé ---
    "ciel":     (106, 154, 208),
    "collines": (236, 242, 249),
    "ombre":    (177, 200, 232),
    "eau":      (147, 200, 225),
    "heros":    (233, 77, 68),
    "aile":     (169, 40, 40),
    "contour":  (24, 24, 38),

    # --- de nuit ---
    "ciel_nuit":     (19, 32, 48),
    "collines_nuit": (92, 95, 98),
    "ombre_nuit":    (58, 67, 78),
    "eau_nuit":      (41, 60, 68),
    "heros_nuit":    (177, 57, 49),
    "aile_nuit":     (127, 28, 28),
    "contour_nuit":  (6, 6, 13),
}

DAUPHIN = {
    "nom": "Dauphin",
    "distance": 1500,
    "gravite": 0.06,

    # --- de jour : des vagues, et un dauphin gris-bleu ---
    "ciel":     (97, 186, 230),
    "collines": (30, 111, 171),
    "ombre":    (21, 80, 132),
    "eau":      (19, 60, 119),
    "heros":    (191, 226, 242),
    "aile":     (109, 149, 183),
    "contour":  (17, 26, 43),

    # --- de nuit ---
    "ciel_nuit":     (30, 65, 83),
    "collines_nuit": (5, 36, 59),
    "ombre_nuit":    (1, 15, 30),
    "eau_nuit":      (1, 11, 30),
    "heros_nuit":    (125, 149, 159),
    "aile_nuit":     (70, 97, 121),
    "contour_nuit":  (4, 7, 17),
}

LUNE = {
    "nom": "Lune",
    "distance": 3000,
    "gravite": 0.037,            # sur la Lune, on plane plus longtemps !

    # --- de jour : le ciel est toujours noir dans l'espace ---
    "ciel":     (40, 36, 65),
    "collines": (151, 148, 159),
    "ombre":    (107, 105, 119),
    "eau":      (74, 74, 90),    # les « mers » de la Lune : de la roche sombre
    "heros":    (233, 233, 233),
    "aile":     (155, 166, 196),
    "contour":  (24, 24, 38),

    # --- de nuit ---
    "ciel_nuit":     (15, 12, 27),
    "collines_nuit": (53, 53, 57),
    "ombre_nuit":    (32, 31, 36),
    "eau_nuit":      (35, 35, 43),
    "heros_nuit":    (149, 149, 149),
    "aile_nuit":     (99, 106, 127),
    "contour_nuit":  (6, 6, 13),
}

# La liste des thèmes, dans l'ordre du menu.
THEMES = [DRAGONNEAU, SKI, DAUPHIN, LUNE]


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
