# ============================================================
# Leçon 01 — Variables, types et premiers programmes
# Exercice 02 — Mini-calculatrice  (semi-guidé)
# ============================================================
# OBJECTIF : Crée une calculatrice qui demande deux nombres
#            à l'utilisateur et affiche plusieurs résultats.
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# Voici comment demander un nombre entier et l'utiliser :

exemple = int(input("Donne-moi un nombre : "))
print(f"Ton nombre au carré : {exemple ** 2}")
# Si tu tapes 4 → affiche : Ton nombre au carré : 16


# --- TON TOUR ---

# TODO 1 : Demande un premier nombre entier à l'utilisateur.
#           Stocke-le dans une variable appelée  a .
#           N'oublie pas de convertir avec int() !


# TODO 2 : Demande un deuxième nombre entier à l'utilisateur.
#           Stocke-le dans une variable appelée  b .


# TODO 3 : Calcule les quatre opérations de base et stocke chaque résultat :
#             somme     = a + b
#             difference = a - b
#             produit   = a * b
#           Pour la division, utilise une variable appelée  quotient .
#           Attention : / donne un float, // donne un int — choisis // ici.


# TODO 4 : Affiche les quatre résultats avec des f-strings.
#           Le résultat doit ressembler à (si l'utilisateur tape 10 puis 3) :
#           10 + 3 = 13
#           10 - 3 = 7
#           10 * 3 = 30
#           10 // 3 = 3


if __name__ == "__main__":
    from tests import tester_ex2
    tester_ex2()
