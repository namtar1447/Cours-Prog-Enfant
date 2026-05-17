# ============================================================
# tests.py — Leçon 01
# Roule ce fichier avec ton père pour la correction finale !
# (Chaque exercice se teste automatiquement quand tu le roules.)
# ============================================================

import sys, io, pathlib
from unittest.mock import patch


# ── Helpers ─────────────────────────────────────────────────

def _lire_source(nom_fichier):
    return (pathlib.Path(__file__).parent / nom_fichier).read_text(encoding="utf-8")


def _apres_todo(source, numero, *mots):
    """Vérifie que tous les mots apparaissent après # TODO <numero>."""
    marqueur = f"# TODO {numero}"
    if marqueur not in source:
        return False
    return all(m in source.split(marqueur)[-1] for m in mots)


def _resume(reussis, total):
    print()
    print("─" * 42)
    print(f"🏁 {reussis} / {total} tests réussis")
    if reussis == total:
        print("   🎉 Parfait ! Tous les tests sont au vert !")
    elif reussis >= total // 2:
        print("   💪 Bon travail ! Corrige les ❌ et relance !")
    else:
        print("   🔧 Continue ! Relis les indices et essaie de nouveau.")


# ════════════════════════════════════════════════════════════
# Exercice 01 — Fiche de héros
# ════════════════════════════════════════════════════════════

def tester_ex1():
    r = [0, 0]  # [réussis, total]

    def v(nom, cond, indice_1, indice_2):
        r[1] += 1
        if cond:
            print(f"  ✅ {nom}")
            r[0] += 1
        else:
            print(f"  ❌ {nom}")
            print(f"     💡 Indice : {indice_1}")
            print(f"        Si tu es encore bloqué : {indice_2}")
            print( "        Sinon, consulte CORRECTION.md avec ton père.")

    print()
    print("─" * 42)
    print("🧪 Tests — Exercice 01 : Fiche de héros")
    print("─" * 42)

    source = _lire_source("exercice_01.py")
    sortie_cap = io.StringIO()

    try:
        with patch("sys.stdout", new=sortie_cap):
            import exercice_01 as ex1
    except Exception as e:
        print(f"  ⛔ Erreur dans exercice_01.py : {e}")
        print("     Vérifie qu'il n'y a pas d'erreur de syntaxe.")
        return 0, 0

    # Ignorer la ligne de l'exemple pour les tests de sortie
    lignes_eleve = [
        l for l in sortie_cap.getvalue().splitlines()
        if "épée" not in l and "Arme" not in l
    ]
    sortie_eleve = "\n".join(lignes_eleve)

    # ── Variables ────────────────────────────────────────────
    v("Variable 'nom' existe et est du texte (str)",
      hasattr(ex1, "nom") and isinstance(ex1.nom, str) and len(ex1.nom) > 0,
      "As-tu créé une variable qui s'appelle exactement  nom  ?",
      'La valeur doit être du texte entre guillemets, ex. : nom = "Adam"')

    v("Variable 'age' existe et est un entier (int)",
      hasattr(ex1, "age") and isinstance(ex1.age, int),
      "As-tu créé une variable qui s'appelle exactement  age  ?",
      "La valeur doit être un entier sans guillemets, ex. : age = 9")

    v("Variable 'niveau' a bien été augmentée de 1 (TODO 5)",
      hasattr(ex1, "niveau") and isinstance(ex1.niveau, int) and ex1.niveau >= 2,
      "As-tu augmenté  niveau  de 1 après l'avoir créé ?",
      "Essaie :  niveau = niveau + 1  puis affiche le résultat avec print().")

    # ── Sortie imprimée ──────────────────────────────────────
    v("TODO 4 — la sortie contient ton vrai prénom",
      hasattr(ex1, "nom") and ex1.nom in sortie_eleve,
      "As-tu affiché la variable  nom  avec print() dans le TODO 4 ?",
      'Essaie : print(f"Héros : {nom} | ...")')

    v("TODO 4 — la sortie contient ton âge",
      hasattr(ex1, "age") and str(ex1.age) in sortie_eleve,
      "As-tu affiché la variable  age  avec print() dans le TODO 4 ?",
      'Assure-toi que  age  apparaît dans ta f-string : f"... Âge : {age} ..."')

    v("TODO 5 — la sortie mentionne le nouveau niveau",
      any(str(n) in sortie_eleve for n in range(2, 20))
      and any(m in sortie_eleve.lower() for m in ["niveau", "level"]),
      "As-tu affiché le nouveau niveau avec print() dans le TODO 5 ?",
      'Essaie : print(f"Nouveau niveau : {niveau}")')

    # ── Qualité : variables utilisées dans les f-strings ────
    v("TODO 4 — utilise {nom} dans la f-string (pas de valeur écrite en dur)",
      _apres_todo(source, 4, "{nom}"),
      "Dans le TODO 4, utilise la variable dans la f-string : {nom}",
      'Écrire "Adam" directement ne se mettra pas à jour si le nom change !')

    v("TODO 4 — utilise {age} dans la f-string (pas de valeur écrite en dur)",
      _apres_todo(source, 4, "{age}"),
      "Dans le TODO 4, insère la variable age dans la f-string : {age}",
      'Exemple complet : print(f"Héros : {nom} | Âge : {age} | Niveau : {niveau}")')

    v("TODO 5 — utilise la variable niveau dans le print (pas de chiffre en dur)",
      _apres_todo(source, 5, "{niveau}"),
      "Dans le TODO 5, affiche la variable, pas le chiffre 2 directement.",
      'Essaie : print(f"Nouveau niveau : {niveau}")  — avec les accolades !')

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Exercice 02 — Mini-calculatrice
# ════════════════════════════════════════════════════════════

