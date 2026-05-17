# ============================================================
# Leçon 02 — Conditions — if / elif / else
# Exercice 01 — Division sans catastrophe  (guidé)
# ============================================================
# OBJECTIF : Demande deux nombres à l'utilisateur et divise
#            le premier par le second.
#            Si le deuxième est zéro, affiche un message d'erreur
#            au lieu de planter le programme !
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici comment utiliser if / else pour choisir une action :

pv = 30
degats = 35

if degats > pv:
    print("Le héros est K.O. !")
else:
    print(f"Il reste {pv - degats} PV.")
# Essaie de changer  degats = 10  et re-roule — l'autre branche s'exécute !


# --- TON TOUR ---

# TODO 1 : Demande un premier nombre entier à l'utilisateur.
#           Stocke-le dans une variable appelée  a .
#           N'oublie pas de convertir avec int() !


# TODO 2 : Demande un deuxième nombre entier à l'utilisateur.
#           Stocke-le dans une variable appelée  b .


# TODO 3 : Vérifie si  b  est égal à zéro.
#           Si oui, affiche exactement :
#           Erreur : impossible de diviser par zéro !


# TODO 4 : Sinon (b n'est pas zéro), ajoute le code après le print plus haut
#           Calcule  a / b  et affiche le résultat.
#           Le résultat doit ressembler à (si a=10 et b=2) :
#           10 / 2 = 5.0


if __name__ == "__main__":
    from tests import tester_ex1
    tester_ex1()
