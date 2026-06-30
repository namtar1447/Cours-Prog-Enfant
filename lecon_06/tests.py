# ============================================================
# tests.py — Leçon 06
# Roule ce fichier avec ton père pour la correction finale !
# (Chaque exercice se teste automatiquement quand tu le roules.)
# ============================================================

import sys, io, pathlib
from unittest.mock import patch


# ── Helpers ─────────────────────────────────────────────────

def _lire_source(nom_fichier):
    return (pathlib.Path(__file__).parent / nom_fichier).read_text(encoding="utf-8")


def _apres_todo(source, numero, *mots):
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
# Exercice 01 — Mathématiques de précision
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
    print("🧪 Tests — Exercice 01 : Mathématiques de précision")
    print("─" * 42)

    source = _lire_source("exercice_01.py")
    sortie_cap = io.StringIO()

    try:
        with patch("sys.stdout", new=sortie_cap):
            import exercice_01 as ex1  # noqa: F401
    except Exception as e:
        print(f"  ⛔ Erreur dans exercice_01.py : {e}")
        print("     Vérifie qu'il n'y a pas d'erreur de syntaxe.")
        print("     mpmath est-il installé ? (Outils → Gérer les paquets)")
        return 0, 0

    sortie = sortie_cap.getvalue()
    # Exclure les lignes de l'exemple (sqrt(2), π normal, π précis)
    lignes = [l for l in sortie.splitlines()
              if "sqrt(2)" not in l and "π normal" not in l and "π précis" not in l]
    sortie_eleve = "\n".join(lignes)

    # ── TODO 1 — diagonale ───────────────────────────────────
    import math
    diag = math.sqrt(6**2 + 8**2)  # = 10.0

    v("TODO 1 — utilise math.sqrt()",
      _apres_todo(source, 1, "sqrt"),
      "As-tu utilisé math.sqrt() dans le TODO 1 ?",
      "Exemple : d = math.sqrt(6**2 + 8**2)")

    v("TODO 1 — la diagonale est correcte (10 m)",
      "10" in sortie_eleve,
      "La diagonale d'une pièce 6×8 mesure 10 m (Pythagore : 6²+8²=100, √100=10).",
      "Calcul : math.sqrt(6**2 + 8**2)  →  10.0")

    # ── TODO 2 — factorial(15) ────────────────────────────────
    fact15 = str(math.factorial(15))

    v("TODO 2 — calcule factorial(15)",
      _apres_todo(source, 2, "factorial"),
      "As-tu utilisé math.factorial(15) dans le TODO 2 ?",
      "Exemple : r = math.factorial(15)  puis print(r)")

    v("TODO 2 — affiche le nombre de chiffres",
      _apres_todo(source, 2, "len") and _apres_todo(source, 2, "str"),
      "As-tu utilisé len(str(...)) pour compter les chiffres ?",
      "Exemple : print(f\"factorial(15) a {len(str(math.factorial(15)))} chiffres\")")

    # ── TODO 3 — factorial(100) chiffres ──────────────────────
    nb_chiffres_100 = str(len(str(math.factorial(100))))  # 158

    v("TODO 3 — affiche le nombre de chiffres de factorial(100)",
      nb_chiffres_100 in sortie_eleve,
      f"factorial(100) a {nb_chiffres_100} chiffres — ce nombre doit apparaître dans ta sortie.",
      "Calcul : len(str(math.factorial(100)))  →  158")

    # ── TODO 4 — mp.pi ───────────────────────────────────────
    v("TODO 4 — utilise mp.pi",
      _apres_todo(source, 4, "mp.pi"),
      "As-tu affiché mp.pi dans le TODO 4 ?",
      "Exemple : print(mp.pi)")

    v("TODO 4 — change mp.dps deux fois",
      source.count("mp.dps") >= 2,
      "As-tu changé mp.dps deux fois (une fois à 50, une fois à 100) ?",
      "Exemple : mp.dps = 50  puis  mp.dps = 100")

    # ── TODO 5 — table de factorielles ───────────────────────
    v("TODO 5 — utilise une boucle for",
      _apres_todo(source, 5, "for"),
      "As-tu écrit une boucle for dans le TODO 5 ?",
      "Exemple : for n in range(1, 13):")

    v("TODO 5 — affiche factorial dans la boucle",
      _apres_todo(source, 5, "factorial"),
      "As-tu utilisé factorial() à l'intérieur de ta boucle (TODO 5) ?",
      "Exemple : r = math.factorial(n)  puis print(...)")

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Exercice 02 — Tétration
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
    print("🧪 Tests — Exercice 02 : Tétration")
    print("─" * 42)

    source = _lire_source("exercice_02.py")
    sortie_cap = io.StringIO()

    try:
        with patch("sys.stdout", new=sortie_cap):
            import exercice_02 as ex2
    except Exception as e:
        print(f"  ⛔ Erreur dans exercice_02.py : {e}")
        print("     Vérifie qu'il n'y a pas d'erreur de syntaxe.")
        return 0, 0

    sortie = sortie_cap.getvalue()
    # Exclure les lignes de l'exemple
    lignes = [l for l in sortie.splitlines()
              if not any(ex in l for ex in ["2↑↑1 = 2", "2↑↑2 = 4", "2↑↑3 = 16", "2↑↑4 = 65536"])]
    sortie_eleve = "\n".join(lignes)

    # ── Fonction tetration ────────────────────────────────────
    tet = getattr(ex2, "tetration", None)

    v("La fonction 'tetration' existe",
      callable(tet),
      "La fonction tetration() est déjà fournie dans l'exemple — ne la supprime pas !",
      "Elle doit rester au-dessus des TODO.")

    v("tetration(2, 1) = 2",
      callable(tet) and tet(2, 1) == 2,
      "tetration(2, 1) devrait retourner 2 (cas de base b==1).",
      "Vérifie que la définition de tetration() est intacte dans l'exemple.")

    v("tetration(2, 4) = 65536",
      callable(tet) and tet(2, 4) == 65536,
      "tetration(2, 4) = 2^(2^(2^2)) = 2^(2^4) = 2^16 = 65536.",
      "La fonction doit être récursive : return a ** tetration(a, b-1)")

    v("tetration(3, 3) = 7625597484987",
      callable(tet) and tet(3, 3) == 7625597484987,
      "tetration(3, 3) = 3^(3^3) = 3^27 = 7 625 597 484 987.",
      "Vérifie que la fonction est bien définie et essaie tetration(3, 3) dans Thonny.")

    # ── TODO 1 — boucle 2↑↑1 à 2↑↑5 ─────────────────────────
    v("TODO 1 — utilise une boucle for",
      _apres_todo(source, 1, "for"),
      "As-tu écrit une boucle for dans le TODO 1 ?",
      "Exemple : for b in range(1, 6): print(tetration(2, b))")

    v("TODO 1 — affiche le nombre de chiffres",
      _apres_todo(source, 1, "len"),
      "As-tu utilisé len() pour compter les chiffres dans le TODO 1 ?",
      "Exemple : print(f\"({len(str(r))} chiffres)\")")

    # ── TODO 3 — trouver le seuil ─────────────────────────────
    v("TODO 3 — utilise une boucle while",
      _apres_todo(source, 3, "while"),
      "As-tu utilisé une boucle while dans le TODO 3 ?",
      "Exemple : while tetration(2, b) <= 1_000_000: b += 1")

    v("TODO 3 — la réponse correcte (b=5) apparaît dans la sortie",
      "5" in sortie_eleve,
      "2↑↑4 = 65 536 < 1 000 000, donc 2↑↑5 = 2^65536 > 1 000 000. La réponse est b=5.",
      "Vérifie que ta boucle while s'arrête bien quand tetration(2, b) > 1_000_000.")

    # ── TODO 4 — somme des chiffres ───────────────────────────
    v("TODO 4 — utilise une boucle sur str()",
      _apres_todo(source, 4, "for") and _apres_todo(source, 4, "str"),
      "As-tu parcouru les chiffres de 65536 avec for c in str(65536): ?",
      "Exemple : total = 0  /  for c in str(65536): total += int(c)")

    v("TODO 4 — la somme est correcte (6+5+5+3+6 = 25)",
      "25" in sortie_eleve,
      "La somme des chiffres de 65536 est : 6+5+5+3+6 = 25.",
      "Vérifie que tu convertis chaque caractère en int avant d'additionner.")

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Correction finale — à rouler avec ton père
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   Correction finale — Leçon 06           ║")
    print("╚══════════════════════════════════════════╝")

    r1 = tester_ex01()
    r2 = tester_ex02()

    grand_total_r = r1[0] + r2[0]
    grand_total_t = r1[1] + r2[1]

    print()
    print("═" * 42)
    print(f"🏆 Total leçon 06 : {grand_total_r} / {grand_total_t} tests réussis")
    if grand_total_r == grand_total_t:
        print("   🎉 Leçon 06 complétée avec succès !")
    print()
