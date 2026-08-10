# ============================================================
# tests.py — Leçon 06b
# Roule ce fichier avec ton père pour la correction finale !
# (Chaque module se teste aussi tout seul quand tu le roules.)
# ============================================================

import sys

try:                       # pour que les ✅ s'affichent aussi hors de Thonny
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

from mpmath import mp, mpf

mp.dps = 30


def _verificateur(compteur):
    """Fabrique la fonction v() qui note un test et donne deux indices."""

    def v(nom, condition, indice_1, indice_2):
        compteur[1] += 1

        try:
            reussi = bool(condition())
        except Exception as e:
            reussi = False
            nom = f"{nom}   ({type(e).__name__}: {e})"

        if reussi:
            print(f"  ✅ {nom}")
            compteur[0] += 1
        else:
            print(f"  ❌ {nom}")
            print(f"     💡 Indice : {indice_1}")
            print(f"        Si tu es encore bloqué : {indice_2}")
            print(f"        Sinon, consulte CORRECTION.md avec ton père.")

    return v


def _resume(reussis, total):
    print(f"\n🏁 {reussis} / {total} tests réussis")

    if reussis == total:
        print("   🎉 Parfait ! Lance projet.py — c'est TON code qui calcule.")
    elif reussis >= total * 0.6:
        print("   💪 Bien parti ! Relis les indices ci-dessus.")
    else:
        print("   🔍 Reprends un TODO à la fois, du premier au dernier.")


# ============================================================
# mes_operations.py
# ============================================================

def tester_operations():
    print("\n🔢 mes_operations.py")
    r = [0, 0]
    v = _verificateur(r)

    import mes_operations as ops

    # --- TODO 1 : puissance ---
    v("puissance(2, 10) donne 1024",
      lambda: ops.puissance(mpf(2), mpf(10)) == 1024,
      "'à la puissance' s'écrit avec deux étoiles en Python",
      "return base ** exposant, après le garde-fou déjà écrit")

    v("puissance(2, 0) donne 1",
      lambda: ops.puissance(mpf(2), mpf(0)) == 1,
      "n'importe quel nombre à la puissance 0 vaut 1",
      "Python le fait tout seul — si ça rate, ta fonction ne renvoie rien")

    v("puissance refuse un exposant démesuré",
      lambda: _leve(ValueError, ops.puissance, mpf(2), mpf(10) ** 20),
      "le garde-fou verifier_exposant est fourni au-dessus",
      "il doit être appelé AVANT le calcul, pas après")

    # --- TODO 2 : racine_carree ---
    v("racine_carree(16) donne 4",
      lambda: ops.racine_carree(mpf(16)) == 4,
      "regarde la boîte à outils en haut du fichier",
      "mpmath a une fonction dont le nom veut dire 'square root'")

    v("racine_carree(2) garde toutes les décimales",
      lambda: str(ops.racine_carree(mpf(2)))[:12] == "1.4142135623",
      "utilise la fonction de mpmath, pas celle de math",
      "math.sqrt n'a que 15 décimales — mpmath.sqrt suit mp.dps")

    # --- TODO 3 : racine_nieme ---
    v("racine_nieme(8, 3) donne 2",
      lambda: ops.racine_nieme(mpf(8), mpf(3)) == 2,
      "il existe une fonction mpmath pour la racine k-ième",
      "mpmath.root(nombre, indice) — mais l'indice doit être un entier")

    v("racine_nieme(81, 4) donne 3",
      lambda: ops.racine_nieme(mpf(81), mpf(4)) == 3,
      "3×3×3×3 = 81",
      "si ça plante avec un TypeError, entoure l'indice de int(...)")

    # --- TODO 4 : factorielle ---
    v("factorielle(5) donne 120",
      lambda: ops.factorielle(mpf(5)) == 120,
      "5! = 5×4×3×2×1",
      "mpmath sait déjà le faire — regarde la boîte à outils")

    v("factorielle(0) donne 1",
      lambda: ops.factorielle(mpf(0)) == 1,
      "par convention, 0! vaut 1",
      "mpmath.factorial le sait déjà — si ça rate, tu l'as écrite à la main")

    v("factorielle(100) est un nombre géant",
      lambda: ops.factorielle(mpf(100)) > mpf(10) ** 150,
      "100! a 158 chiffres, comme à la leçon 06",
      "si le résultat est faux, tu as peut-être écrit une boucle incomplète")

    # --- TODO 5 : tetration ---
    v("tetration(2, 3) donne 16",
      lambda: ops.tetration(mpf(2), mpf(3)) == 16,
      "2↑↑3 = 2^(2^2) = 2^4",
      "commence à 1, puis répète hauteur fois : resultat = puissance(base, resultat)")

    v("tetration(2, 4) donne 65536",
      lambda: ops.tetration(mpf(2), mpf(4)) == 65536,
      "un étage de plus que le test précédent",
      "2^(2^(2^2)) = 2^16")

    v("tetration(2, 0) donne 1",
      lambda: ops.tetration(mpf(2), mpf(0)) == 1,
      "une tour de zéro étage vaut 1",
      "si tu pars de resultat = base au lieu de 1, ce test rate")

    v("tetration(3, 3) donne 7625597484987",
      lambda: ops.tetration(mpf(3), mpf(3)) == 7625597484987,
      "3^(3^3) = 3^27",
      "le même code doit marcher pour n'importe quelle base")

    v("tetration passe par TA fonction puissance",
      lambda: _compte_appels(ops) >= 2,
      "chaque étage de la tour est une puissance",
      "écris puissance(base, resultat), pas base ** resultat — "
      "sinon le garde-fou saute et 2↑↑6 fige l'ordinateur")

    _resume(r[0], r[1])
    return r[0], r[1]


