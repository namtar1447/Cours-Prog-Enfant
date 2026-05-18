# ============================================================
# Leçon 04 — Fonctions, paramètres, return
# Exercice 01 — Mes premières fonctions mathématiques  (guidé)
# ============================================================
# OBJECTIF : Créer des fonctions qui calculent et retournent
#            un résultat, puis les appeler pour l'afficher.
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici une fonction qui triple un nombre et retourne le résultat :

def tripler(n):
    return n * 3

print(f"tripler(4) = {tripler(4)}")   # affiche : tripler(4) = 12
print(f"tripler(7) = {tripler(7)}")   # affiche : tripler(7) = 21


# --- TON TOUR ---

# TODO 1 : Crée une fonction doubler(n) qui retourne le double de n.
#           Exemples attendus :
#             doubler(5)  → retourne 10
#             doubler(3)  → retourne 6


# TODO 2 : Crée une fonction carre(n) qui retourne n multiplié par n.
#           Exemples attendus :
#             carre(4)  → retourne 16
#             carre(9)  → retourne 81


# TODO 3 : Crée une fonction perimetre_rectangle(longueur, largeur)
#           qui retourne le périmètre d'un rectangle.
#           Rappel : périmètre = 2 × longueur + 2 × largeur
#           Exemples attendus :
#             perimetre_rectangle(5, 3)  → retourne 16
#             perimetre_rectangle(10, 4) → retourne 28


# TODO 4 : Appelle tes 3 fonctions avec des valeurs de ton choix
#           et affiche les résultats avec print() et des f-strings.
#           Exemple de format :
#             Le double de 6 = 12
#             Le carré de 5 = 25
#             Périmètre d'un rectangle 8×3 = 22


if __name__ == "__main__":
    from tests import tester_ex01
    tester_ex01()
