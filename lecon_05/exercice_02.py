# ============================================================
# Leçon 05 — Listes et dictionnaires
# Exercice 02 — La fiche de héros  (semi-guidé)
# ============================================================
# OBJECTIF : Créer la fiche d'un héros avec un dictionnaire,
#            simuler des événements de combat, et enregistrer
#            tout dans un journal (une liste).
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici comment modifier un dictionnaire et enregistrer dans une liste :

monstre = {"nom": "Gobelin", "pv": 30, "force": 8}
journal_exemple = []

monstre["pv"] = monstre["pv"] - 10          # le héros attaque
journal_exemple.append("Gobelin perd 10 pv")

print(f"PV du monstre : {monstre['pv']}")
for entree in journal_exemple:
    print(f"  📜 {entree}")


# --- TON TOUR ---

# TODO 1 : Crée un dictionnaire appelé  heros  avec au moins
#           ces 4 clés : "nom", "pv", "force", "niveau"
#           Donne-lui les valeurs de ton choix.


# TODO 2 : Crée une liste vide appelée  journal.
#           Affiche la fiche de ton héros en lisant chaque
#           valeur du dictionnaire avec ses clés.
#           Exemple :
#             ⚔️  Nom    : Arthur
#             ❤️  PV     : 100
#             💪  Force  : 42
#             ⭐  Niveau : 5


# TODO 3 : Simule une attaque ennemie qui réduit les pv du héros
#           d'une valeur de ton choix (entre 10 et 30).
#           Enregistre l'événement dans  journal  avec append().
#           Affiche les nouveaux pv.
#           Exemple :
#             💥 Attaque ! Arthur perd 15 pv → il lui reste 85 pv


# TODO 4 : Simule un soin qui augmente les pv du héros.
#           Enregistre l'événement dans  journal  avec append().
#           Affiche les nouveaux pv.


# TODO 5 : Affiche tout le journal en parcourant la liste avec une boucle.
#           Exemple :
#             📜 Journal de combat :
#             [1] Arthur perd 15 pv → il lui reste 85 pv
#             [2] Arthur récupère 20 pv → il lui reste 105 pv


if __name__ == "__main__":
    from tests import tester_ex02
    tester_ex02()
