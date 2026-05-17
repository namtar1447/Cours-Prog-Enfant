# ============================================================
# Leçon 02 — Conditions — if / elif / else
# Exercice 02 — Calculatrice à choix  (semi-guidé)
# ============================================================
# OBJECTIF : Demande deux nombres et une opération (+, -, *, /)
#            à l'utilisateur, puis affiche le bon résultat.
#            Si l'opération est inconnue, dis-le !
#            Si on divise par zéro, protège le programme !
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici comment choisir parmi plusieurs cas avec elif :

saison = "hiver"

if saison == "été":
    print("Il fait chaud !")
elif saison == "hiver":
    print("Couvre-toi bien !")
elif saison == "printemps":
    print("Les fleurs poussent !")
else:
    print("Saison inconnue.")


# --- TON TOUR ---

# TODO 1 : Demande un premier nombre entier  a  à l'utilisateur,
#           puis un deuxième entier  b .
#           (Deux lignes, comme dans l'exercice 01.)


# TODO 2 : Demande l'opération à effectuer.
#           Stocke-la dans une variable appelée  op .
#           Exemple de message : "Opération (+, -, *, /) : "
#           Attention : op est du texte (str), pas de int() ici !


# TODO 3 : Utilise if / elif / else pour choisir la bonne opération.
#           • Si op est "+"  → affiche  a + b
#           • Si op est "-"  → affiche  a - b
#           • Si op est "*"  → affiche  a * b
#           • Si op est "/"  :
#               - si b == 0 → affiche "Erreur : division par zéro !"
#               - sinon     → affiche  a / b
#           • Sinon (opération inconnue) → affiche "Opération inconnue !"
#
#           Rappel : pour comparer une chaîne, écris  op == "+"


if __name__ == "__main__":
    from tests import tester_ex2
    tester_ex2()
