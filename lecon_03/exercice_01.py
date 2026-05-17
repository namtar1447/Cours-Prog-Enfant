# ============================================================
# Leçon 03 — Boucles — for / while
# Exercice 01 — La table de multiplication  (guidé)
# ============================================================
# OBJECTIF : Demande un nombre à l'utilisateur et affiche
#            sa table de multiplication complète (de 1 à 10)
#            en utilisant une boucle for.
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici une boucle for qui compte de 1 à 5 :

for i in range(1, 6):
    print(f"Tour numéro {i}")
# Affiche : Tour numéro 1, Tour numéro 2, ... Tour numéro 5


# --- TON TOUR ---

# TODO 1 : Demande un nombre entier à l'utilisateur.
#           Stocke-le dans une variable appelée  n .


# TODO 2 : Affiche un titre avant le tableau.
#           Le résultat doit ressembler à (si l'utilisateur tape 7) :
#           === Table du 7 ===


# TODO 3 : Écris une boucle for qui répète 10 fois (de 1 à 10).
#           À chaque tour, affiche la multiplication.
#           Le résultat doit ressembler à :
#           7 × 1 = 7
#           7 × 2 = 14
#           ...
#           7 × 10 = 70
#
#           Rappel : pour multiplier, utilise *
#           Pour afficher ×, écris directement le symbole ×


if __name__ == "__main__":
    from tests import tester_ex1
    tester_ex1()
