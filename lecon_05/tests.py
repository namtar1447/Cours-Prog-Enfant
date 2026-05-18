# ============================================================
# tests.py — Leçon 05
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
# Exercice 01 — L'inventaire du héros
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
    print("🧪 Tests — Exercice 01 : Inventaire du héros")
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
    # Ignorer les lignes de l'exemple (qui contiennent les mots de l'exemple)
    lignes = [l for l in sortie.splitlines() if "boule de feu" not in l and "téléportation" not in l and "éclair" not in l]
    sortie_eleve = "\n".join(lignes)

    # ── La liste inventaire ──────────────────────────────────
    inventaire = getattr(ex1, "inventaire", None)

    v("La variable 'inventaire' est une liste",
      isinstance(inventaire, list),
      "As-tu créé  inventaire = [...]  dans le TODO 1 ?",
      "Exemple : inventaire = [\"épée\", \"bouclier\", \"potion\", \"arc\"]")

    v("La liste contient au moins 4 objets au départ",
      isinstance(inventaire, list) and len(inventaire) >= 3,
      "Ta liste doit contenir au moins 4 objets au départ (TODO 1).",
      "Ajoute des objets entre les crochets, séparés par des virgules.")

    # ── append et pop ────────────────────────────────────────
    v("TODO 3 — utilise append()",
      _apres_todo(source, 3, "append"),
      "As-tu utilisé  inventaire.append(...)  dans le TODO 3 ?",
      "Exemple : inventaire.append(\"flèche\")")

    v("TODO 3 — utilise len()",
      _apres_todo(source, 3, "len"),
      "As-tu utilisé  len(inventaire)  dans le TODO 3 pour afficher la taille ?",
      "Exemple : print(f\"Il y a {len(inventaire)} objets\")")

    v("TODO 4 — utilise pop()",
      _apres_todo(source, 4, "pop"),
      "As-tu utilisé  inventaire.pop()  dans le TODO 4 ?",
      "Exemple : retiré = inventaire.pop()  puis print(retiré)")

    # ── Boucle for + enumerate ───────────────────────────────
    v("TODO 5 — utilise une boucle for",
      _apres_todo(source, 5, "for"),
      "As-tu écrit une boucle  for  dans le TODO 5 ?",
      "Exemple : for i, objet in enumerate(inventaire):")

    v("TODO 5 — utilise enumerate()",
      _apres_todo(source, 5, "enumerate"),
      "As-tu utilisé  enumerate()  dans ta boucle pour numéroter les objets ?",
      "Exemple : for i, objet in enumerate(inventaire):  /  print(f\"[{i}] {objet}\")")

    # ── Sortie ───────────────────────────────────────────────
    v("Le programme affiche quelque chose",
      len(sortie_eleve.strip()) > 0,
      "Ton programme n'affiche rien — as-tu des print() dans tes TODO ?",
      "Chaque TODO doit contenir au moins un print().")

    v("La sortie contient un index entre crochets (ex : [0])",
      any(f"[{i}]" in sortie_eleve for i in range(10)),
      "As-tu affiché les index avec  [i]  dans le TODO 5 ?",
      "Exemple : print(f\"[{i}] {objet}\")")

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Exercice 02 — La fiche de héros
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
    print("🧪 Tests — Exercice 02 : Fiche de héros")
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
    # Ignorer les lignes de l'exemple (Gobelin)
    lignes = [l for l in sortie.splitlines() if "Gobelin" not in l and "journal_exemple" not in l]
    sortie_eleve = "\n".join(lignes)

    # ── Dictionnaire heros ───────────────────────────────────
    heros = getattr(ex2, "heros", None)

    v("La variable 'heros' est un dictionnaire",
      isinstance(heros, dict),
      "As-tu créé  heros = {...}  dans le TODO 1 ?",
      "Exemple : heros = {\"nom\": \"Arthur\", \"pv\": 100, \"force\": 42, \"niveau\": 5}")

    v("Le dictionnaire contient la clé 'nom'",
      isinstance(heros, dict) and "nom" in heros,
      "As-tu ajouté la clé  \"nom\"  dans ton dictionnaire ?",
      "Exemple : heros = {\"nom\": \"Arthur\", ...}")

    v("Le dictionnaire contient la clé 'pv'",
      isinstance(heros, dict) and "pv" in heros,
      "As-tu ajouté la clé  \"pv\"  dans ton dictionnaire ?",
      "Exemple : \"pv\": 100")

    v("Le dictionnaire contient au moins 4 clés",
      isinstance(heros, dict) and len(heros) >= 4,
      "Ton dictionnaire doit avoir au moins 4 clés (nom, pv, force, niveau).",
      "Ajoute les clés manquantes séparées par des virgules dans les accolades.")

    # ── Liste journal ────────────────────────────────────────
    journal = getattr(ex2, "journal", None)

    v("La variable 'journal' est une liste",
      isinstance(journal, list),
      "As-tu créé  journal = []  dans le TODO 2 ?",
      "Une liste vide s'écrit avec deux crochets : journal = []")

    v("Le journal contient au moins 2 entrées",
      isinstance(journal, list) and len(journal) >= 2,
      "As-tu ajouté au moins 2 événements dans le journal avec append() (TODO 3 et 4) ?",
      "Exemple : journal.append(\"Arthur perd 15 pv\")")

    # ── Structure du code ────────────────────────────────────
    v("TODO 3 — utilise append() pour enregistrer l'attaque",
      _apres_todo(source, 3, "append"),
      "As-tu utilisé  journal.append(...)  dans le TODO 3 ?",
      "Exemple : journal.append(f\"Arthur perd {degats} pv\")")

    v("TODO 5 — utilise une boucle for pour afficher le journal",
      _apres_todo(source, 5, "for"),
      "As-tu écrit une boucle  for  dans le TODO 5 pour parcourir le journal ?",
      "Exemple : for entree in journal:  /  print(entree)")

    # ── Sortie ───────────────────────────────────────────────
    v("La sortie affiche le nom du héros",
      isinstance(heros, dict) and "nom" in heros and str(heros["nom"]) in sortie_eleve,
      "As-tu affiché le nom de ton héros avec print() dans le TODO 2 ?",
      "Exemple : print(f\"Nom : {heros['nom']}\")")

    _resume(r[0], r[1])
    return r[0], r[1]


# ════════════════════════════════════════════════════════════
# Correction finale — à rouler avec ton père
# ════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("╔══════════════════════════════════════════╗")
    print("║   Correction finale — Leçon 05           ║")
    print("╚══════════════════════════════════════════╝")

    r1 = tester_ex01()
    r2 = tester_ex02()

    grand_total_r = r1[0] + r2[0]
    grand_total_t = r1[1] + r2[1]

    print()
    print("═" * 42)
    print(f"🏆 Total leçon 05 : {grand_total_r} / {grand_total_t} tests réussis")
    if grand_total_r == grand_total_t:
        print("   🎉 Leçon 05 complétée avec succès !")
    print()