# ============================================================
# mon_historique.py
# ============================================================

def tester_historique():
    print("\n📜 mon_historique.py")
    r = [0, 0]
    v = _verificateur(r)

    import mon_historique as h

    # --- TODO 1 : noter ---
    v("noter ajoute un calcul à la liste",
      lambda: _apres_noter(h, [])[0] is not None,
      "une liste s'agrandit avec .append(...)",
      "historique.append({...}) — le dictionnaire a deux clés")

    v("le calcul noté a les clés 'expression' et 'resultat'",
      lambda: _apres_noter(h, [])[0] == {"expression": "12+3", "resultat": "15"},
      "reprends exactement la forme de l'EXEMPLE en haut du fichier",
      "{'expression': expression, 'resultat': resultat}")

    v("noter modifie la liste reçue, il n'en crée pas une nouvelle",
      lambda: _modifie_sur_place(h),
      "la calculatrice et le panneau se partagent la même liste",
      "historique = [...] fabrique une autre liste ; .append() modifie celle-là")

    v("noter garde l'ordre : deux calculs, le plus récent à la fin",
      lambda: _deux_calculs(h)[-1]["expression"] == "2↑↑4",
      ".append ajoute toujours à la fin",
      "n'inverse rien dans noter — c'est le rôle de du_plus_recent")

    # --- TODO 2 : dernier ---
    v("dernier([]) renvoie None, mais pas dernier d'une liste pleine",
      lambda: h.dernier([]) is None and h.dernier(_deux_calculs(h)) is not None,
      "au tout premier démarrage, l'historique est vide",
      "teste si la liste est vide AVANT d'aller chercher le dernier élément")

    v("dernier renvoie bien le calcul le plus récent",
      lambda: h.dernier(_deux_calculs(h))["resultat"] == "65536",
      "le dernier élément d'une liste porte l'indice -1",
      "return historique[-1], mais seulement si la liste n'est pas vide")

    # --- TODO 3 : du_plus_recent ---
    v("du_plus_recent inverse l'ordre",
      lambda: h.du_plus_recent(_deux_calculs(h))[0]["expression"] == "2↑↑4",
      "le plus récent doit arriver en premier",
      "list(reversed(historique)) ou historique[::-1]")

    v("du_plus_recent ne modifie PAS l'historique original",
      lambda: _ne_touche_pas(h),
      "la méthode .reverse() retourne la liste elle-même — piège !",
      "list(reversed(...)) fabrique une copie, .reverse() abîme l'original")

    v("du_plus_recent d'une liste vide renvoie une liste vide",
      lambda: list(h.du_plus_recent([])) == [],
      "aucun cas spécial à écrire, ça marche tout seul",
      "si ça rate, ta fonction ne renvoie rien")

    # --- TODO 4 : MESSAGES ---
    v("MESSAGES contient 'ZeroDivisionError'",
      lambda: "ZeroDivisionError" in h.MESSAGES,
      "un dictionnaire associe une clé à une valeur",
      "MESSAGES = {'ZeroDivisionError': '❌ …', 'ValueError': '❌ …'}")

    v("MESSAGES contient 'ValueError'",
      lambda: "ValueError" in h.MESSAGES,
      "il faut les deux noms d'erreur",
      "la clé s'écrit exactement comme Python l'écrit, majuscules comprises")

    v("les messages commencent par ❌ et parlent français",
      lambda: len(h.MESSAGES) >= 2 and all(str(m).startswith("❌") and len(str(m)) > 5
                                           for m in h.MESSAGES.values()),
      "le ❌ rend l'erreur visible sur l'écran de la calculatrice",
      "copie-colle le ❌ depuis cette ligne si ton clavier ne le fait pas")

    # --- TODO 5 : message_pour ---
    v("message_pour('ZeroDivisionError') renvoie ton message",
      lambda: h.message_pour("ZeroDivisionError") == h.MESSAGES["ZeroDivisionError"],
      "va chercher dans le dictionnaire MESSAGES",
      "MESSAGES[nom_erreur] — mais attention au cas où la clé n'existe pas")

    v("message_pour d'une erreur inconnue ne plante pas",
      lambda: isinstance(h.message_pour("ErreurJamaisVue"), str)
              and len(h.message_pour("ErreurJamaisVue")) > 0,
      "MESSAGES['clé inconnue'] déclenche une KeyError",
      "MESSAGES.get(nom_erreur, 'message par défaut') ne plante jamais")

    _resume(r[0], r[1])
    return r[0], r[1]


