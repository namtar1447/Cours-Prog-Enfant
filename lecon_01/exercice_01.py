# ============================================================
# Leçon 01 — Variables, types et premiers programmes
# Exercice 01 — Ma fiche de héros  (guidé)
# ============================================================
# OBJECTIF : Crée ta propre fiche de personnage RPG en Python !
#            Tu vas créer des variables de différents types
#            et les afficher avec print().
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici comment créer des variables de types différents :

arme   = "épée"        # str  — texte entre guillemets
degats = 5             # int  — nombre entier
critique = True        # bool — vrai ou faux

print(f"Arme : {arme} | Dégâts : {degats} | Critique : {critique}")
# affiche : Arme : épée | Dégâts : 5 | Critique : True


# --- TON TOUR ---

# TODO 1 : Crée une variable appelée  nom  qui contient ton prénom.
#           Ce doit être du texte (str) — n'oublie pas les guillemets !

# TODO 2 : Crée une variable appelée  age  qui contient ton âge.
#           Ce doit être un nombre entier (int) — sans guillemets.

# TODO 3 : Crée une variable appelée  niveau  qui vaut 1.
#           C'est le niveau de départ de ton héros.

# TODO 4 : Affiche une phrase de présentation avec print() et une f-string.
#           Le résultat doit ressembler à (avec tes vraies valeurs) :
#           Héros : Adam | Âge : 9 | Niveau : 1

# TODO 5 : Ton héros monte de niveau !
#           Augmente la variable  niveau  de 1, puis affiche le nouveau niveau.
#           Le résultat doit ressembler à :
#           Nouveau niveau : 2


if __name__ == "__main__":
    from tests import tester_ex1
    tester_ex1()
