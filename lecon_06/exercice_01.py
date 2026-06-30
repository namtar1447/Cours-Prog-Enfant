# ============================================================
# Leçon 06 — Modules et mpmath
# Exercice 01 — Mathématiques de précision  (guidé)
# ============================================================
# OBJECTIF : Utiliser import math et mpmath pour faire des
#            calculs impossibles à faire à la main.
#
# 🔧 Avant de commencer :
#    Installer mpmath dans Thonny :
#    Outils → Gérer les paquets → chercher "mpmath" → Installer
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici comment utiliser import et mpmath :

import math
from mpmath import mp

mp.dps = 15                        # 15 décimales (comme Python normal)
print(f"sqrt(2)  = {math.sqrt(2)}")    # environ 1.41421356...
print(f"π normal = {math.pi}")         # 3.141592653589793

mp.dps = 50                        # 50 décimales avec mpmath
print(f"π précis = {mp.pi}")          # 50 décimales exactes !


# --- TON TOUR ---

# TODO 1 : Dans une pièce de 6 m × 8 m, calcule la longueur
#           de la diagonale avec math.sqrt et le théorème de Pythagore.
#           (rappel : diagonale = sqrt(longueur² + largeur²))
#           Affiche "La diagonale mesure X mètres"


# TODO 2 : Calcule math.factorial(15) et affiche le résultat.
#           Ensuite affiche "factorial(15) a X chiffres"
#           (Astuce : len(str(nombre)) compte les chiffres)


# TODO 3 : Calcule math.factorial(100) et affiche
#           uniquement le nombre de chiffres qu'il contient.
#           Affiche "factorial(100) a X chiffres !"


# TODO 4 : Règle mp.dps à 50 et affiche mp.pi.
#           Ensuite règle mp.dps à 100 et affiche mp.pi à nouveau.
#           Quelle différence vois-tu ?


# TODO 5 : Affiche une table de factorielles de 1 à 12
#           avec une boucle for.
#           Format de chaque ligne :
#             "1!  = 1          (1 chiffre)"
#             "10! = 3628800    (7 chiffres)"


if __name__ == "__main__":
    from tests import tester_ex01
    tester_ex01()