# ============================================================
# Petits outils pour les tests
# ============================================================

def _leve(erreur, fonction, *args):
    """Vrai si la fonction lève bien l'erreur attendue."""
    try:
        fonction(*args)
    except erreur:
        return True
    except Exception:
        return False

    return False


def _compte_appels(ops):
    """Compte combien de fois tetration passe par puissance."""
    vraie = ops.puissance
    appels = [0]

    def espion(base, exposant):
        appels[0] += 1
        return vraie(base, exposant)

    ops.puissance = espion

    try:
        ops.tetration(mpf(2), mpf(3))
    except Exception:
        pass
    finally:
        ops.puissance = vraie

    return appels[0]


def _apres_noter(h, liste):
    h.noter(liste, "12+3", "15")
    return liste or [None]


def _deux_calculs(h):
    liste = []
    h.noter(liste, "12+3", "15")
    h.noter(liste, "2↑↑4", "65536")
    return liste


def _modifie_sur_place(h):
    liste = []
    h.noter(liste, "12+3", "15")
    return len(liste) == 1


def _ne_touche_pas(h):
    liste = _deux_calculs(h)
    avant = [dict(c) for c in liste]
    renvoye = h.du_plus_recent(liste)

    if renvoye is None or len(list(renvoye)) != len(avant):
        return False

    return liste == avant


# ============================================================
# Correction finale : les deux modules + grand total
# ============================================================

if __name__ == "__main__":
    r1 = tester_operations()
    r2 = tester_historique()

    print(f"\n🏆 Total : {r1[0] + r2[0]} / {r1[1] + r2[1]}")

    if r1[0] + r2[0] == r1[1] + r2[1]:
        print("   Lance projet.py — ta calculatrice est complète !")
