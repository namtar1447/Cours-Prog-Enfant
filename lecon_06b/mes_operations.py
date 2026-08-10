# ============================================================
# Leçon 06b — Calculatrice graphique
# mes_operations.py — LES OPÉRATIONS DE LA CALCULATRICE
# ============================================================
# OBJECTIF : Écrire les cinq opérations « de mathématicien » que
#            ta calculatrice sait faire. Le reste du programme est
#            déjà écrit : il ne lui manque que ces cinq fonctions.
#
#            Quand elles marcheront, lance projet.py et tu verras
#            TES fonctions faire tourner une vraie calculatrice.
#
# COMMENT TESTER : Clique sur ▶
# ============================================================

import mpmath
from mpmath import mpf


# ============================================================
# BOÎTE À OUTILS — ce que mpmath sait déjà faire
# ============================================================
# Tu n'auras pas besoin de tout. À toi de choisir.
#
#   mpmath.sqrt(n)            racine carrée de n
#   mpmath.root(n, k)         racine k-ième de n   (root(8, 3) → 2)
#   mpmath.factorial(n)       factorielle de n     (factorial(5) → 120)
#   mpmath.log10(n)           logarithme en base 10
#   mpmath.floor(n)           arrondi vers le bas
#   mpmath.pi                 π avec autant de décimales que réglé
#   a ** b                    a à la puissance b
#
# Rappel de la leçon 06 : mpf est le type « nombre à précision
# réglable » de mpmath. mpf(1) est le nombre 1.
# ============================================================


# ============================================================
# GARDE-FOUS — fournis, ne pas modifier
# ============================================================
# Sans eux, 2↑↑6 occupe l'ordinateur pendant une demi-heure.
# Appelle-les au début des fonctions concernées, c'est déjà écrit.

EXPOSANT_MAX = mpf(10) ** 15
HAUTEUR_MAX = 100


def verifier_exposant(exposant):
    if abs(exposant) > EXPOSANT_MAX:
        raise ValueError("Exposant trop grand")


def verifier_hauteur(hauteur):
    if hauteur != int(hauteur) or hauteur < 0:
        raise ValueError("Tétration : hauteur entière ≥ 0")

    if hauteur > HAUTEUR_MAX:
        raise ValueError("Tétration : hauteur trop grande")


# ============================================================
# EXEMPLE (ne pas modifier)
# ============================================================
# Voici à quoi ressemble une opération finie. Elle utilise mpmath
# pour garder toute la précision réglée dans la calculatrice.

def aire_cercle(rayon):
    """L'aire d'un cercle : π × rayon²."""
    return mpmath.pi * rayon ** 2


# ============================================================
# TON TOUR
# ============================================================

# TODO 1 : puissance(base, exposant)
#           Renvoie la base élevée à l'exposant.
#           Le garde-fou verifier_exposant(exposant) doit être appelé
#           EN PREMIER — sinon 2↑↑6 fige la calculatrice.

def puissance(base, exposant):
    verifier_exposant(exposant)
    # ton code ici


# TODO 2 : racine_carree(nombre)
#           Renvoie la racine carrée du nombre.

def racine_carree(nombre):
    pass


# TODO 3 : racine_nieme(nombre, indice)
#           Renvoie la racine « indice »-ième du nombre.
#           racine_nieme(8, 3) doit donner 2, parce que 2×2×2 = 8.
#           Attention : mpmath.root veut un indice entier.

def racine_nieme(nombre, indice):
    pass


# TODO 4 : factorielle(nombre)
#           Renvoie la factorielle : 5! = 5×4×3×2×1 = 120.

def factorielle(nombre):
    pass


# TODO 5 : tetration(base, hauteur)
#           base↑↑hauteur = base^(base^(base^…)), hauteur fois.
#           2↑↑3 = 2^(2^2) = 2^4 = 16.
#           Tu l'as déjà écrite à la leçon 06 — mais cette fois,
#           sers-toi de TA fonction puissance() du TODO 1, pour que
#           le garde-fou s'applique aussi à chaque étage.
#           Rappel : une hauteur de 0 donne 1.

def tetration(base, hauteur):
    verifier_hauteur(hauteur)
    # ton code ici


if __name__ == "__main__":
    from tests import tester_operations
    tester_operations()
