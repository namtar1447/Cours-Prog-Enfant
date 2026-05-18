# ============================================================
# tests.py — Leçon 04
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
# Exercice 01 — Mes premières fonctions mathématiques
# ════════════════════════════════════════════════════════════

def tester_ex01():
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
    print("🧪 Tests — Exercice 01 : Fonctions mathématiques")
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

    sortie = sortie_cap.getvalue()

    # ── Fonction doubler ─────────────────────────────────────
    v("La fonction doubler() existe",
      callable(getattr(ex1, "doubler", None)),
      "As-tu écrit  def doubler(n):  dans le TODO 1 ?",
      "Structure : def doubler(n):  puis sur la ligne suivante indentée : return n * 2")

    v("doubler(5) retourne 10",
      getattr(ex1, "doubler", lambda x: None)(5) == 10,
      "Ta fonction doubler retourne-t-elle n * 2 ?",
      "Assure-toi d'avoir  return n * 2  (et non print).")

    v("doubler(0) retourne 0",
      getattr(ex1, "doubler", lambda x: None)(0) == 0,
      "doubler(0) devrait retourner 0 — vérifie ta formule.",
      "return n * 2  →  0 * 2 = 0")

    # ── Fonction carre ───────────────────────────────────────
    v("La fonction carre() existe",
      callable(getattr(ex1, "carre", None)),
      "As-tu écrit  def carre(n):  dans le TODO 2 ?",
      "Structure : def carre(n):  puis  return n * n")

    v("carre(4) retourne 16",
      getattr(ex1, "carre", lambda x: None)(4) == 16,
      "carre(4) devrait retourner 16 — as-tu utilisé  n * n ?",
      "return n * n  →  4 * 4 = 16")

    v("carre(9) retourne 81",
      getattr(ex1, "carre", lambda x: None)(9) == 81,
      "carre(9) devrait retourner 81.",
      "return n * n  →  9 * 9 = 81")

    # ── Fonction perimetre_rectangle ─────────────────────────
    v("La fonction perimetre_rectangle() existe",
      callable(getattr(ex1, "perimetre_rectangle", None)),
      "As-tu écrit  def perimetre_rectangle(longueur, largeur):  dans le TODO 3 ?",
      "N'oublie pas les deux paramètres : longueur et largeur.")

    fn_pr = getattr(ex1, "perimetre_rectangle", lambda a, b: None)
    v("perimetre_rectangle(5, 3) retourne 16",
      fn_pr(5, 3) == 16,
      "Périmètre = 2 × longueur + 2 × largeur — as-tu utilisé cette formule ?",
      "return 2 * longueur + 2 * largeur  →  2*5 + 2*3 = 16")

    v("perimetre_rectangle(10, 4) retourne 28",
      fn_pr(10, 4) == 28,
      "Vérifie ta formule avec d'autres valeurs.",
      "2 * 10 + 2 * 4 = 28")

    # ── Structure du code ────────────────────────────────────
    v("TODO 1 — utilise def et return",
      _apres_todo(source, 1, "def") and _apres_todo(source, 1, "return"),
      "As-tu bien utilisé  def  et  return  dans le TODO 1 ?",
      "Structure : def doubler(n):  /  (indenté) return n * 2")

    v("TODO 4 — affiche quelque chose avec print",
      _apres_todo(source, 4, "print"),
      "As-tu utilisé print() dans le TODO 4 pour afficher les résultats ?",
      'Exemple : print(f"Le double de 6 = {doubler(6)}")')

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Exercice 02 — Calculatrice de formes géométriques
# ════════════════════════════════════════════════════════════

