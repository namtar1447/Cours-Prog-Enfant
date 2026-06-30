# ============================================================
# Leçon 06 — Modules et mpmath
# Exercice 02 — Tétration  (semi-guidé)
# ============================================================
# OBJECTIF : Programmer la tétration — l'opération mathématique
#            qui dépasse les puissances — et observer des nombres
#            qui grandissent de façon explosive.
#
# COMMENT TESTER : Clique sur ▶
# ============================================================


# --- EXEMPLE (ne pas modifier) ---
# La tétration : a↑↑b = a^(a^(a^...)) b fois
# Exemple : 2↑↑3 = 2^(2^2) = 2^4 = 16

def tetration(a, b):
    """Calcule a↑↑b de façon récursive."""
    if b == 0:
        return 1
    if b == 1:
        return a
    return a ** tetration(a, b - 1)

print(f"2↑↑1 = {tetration(2, 1)}")   # 2
print(f"2↑↑2 = {tetration(2, 2)}")   # 4
print(f"2↑↑3 = {tetration(2, 3)}")   # 16
print(f"2↑↑4 = {tetration(2, 4)}")   # 65536


# --- TON TOUR ---

# TODO 1 : Affiche les résultats de 2↑↑1 à 2↑↑5 dans une boucle.
#           Pour chaque résultat, affiche aussi le nombre de chiffres.
#           Format : "2↑↑4 = 65536   (5 chiffres)"
#
#           ⚠️  2↑↑5 a 19 728 chiffres — affiche seulement le compte,
#               pas le nombre complet !
#               (Astuce : if len(str(r)) > 20: affiche juste le compte)


# TODO 2 : Fais la même chose pour 3↑↑1 à 3↑↑3.
#           ⚠️  Ne calcule pas 3↑↑4 — ce serait un nombre avec
#               des milliards de milliards de chiffres !


# TODO 3 : Trouve le plus petit b tel que 2↑↑b dépasse 1 000 000.
#           Utilise une boucle while qui essaie b = 1, 2, 3…
#           Affiche : "2↑↑b dépasse 1 000 000 pour b = X"


# TODO 4 : Calcule la somme de tous les chiffres de 2↑↑4 (= 65536).
#           Parcours chaque caractère de str(65536) avec une boucle,
#           convertis-le en int, et additionne.
#           Affiche : "Somme des chiffres de 65536 = X"


if __name__ == "__main__":
    from tests import tester_ex02
    tester_ex02()
