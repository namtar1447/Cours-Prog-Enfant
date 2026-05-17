# ============================================================
# Leçon 03 — Boucles — for / while
# Exercice 02 — Compte à rebours  (semi-guidé)
# ============================================================
# OBJECTIF : Crée un compte à rebours avec une boucle while.
#            Le programme demande un nombre de départ,
#            affiche chaque nombre en descendant jusqu'à 1,
#            puis annonce le décollage !
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici comment while diminue un compteur :

vie = 3
while vie > 0:
    print(f"Il reste {vie} vie(s)")
    vie = vie - 1
print("Game over !")


# --- TON TOUR ---

# TODO 1 : Demande un nombre entier à l'utilisateur.
#           Stocke-le dans une variable appelée  depart .
#           Ce sera le point de départ du compte à rebours.


# TODO 2 : Tant que  depart  est supérieur à zéro :
#           Affiche le nombre actuel.
#           Puis diminue  depart  de 1.
#           (N'oublie pas le décalage avec Tab !)


# TODO 3 : Quand la boucle est terminée, affiche :
#           🚀 Décollage !


if __name__ == "__main__":
    from tests import tester_ex2
    tester_ex2()
