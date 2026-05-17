# ============================================================
# tests.py — Leçon 03
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
# Exercice 01 — La table de multiplication
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
    print("🧪 Tests — Exercice 01 : Table de multiplication")
    print("─" * 42)

    source = _lire_source("exercice_01.py")
    sortie_cap = io.StringIO()

    # Simulation : n = 7
    try:
        with patch("builtins.input", side_effect=["7"]):
            with patch("sys.stdout", new=sortie_cap):
                import exercice_01 as ex1
    except StopIteration:
        print("  ⛔ Le programme a appelé input() trop de fois.")
        print("     Vérifie que tu as exactement un  input()  dans tes TODO.")
        return 0, 0
    except Exception as e:
        print(f"  ⛔ Erreur dans exercice_01.py : {e}")
        print("     Vérifie qu'il n'y a pas d'erreur de syntaxe.")
        return 0, 0

    # Ignorer les lignes de l'exemple
    lignes_eleve = [
        l for l in sortie_cap.getvalue().splitlines()
        if "Tour numéro" not in l
    ]
    sortie_eleve = "\n".join(lignes_eleve)

    # ── Variables ────────────────────────────────────────────
    v("Variable 'n' existe et vaut 7",
      hasattr(ex1, "n") and ex1.n == 7,
      "As-tu créé  n = int(input(...))  dans le TODO 1 ?",
      'Rappel : n = int(input("Donne un nombre : "))')

    # ── Sortie imprimée ──────────────────────────────────────
    v("La sortie contient '7' (le nombre choisi)",
      "7" in sortie_eleve,
      "As-tu affiché la variable  n  dans le TODO 2 ou 3 ?",
      "Le titre et les lignes de la table doivent afficher n.")

    v("La table va jusqu'à 7 × 10 = 70",
      "70" in sortie_eleve,
      "Ta boucle s'arrête-t-elle bien à 10 ?",
      "Utilise range(1, 11) pour aller de 1 à 10 inclus.")

    v("La table contient 10 lignes de résultats",
      len([l for l in lignes_eleve if any(c.isdigit() for c in l)
           and "===" not in l and "Table" not in l]) >= 10,
      "As-tu bien 10 tours dans ta boucle (de 1 à 10) ?",
      "Essaie range(1, 11) — range(1, 10) s'arrête à 9 !")

    # ── Structure : boucle ───────────────────────────────────
    v("TODO 3 — utilise une boucle 'for'",
      _apres_todo(source, 3, "for"),
      "As-tu écrit  for  dans le TODO 3 ?",
      "Structure : for i in range(1, 11):")

    v("TODO 3 — utilise 'range'",
      _apres_todo(source, 3, "range"),
      "As-tu utilisé  range()  dans ta boucle ?",
      "Exemple : for i in range(1, 11):")

    v("TODO 3 — calcule la multiplication avec n",
      _apres_todo(source, 3, "n") and (
          _apres_todo(source, 3, "n * i") or
          _apres_todo(source, 3, "n*i")  or
          _apres_todo(source, 3, "i * n") or
          _apres_todo(source, 3, "i*n")
      ),
      "As-tu calculé  n * i  à l'intérieur de la boucle ?",
      'Essaie : print(f"{n} × {i} = {n * i}")')

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Exercice 02 — Compte à rebours
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
    print("🧪 Tests — Exercice 02 : Compte à rebours")
    print("─" * 42)

    source = _lire_source("exercice_02.py")
    sortie_cap = io.StringIO()

    # Simulation : depart = 5
    try:
        with patch("builtins.input", side_effect=["5"]):
            with patch("sys.stdout", new=sortie_cap):
                import exercice_02 as ex2
    except StopIteration:
        print("  ⛔ Le programme a appelé input() trop de fois.")
        print("     Vérifie que tu as exactement un  input()  dans tes TODO.")
        return 0, 0
    except Exception as e:
        print(f"  ⛔ Erreur dans exercice_02.py : {e}")
        print("     Vérifie qu'il n'y a pas d'erreur de syntaxe.")
        return 0, 0

    # Ignorer les lignes de l'exemple
    lignes_eleve = [
        l for l in sortie_cap.getvalue().splitlines()
        if "vie" not in l.lower() and "game over" not in l.lower()
    ]
    sortie_eleve = "\n".join(lignes_eleve)

    # ── Variables ────────────────────────────────────────────
    v("Variable 'depart' existe et vaut 5",
      hasattr(ex2, "depart") and ex2.depart == 0,
      "As-tu créé  depart = int(input(...))  dans le TODO 1 ?",
      "La variable doit s'appeler exactement  depart  (sans accent).")

    # ── Sortie imprimée ──────────────────────────────────────
    v("La sortie contient '5' (premier nombre affiché)",
      "5" in sortie_eleve,
      "As-tu affiché  depart  dans le TODO 2 ?",
      'Essaie : print(depart)  ou  print(f"...")')

    v("La sortie contient '1' (dernier nombre avant décollage)",
      "1" in sortie_eleve,
      "Ta boucle s'arrête-t-elle quand depart vaut 0 ?",
      "La condition  depart > 0  affiche 1, puis s'arrête.")

    v("La sortie annonce le décollage",
      any(m in sortie_eleve for m in ["Décollage", "décollage", "🚀"]),
      "As-tu affiché un message de décollage dans le TODO 3 ?",
      'Essaie : print("🚀 Décollage !")  — en dehors de la boucle !')

    # ── Structure : while ────────────────────────────────────
    v("TODO 2 — utilise une boucle 'while'",
      _apres_todo(source, 2, "while"),
      "As-tu écrit  while  dans le TODO 2 ?",
      "Structure : while depart > 0:")

    v("TODO 2 — diminue 'depart' dans la boucle",
      _apres_todo(source, 2, "depart") and (
          _apres_todo(source, 2, "depart - 1") or
          _apres_todo(source, 2, "depart-1")   or
          _apres_todo(source, 2, "depart -= 1")
      ),
      "As-tu diminué  depart  à l'intérieur de la boucle ?",
      "Essaie : depart = depart - 1  (bien indenté sous le while !)")

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Correction finale — à rouler avec ton père
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   Correction finale — Leçon 03           ║")
    print("╚══════════════════════════════════════════╝")

    r1 = tester_ex1()
    r2 = tester_ex2()

    grand_total_r = r1[0] + r2[0]
    grand_total_t = r1[1] + r2[1]

    print()
    print("═" * 42)
    print(f"🏆 Total leçon 03 : {grand_total_r} / {grand_total_t} tests réussis")
    if grand_total_r == grand_total_t:
        print("   🎉 Leçon 03 complétée avec succès !")
    print()