def tester_ex2():
    r = [0, 0]

    def v(nom, cond, indice_1, indice_2):
        r[1] += 1
        if cond:
            print(f"  ✅ {nom}")
            r[0] += 1
        else:
            print(f"  ❌ {nom}")
            print(f"     💡 Indice : {indice_1}")
            print(f"        Si tu es encore bloqué : {indice_2}")
            print( "        Sinon, consulte CORRECTION.md avec ton père.")

    print()
    print("─" * 42)
    print("🧪 Tests — Exercice 02 : Mini-calculatrice")
    print("─" * 42)

    # Simulation : exemple reçoit "4", a reçoit "10", b reçoit "3"
    try:
        with patch("builtins.input", side_effect=["4", "10", "3"]):
            with patch("sys.stdout", new_callable=io.StringIO):
                import exercice_02 as ex2
    except StopIteration:
        print("  ⛔ Le programme a appelé input() trop de fois.")
        print("     Vérifie que tu as exactement deux  input()  dans tes TODO.")
        return 0, 0
    except Exception as e:
        print(f"  ⛔ Erreur dans exercice_02.py : {e}")
        print("     Vérifie qu'il n'y a pas d'erreur de syntaxe.")
        return 0, 0

    v("Variable 'a' existe et vaut 10",
      hasattr(ex2, "a") and ex2.a == 10,
      "As-tu créé une variable  a  avec int(input(...)) ?",
      'Rappel : a = int(input("Premier nombre : "))')

    v("Variable 'b' existe et vaut 3",
      hasattr(ex2, "b") and ex2.b == 3,
      "As-tu créé une variable  b  avec int(input(...)) ?",
      'Rappel : b = int(input("Deuxième nombre : "))')

    v("Variable 'somme' vaut 13  (10 + 3)",
      hasattr(ex2, "somme") and ex2.somme == 13,
      "As-tu calculé  somme = a + b  ?",
      "Vérifie que tu utilises + et que a et b sont bien des int.")

    v("Variable 'difference' vaut 7  (10 - 3)",
      hasattr(ex2, "difference") and ex2.difference == 7,
      "As-tu calculé  difference = a - b  ?",
      "Utilise le signe moins : difference = a - b")

    v("Variable 'produit' vaut 30  (10 * 3)",
      hasattr(ex2, "produit") and ex2.produit == 30,
      "As-tu calculé  produit = a * b  ?",
      "Utilise l'étoile pour multiplier : produit = a * b")

    v("Variable 'quotient' vaut 3  (10 // 3)",
      hasattr(ex2, "quotient") and ex2.quotient == 3,
      "As-tu calculé  quotient = a // b  ?",
      "Utilise // pour la division entière : quotient = a // b")

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Correction finale — à rouler avec ton père
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   Correction finale — Leçon 01           ║")
    print("╚══════════════════════════════════════════╝")

    r1 = tester_ex1()
    r2 = tester_ex2()

    grand_total_r = r1[0] + r2[0]
    grand_total_t = r1[1] + r2[1]

    print()
    print("═" * 42)
    print(f"🏆 Total leçon 01 : {grand_total_r} / {grand_total_t} tests réussis")
    if grand_total_r == grand_total_t:
        print("   🎉 Leçon 01 complétée avec succès !")
    print()
