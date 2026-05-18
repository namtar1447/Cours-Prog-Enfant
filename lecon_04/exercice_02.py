# ============================================================
# Leçon 04 — Fonctions, paramètres, return
# Exercice 02 — Calculatrice de formes géométriques  (semi-guidé)
# ============================================================
# OBJECTIF : Créer des fonctions pour calculer des aires,
#            puis demander à l'utilisateur quelle forme calculer
#            et appeler la bonne fonction avec ses dimensions.
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici comment demander un choix et appeler une fonction selon ce choix :

def saluer(prenom):
    return f"Bonjour, {prenom} !"

choix = input("Ton prénom : ")
message = saluer(choix)
print(message)


# --- TON TOUR ---

# TODO 1 : Crée une fonction aire_rectangle(longueur, largeur)
#           qui retourne l'aire d'un rectangle.
#           Rappel : aire = longueur × largeur
#           Exemple : aire_rectangle(5, 3) → retourne 15


# TODO 2 : Crée une fonction aire_triangle(base, hauteur)
#           qui retourne l'aire d'un triangle.
#           Rappel : aire = base × hauteur ÷ 2
#           Exemple : aire_triangle(4, 6) → retourne 12.0


# TODO 3 : Crée une fonction aire_carre(cote)
#           qui retourne l'aire d'un carré.
#           Rappel : aire = côté × côté
#           Exemple : aire_carre(7) → retourne 49


# TODO 4 : Demande à l'utilisateur quelle forme il veut calculer
#           (rectangle, triangle ou carre), puis demande les dimensions
#           nécessaires, appelle la bonne fonction et affiche le résultat.
#           Exemple de ce que l'utilisateur devrait voir :
#
#             Quelle forme ? (rectangle / triangle / carre) : rectangle
#             Longueur : 5
#             Largeur : 3
#             Aire du rectangle : 15
#
#           Indice : utilise if / elif / else pour choisir la bonne fonction.


if __name__ == "__main__":
    from tests import tester_ex02
    tester_ex02()