def tester_ex02():
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
    print("🧪 Tests — Exercice 02 : Calculatrice de formes")
    print("─" * 42)

    source = _lire_source("exercice_02.py")

    # ── Test des fonctions sans input() ─────────────────────
    sortie_cap = io.StringIO()
    try:
        # On simule le prénom de l'exemple + le choix rectangle + dimensions
        with patch("builtins.input", side_effect=["Adam", "rectangle", "5", "3"]):
            with patch("sys.stdout", new=sortie_cap):
                import exercice_02 as ex2
    except StopIteration:
        print("  ⛔ Le programme a appelé input() plus de fois qu'attendu.")
        print("     Vérifie que tu as exactement 3 input() dans tes TODO.")
        return 0, 0
    except Exception as e:
        print(f"  ⛔ Erreur dans exercice_02.py : {e}")
        print("     Vérifie qu'il n'y a pas d'erreur de syntaxe.")
        return 0, 0

    sortie = sortie_cap.getvalue()

    # ── Fonctions ────────────────────────────────────────────
    v("La fonction aire_rectangle() existe",
      callable(getattr(ex2, "aire_rectangle", None)),
      "As-tu écrit  def aire_rectangle(longueur, largeur):  dans le TODO 1 ?",
      "Structure : def aire_rectangle(longueur, largeur):  /  return longueur * largeur")

    fn_ar = getattr(ex2, "aire_rectangle", lambda a, b: None)
    v("aire_rectangle(5, 3) retourne 15",
      fn_ar(5, 3) == 15,
      "Aire du rectangle = longueur × largeur — as-tu utilisé cette formule ?",
      "return longueur * largeur  →  5 * 3 = 15")

    v("La fonction aire_triangle() existe",
      callable(getattr(ex2, "aire_triangle", None)),
      "As-tu écrit  def aire_triangle(base, hauteur):  dans le TODO 2 ?",
      "Structure : def aire_triangle(base, hauteur):  /  return base * hauteur / 2")

    fn_at = getattr(ex2, "aire_triangle", lambda a, b: None)
    v("aire_triangle(4, 6) retourne 12",
      fn_at(4, 6) == 12 or fn_at(4, 6) == 12.0,
      "Aire du triangle = base × hauteur ÷ 2 — as-tu divisé par 2 ?",
      "return base * hauteur / 2  →  4 * 6 / 2 = 12.0")

    v("La fonction aire_carre() existe",
      callable(getattr(ex2, "aire_carre", None)),
      "As-tu écrit  def aire_carre(cote):  dans le TODO 3 ?",
      "Structure : def aire_carre(cote):  /  return cote * cote")

    fn_ac = getattr(ex2, "aire_carre", None)
    v("aire_carre(7) retourne 49",
      fn_ac is not None and fn_ac(7) == 49,
      "Aire du carré = côté × côté — as-tu utilisé  cote * cote ?",
      "return cote * cote  →  7 * 7 = 49")

    # ── Sortie imprimée (simulation rectangle 5×3) ───────────
    v("La sortie affiche le résultat 15 (aire du rectangle 5×3)",
      "15" in sortie,
      "Ton programme affiche-t-il l'aire calculée dans le TODO 4 ?",
      'Exemple : print(f"Aire du rectangle : {aire_rectangle(longueur, largeur)}")')

    # ── Structure du code ────────────────────────────────────
    v("TODO 4 — utilise if ou elif pour choisir la forme",
      _apres_todo(source, 4, "if") or _apres_todo(source, 4, "elif"),
      "As-tu utilisé  if / elif  dans le TODO 4 pour choisir la bonne fonction ?",
      'Exemple : if choix == "rectangle":  puis appelle aire_rectangle(...)')

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Correction finale — à rouler avec ton père
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   Correction finale — Leçon 04           ║")
    print("╚══════════════════════════════════════════╝")

    r1 = tester_ex01()
    r2 = tester_ex02()

    grand_total_r = r1[0] + r2[0]
    grand_total_t = r1[1] + r2[1]

    print()
    print("═" * 42)
    print(f"🏆 Total leçon 04 : {grand_total_r} / {grand_total_t} tests réussis")
    if grand_total_r == grand_total_t:
        print("   🎉 Leçon 04 complétée avec succès !")
    print()
