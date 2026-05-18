# ============================================================
# Leçon 05 — Listes et dictionnaires
# Exercice 01 — L'inventaire du héros  (guidé)
# ============================================================
# OBJECTIF : Créer et manipuler une liste d'inventaire —
#            lire des éléments, en ajouter, en retirer,
#            et afficher tout le contenu avec une boucle.
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici une liste de sorts magiques :

sorts = ["boule de feu", "éclair", "soin"]

print(f"Premier sort : {sorts[0]}")      # index 0 = premier
print(f"Dernier sort : {sorts[2]}")      # index 2 = troisième
sorts.append("téléportation")           # ajoute à la fin
retiré = sorts.pop()                    # retire le dernier
print(f"Sort retiré : {retiré}")

for i, sort in enumerate(sorts):
    print(f"  [{i}] {sort}")


# --- TON TOUR ---

# TODO 1 : Crée une liste appelée  inventaire  qui contient
#           au moins 4 objets de ton choix (armes, potions, etc.)


# TODO 2 : Affiche le premier objet et le dernier objet de ta liste
#           en utilisant leur index.
#           (Rappel : le dernier index = len(inventaire) - 1)


# TODO 3 : Ajoute un nouvel objet à la fin de ta liste avec append().
#           Affiche ensuite un message qui dit combien d'objets
#           il y a maintenant (utilise len()).


# TODO 4 : Retire le dernier objet avec pop() et stocke-le dans une
#           variable. Affiche quel objet a été retiré.


# TODO 5 : Affiche tout l'inventaire final avec une boucle for
#           et enumerate() pour numéroter chaque ligne.
#           Résultat attendu (exemple) :
#             Inventaire final :
#             [0] épée
#             [1] bouclier
#             [2] potion


if __name__ == "__main__":
    from tests import tester_ex01
    tester_ex01()
