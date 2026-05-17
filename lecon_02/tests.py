# ============================================================
# tests.py — Leçon 02
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
# Exercice 01 — Division sans catastrophe
# ════════════════════════════════════════════════════════════

def tester_ex1():
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
    print("🧪 Tests — Exercice 01 : Division sans catastrophe")
    print("─" * 42)

    source = _lire_source("exercice_01.py")
    sortie_cap = io.StringIO()

    # Simulation : a = 10, b = 2  (cas normal, division possible)
    try:
        with patch("builtins.input", side_effect=["10", "2"]):
            with patch("sys.stdout", new=sortie_cap):
                import exercice_01 as ex1
    except StopIteration:
        print("  ⛔ Le programme a appelé input() trop de fois.")
        print("     Vérifie que tu as exactement deux  input()  dans tes TODO.")
        return 0, 0
    except Exception as e:
        print(f"  ⛔ Erreur dans exercice_01.py : {e}")
        print("     Vérifie qu'il n'y a pas d'erreur de syntaxe.")
        return 0, 0

    sortie_eleve = sortie_cap.getvalue()

    # ── Variables ────────────────────────────────────────────
    v("Variable 'a' existe et vaut 10",
      hasattr(ex1, "a") and ex1.a == 10,
      "As-tu créé  a = int(input(...))  dans le TODO 1 ?",
      'Rappel : a = int(input("Premier nombre : "))')

    v("Variable 'b' existe et vaut 2",
      hasattr(ex1, "b") and ex1.b == 2,
      "As-tu créé  b = int(input(...))  dans le TODO 2 ?",
      'Rappel : b = int(input("Deuxième nombre : "))')

    # ── Sortie imprimée ──────────────────────────────────────
    v("La division 10 / 2 apparaît dans la sortie (= 5)",
      "5" in sortie_eleve,
      "As-tu affiché le résultat de a / b dans le TODO 4 ?",
      'Essaie : print(f"{a} / {b} = {a / b}")')

    # ── Structure : conditions ───────────────────────────────
    v("TODO 3 — vérifie si b == 0 avec un 'if'",
      _apres_todo(source, 3, "if") and _apres_todo(source, 3, "== 0"),
      "As-tu écrit  if b == 0:  dans le TODO 3 ?",
      "Essaie exactement : if b == 0:")

    v("Utilise 'else' pour la division (cas b != 0)",
      _apres_todo(source, 3, "else"),
      "Après le if b == 0, as-tu ajouté un  else  pour diviser ?",
      "Structure : if b == 0:\n    print(\"Erreur\")\nelse:\n    print(a / b)")

    v("Calcule a / b dans le else",
      _apres_todo(source, 3, "a / b") or _apres_todo(source, 3, "a/b")
      or _apres_todo(source, 4, "a / b") or _apres_todo(source, 4, "a/b"),
      "As-tu calculé  a / b  dans la partie else ?",
      'Essaie : print(f"{a} / {b} = {a / b}")')

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Exercice 02 — Calculatrice à choix
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
    print("🧪 Tests — Exercice 02 : Calculatrice à choix")
    print("─" * 42)

    source = _lire_source("exercice_02.py")
    sortie_cap = io.StringIO()

    # Simulation : a=20, b=4, op="/"  →  20 / 4 = 5.0
    try:
        with patch("builtins.input", side_effect=["20", "4", "/"]):
            with patch("sys.stdout", new=sortie_cap):
                import exercice_02 as ex2
    except StopIteration:
        print("  ⛔ Le programme a appelé input() trop de fois.")
        print("     Vérifie que tu as exactement trois  input()  : a, b, et op.")
        return 0, 0
    except Exception as e:
        print(f"  ⛔ Erreur dans exercice_02.py : {e}")
        print("     Vérifie qu'il n'y a pas d'erreur de syntaxe.")
        return 0, 0

    sortie_eleve = sortie_cap.getvalue()

    # ── Variables ────────────────────────────────────────────
    v("Variable 'a' existe et vaut 20",
      hasattr(ex2, "a") and ex2.a == 20,
      "As-tu créé  a = int(input(...))  dans le TODO 1 ?",
      'Rappel : a = int(input("Premier nombre : "))')

    v("Variable 'b' existe et vaut 4",
      hasattr(ex2, "b") and ex2.b == 4,
      "As-tu créé  b = int(input(...))  dans le TODO 1 ?",
      'Rappel : b = int(input("Deuxième nombre : "))')

    v("Variable 'op' existe",
      hasattr(ex2, "op"),
      "As-tu créé une variable  op  pour l'opération dans le TODO 2 ?",
      'Essaie : op = input("Opération (+, -, *, /) : ")')

    # ── Sortie imprimée ──────────────────────────────────────
    v("La division 20 / 4 apparaît dans la sortie (= 5)",
      "5" in sortie_eleve,
      "Avec op='/', le résultat de 20 / 4 doit s'afficher.",
      'Dans ton elif op == "/": essaie print(f"{a} / {b} = {a / b}")')

    # ── Structure : conditions ───────────────────────────────
    v("TODO 3 — utilise 'elif' pour les différentes opérations",
      _apres_todo(source, 3, "elif"),
      "As-tu utilisé  elif  pour les cas -, * et / ?",
      'Structure : if op == "+": ... elif op == "-": ... elif op == "*": ...')

    v("TODO 3 — vérifie la division par zéro dans le cas '/'",
      _apres_todo(source, 3, "== 0"),
      "Dans le cas '/', as-tu vérifié si b == 0 avant de diviser ?",
      'Dans ton elif op == "/": ajoute if b == 0: print("Erreur !") else: ...')

    v("TODO 3 — gère les opérations inconnues avec 'else'",
      _apres_todo(source, 3, "else"),
      "As-tu ajouté un  else  final pour les opérations inconnues ?",
      'À la fin de tes elif, ajoute : else: print("Opération inconnue !")')

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Correction finale — à rouler avec ton père
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   Correction finale — Leçon 02           ║")
    print("╚══════════════════════════════════════════╝")

    r1 = tester_ex1()
    r2 = tester_ex2()

    grand_total_r = r1[0] + r2[0]
    grand_total_t = r1[1] + r2[1]

    print()
    print("═" * 42)
    print(f"🏆 Total leçon 02 : {grand_total_r} / {grand_total_t} tests réussis")
    if grand_total_r == grand_total_t:
        print("   🎉 Leçon 02 complétée avec succès !")
    print()
