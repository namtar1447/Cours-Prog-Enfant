# COURS_FORMAT.md — Référence de format pour le cours de programmation

Ce fichier documente les conventions et gabarits à respecter pour **toutes** les leçons du cours.
Il est destiné à être utilisé dans Claude Code pour guider la création et la modification du contenu.

---

## Contexte du cours

- **Apprenant** : garçon de 9 ans, à l'aise avec Scratch/MakeCode, très avancé en mathématiques
- **Langue** : français (termes techniques en anglais acceptés, ex. `print`, `return`)
- **Animateur** : le père, enseignant en informatique au cégep
- **Format de session** : présentation animée par le père → exercices guidés → mini-projet ou continuation de projet
- **Durée maximale par leçon** : 2 heures (théorie + pratique)

---

## Structure du repo GitHub

```
cours-python/
├── COURS_FORMAT.md          ← ce fichier
├── PLAN_DE_COURS.md         ← progression globale des leçons
├── lecon_01/
│   ├── presentation.html    ← support visuel animé par le père
│   ├── exercice_01.py       ← code à compléter
│   ├── exercice_02.py
│   └── tests.py             ← validation automatique de tous les exercices
├── lecon_02/
│   └── ...
└── projets/
    ├── calculatrice/
    └── jeu_2d/
```

Chaque dossier `lecon_XX/` est **autonome** : aucune dépendance entre dossiers sauf mention explicite.

---

## 1. Fichier `presentation.html`

### Rôle
Support visuel que le père projette/partage et anime lui-même. L'apprenant **regarde et écoute**, il ne navigue pas seul dans ce fichier.

### Format
- **Page web à défilement vertical** (pas de diapositives)
- **Thème sombre** — palette de couleurs à respecter :

```css
--bg:        #1e1e2e;   /* fond principal */
--surface:   #2a2a3e;   /* cartes, blocs */
--accent:    #7c6af7;   /* titres, accents, barres */
--accent2:   #f7a26a;   /* exemples de code, highlights secondaires */
--text:      #cdd6f4;   /* texte courant */
--muted:     #6c7086;   /* texte secondaire */
--success:   #a6e3a1;   /* correct */
--error:     #f38ba8;   /* erreur */
--warning:   #f9e2af;   /* avertissement */
```

- **Police** : `'Segoe UI'` pour le texte, `'Courier New'` ou `monospace` pour le code
- **Pas de dépendances externes** — tout le CSS et JS est inline dans le fichier HTML

### Structure interne obligatoire

```
[BARRE DE PROGRESSION FIXE EN HAUT]
  — affiche le plan de la leçon avec sections numérotées
  — la section active est mise en évidence (accent color)
  — reste visible en tout temps (position: sticky)

[SECTION 0 — EN-TÊTE]
  Numéro et titre de la leçon
  Objectifs d'apprentissage (liste à puces, 3-5 items max)
  Durée estimée

[SECTION 1..N — CONTENU]
  Chaque section = un concept ou une étape
  Voir conventions de contenu ci-dessous

[SECTION FINALE — RÉSUMÉ]
  Ce qu'on a appris (tableau ou liste)
  Lien vers les exercices
  Aperçu de la prochaine leçon
```

### Conventions de contenu

#### Principe directeur — support d'enseignement, pas document de lecture

La présentation est **animée par le père** — l'écran montre les ancres visuelles,
la voix porte l'explication. Le texte à l'écran ne doit pas remplacer ce que le
père dit : si on peut lire la carte en silence et tout comprendre sans lui, c'est
trop long.

#### Cartes analogie

Format : `icône  code/concept  →  métaphore  (précision optionnelle en muted)`

```html
<div class="card analogy">
  <div class="label analogy">Analogie — [thème]</div>
  <div style="display:flex; flex-direction:column; gap:10px; font-size:.95em;">
    <span>🍳 <code style="color:var(--accent2)">def nom():</code> &nbsp;→&nbsp; écrire la recette <span style="color:var(--muted)">(une seule fois)</span></span>
    <span>🍽️ <code style="color:var(--accent2)">nom()</code> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;→&nbsp; cuisiner <span style="color:var(--muted)">(autant de fois qu'on veut)</span></span>
  </div>
</div>
```

Règles :
- Maximum 2-3 lignes icône+flèche
- Pas de paragraphes, pas de "c'est comme si…" développé — le père le dit
- Le label nomme le thème de l'analogie, pas juste "Analogie"

#### Cartes info

Bullets courts — 5 mots max par bullet, ancres pour la parole du père.

```html
<div class="card info">
  <div class="label code">Titre</div>
  <ul style="padding-left: 20px; display: flex; flex-direction: column; gap: 8px;">
    <li><strong>Mot-clé</strong> &nbsp;<code>syntaxe</code> — effet en 3 mots</li>
    <li><strong>Mot-clé</strong> &nbsp;<code>syntaxe</code> — effet en 3 mots</li>
  </ul>
</div>
```

#### Cartes warning

Label court + bloc de code uniquement — pas de paragraphe explicatif.

```html
<div class="card warning">
  <div class="label" style="background:rgba(249,226,175,.2); color:var(--warning)">⚠ Règle en 5 mots</div>
  <div class="code-block" style="margin-top:10px;">...</div>
</div>
```

#### Ce qui reste complet (ne pas raccourcir)

- **Blocs de code** : complets, syntaxe colorée avec `<span>`, fond `#13131f`
- **Visualisations interactives** : animation cliquable JS pur — "Étape suivante", sliders, démos
- **Quiz** : 3 tentatives, 2 niveaux d'indice (voir section quiz ci-dessous)
- **Section Résumé** : tableau complet + carte "À retenir"
- **Section Rappel** : 3 blocs de code compacts en grille responsive

#### Blocs de code

Fond légèrement plus sombre que `--surface`, coins arrondis, syntaxe colorée manuellement avec `<span>`.

#### Visualisations interactives

Quand un concept le permet (boucles, listes, appels de fonctions), inclure une
animation ou démonstration cliquable en JavaScript pur. Ex. : bouton "Étape
suivante" qui montre l'état d'une variable à chaque itération.

#### Quiz intégré

Optionnel par section, 1-2 questions max.

**Pas de murs de texte** : maximum 3 lignes de texte consécutives hors cartes. Alterner texte / code / visuel.

### Format des quiz dans le HTML

- Bouton **"Vérifier"** par question (pas de correction automatique immédiate)
- **3 tentatives** par question avant révélation de la réponse
  - Tentative 1 échouée → indice léger affiché
  - Tentative 2 échouée → indice plus précis affiché
  - Tentative 3 échouée → réponse révélée avec explication
- Feedback visuel : bordure verte (`--success`) si correct, rouge (`--error`) si incorrect
- Questions à choix multiple **ou** à saisie de texte courte (ex. : "Quelle valeur aura `x` ?")

---

## 2. Fichiers `exercice_XX.py`

### Rôle
Code Python que l'apprenant ouvre dans **Thonny** (leçons 1–13) ou **VS Code** (leçons 14–20) et complète.

### Format général

```python
# ============================================================
# Leçon XX — Titre de la leçon
# Exercice YY — Titre de l'exercice
# ============================================================
# OBJECTIF : Description claire de ce que cet exercice accomplit,
#            écrite pour un enfant de 9 ans.
#
# COMMENT TESTER : Clique sur ▶
# ============================================================

# --- EXEMPLE (ne pas modifier) ---
# Voici comment fonctionne [concept] :
exemple_variable = 42
print(exemple_variable)   # affiche : 42

# --- TON TOUR ---

# TODO 1 : [Description du comportement attendu, pas de la syntaxe]
#           Ex. : "Crée une variable qui contient ton âge"
#           (pas : "Écris age = ...")


# TODO 2 : [Description suivante]


if __name__ == "__main__":
    from tests import tester_exYY
    tester_exYY()
```

> **Note :** Le bloc `if __name__ == "__main__":` en bas de chaque exercice lance automatiquement
> les tests de cet exercice quand l'apprenant clique sur ▶ dans Thonny. Il n'est **pas exécuté**
> quand `tests.py` importe le fichier comme module — ce qui évite toute duplication.

### Règles pour les TODO
- Décrire **ce que le code doit faire**, jamais **comment l'écrire**
- Maximum **5 TODO** par exercice
- Laisser suffisamment d'espace vide entre les TODO pour que l'apprenant écrive
- Un commentaire `# --- EXEMPLE ---` précède toujours la partie à compléter
- Ne jamais donner la réponse dans l'exemple si elle est identique à ce qu'on demande

### Niveaux de difficulté des exercices dans une leçon
1. **Exercice 1** — guidé : structure fournie, l'apprenant remplit les trous
2. **Exercice 2** — semi-guidé : quelques indications, plus de liberté
3. **Exercice 3** (si pertinent) — ouvert : consigne courte, solution libre

---

## 3. Fichier PROJET.md" dans les formats de fichiers

### Rôle
Remplace les TODO — donne un objectif ouvert sans dicter la solution.
Présent uniquement quand la leçon se termine par un projet libre.

### Format
```markdown
# Projet — [Titre]

## Ce que ton programme doit faire
- [Comportement attendu 1]
- [Comportement attendu 2]

## Exemple de ce que tu devrais voir
```
> Entrez un nombre : 5
> Entrez un autre nombre : 3
> Résultat : 8

### Critères de réussite

- Le programme démarre sans erreur
- [Critère fonctionnel 1]
- [Critère fonctionnel 2]

### Règles optionnelles si le père décide de pousser une notion plus loin
- Pas de TODO, pas d'indices de syntaxe
- Les critères décrivent le **comportement**, jamais le code
- Le fichier de départ (`projet_XX.py`) contient uniquement les imports
  nécessaires et éventuellement la structure `if __name__ == "__main__":`
- Pas de `tests.py` automatique — correction par le père selon les critères

## 4. Fichier `tests.py`

### Rôle
`tests.py` a **deux usages** :

| Contexte | Comment | Ce qui se passe |
|---|---|---|
| L'apprenant clique ▶ sur un exercice | `exercice_XX.py` appelle `tester_exXX()` via son bloc `__main__` | Tests de cet exercice seulement |
| Correction finale avec le père | ▶ sur `tests.py` directement | Tous les exercices testés, grand total |

### Format général

```python
# ============================================================
# tests.py — Leçon XX
# Roule ce fichier avec ton père pour la correction finale !
# (Chaque exercice se teste automatiquement quand tu le roules.)
# ============================================================

import sys, io, pathlib
from unittest.mock import patch


def _lire_source(nom_fichier):
    return (pathlib.Path(__file__).parent / nom_fichier).read_text(encoding="utf-8")

def _apres_todo(source, numero, *mots):
    marqueur = f"# TODO {numero}"
    if marqueur not in source:
        return False
    return all(m in source.split(marqueur)[-1] for m in mots)

def _resume(reussis, total):
    print(f"\n🏁 {reussis} / {total} tests réussis")
    # message encourageant selon le score


# Une fonction par exercice — importable depuis l'exercice lui-même
def tester_ex01():
    r = [0, 0]  # [réussis, total]

    def v(nom, cond, indice_1, indice_2):
        r[1] += 1
        if cond:
            print(f"  ✅ {nom}"); r[0] += 1
        else:
            print(f"  ❌ {nom}")
            print(f"     💡 Indice : {indice_1}")
            print(f"        Si tu es encore bloqué : {indice_2}")
            print( "        Sinon, consulte CORRECTION.md avec ton père.")

    # Import de l'exercice avec capture de la sortie
    sortie_cap = io.StringIO()
    with patch("sys.stdout", new=sortie_cap):
        import exercice_01 as ex

    # Tests de variables, de sortie, et d'usage des f-strings
    v("...", ..., "indice conceptuel", "indice technique")
    # ...

    _resume(r[0], r[1])
    return r[0], r[1]


# Correction finale : tous les exercices + grand total
if __name__ == "__main__":
    r1 = tester_ex01()
    r2 = tester_ex02()
    print(f"\n🏆 Total : {r1[0]+r2[0]} / {r1[1]+r2[1]}")
```

### Règles pour les tests
- **Feedback en français**, ton encourageant
- **2 niveaux d'indice** par échec : conceptuel puis technique — renvoi vers `CORRECTION.md` au-delà
- Tester le **comportement**, pas le style
- Toujours capturer `stdout` pendant l'import pour pouvoir valider la sortie imprimée
- Inspecter le **code source** (`_apres_todo`) pour détecter les valeurs écrites en dur dans les f-strings
- Chaque fonction `tester_exXX()` retourne `(réussis, total)` pour permettre le grand total dans `__main__`
- `input()` simulé avec `unittest.mock.patch` — prévoir autant de valeurs que d'appels dans le fichier (exemple inclus)

### Fichier `CORRECTION.md` (par leçon)
- Contient les solutions complètes
- **À garder côté père** — ne pas inclure dans la branche GitHub publique de l'apprenant
- Format : une section par exercice avec le code solution et une explication

---

## 5. Fichier `README.md` — ❌ Ne pas générer

Les README.md ne font **pas** partie des livrables d'une leçon. L'apprenant travaille avec
la présentation HTML ouverte dans le navigateur et Thonny — un fichier Markdown texte n'ajoute
aucune valeur dans ce contexte. Le résumé de leçon et le glossaire sont intégrés directement
dans la section **Résumé** de `presentation.html`.

---

## 6. Conventions globales

### Langue et ton
- Tout le contenu est en **français**
- Les mots-clés Python restent en anglais (`print`, `if`, `for`, etc.)
- Ton **encourageant et direct** — s'adresser à "toi" (tutoiement)
- Éviter le jargon adulte ; utiliser des analogies du quotidien d'un enfant de 9 ans
- Les tests servent à valider la compréhension. Par exemple, les tests avec une chaîne n'ont généralement pas besoin de valider les espaces et l'exactitude du français

### Thématiques des leçons
- Choisir des thèmes **concrets et motivants** pour un garçon de 9 ans passionné de jeux
- Exemples acceptables : jeux vidéo, inventaires de RPG, scores, mondes, créatures, magie
- Progression vers les projets cibles : **calculatrice graphique** (interface style TI-83 avec `customtkinter` + tracé de fonctions avec `matplotlib` + grands nombres avec `mpmath`) et **mod Luanti**

### Longueur du contenu
- Chaque leçon doit être réalisable en **maximum 2 heures**
- La présentation HTML seule : 20-35 minutes d'animation
- Les exercices : 45-75 minutes au total
- Mini-projet (si présent) : 15-30 minutes

### Visualisations interactives (dans le HTML)
- Préférer le **JavaScript pur** (pas de bibliothèques externes)
- Animations simples : pas de WebGL, pas de Canvas complexe
- Toujours inclure un bouton "Réinitialiser" sur les démos interactives

### Concepts de game design (blocs 2 et 3)
Certaines leçons incluent une section **"🎮 Design de jeu"** dans la présentation HTML.
Ces sections expliquent *pourquoi* certains mécanismes existent dans les jeux, en langage accessible.
Elles ne contiennent pas de code — elles alimentent la réflexion et la discussion avec le père.

### Gestion d'erreurs (try/except)
- **Leçons 1–5** : ne pas enseigner try/except. Fournir silencieusement un wrapper global
  dans le fichier de départ pour éviter les tracebacks intimidants :
```python
  if __name__ == "__main__":
      try:
          main()
      except Exception as e:
          print(f"Oups ! Une erreur inattendue : {e}")
          print("Relis ton code et réessaie !")
```
- **Leçon 6b** : introduire try/except de façon concrète, uniquement comme réponse à des
  erreurs déjà vécues. Se limiter à `ValueError` (saisie invalide) et `ZeroDivisionError`.
  Pas de hiérarchie d'exceptions, pas de `finally`, pas de `raise`.

---

## 7. Progression des blocs

### Bloc 1 — Python fondamentaux (leçons 1–6) — IDE : Thonny
| Leçon | Sujet principal | Projet/pratique |
|---|---|---|
| 00 | Introduction à Thonny | Écrire et rouler son premier programme |
| 01 | Variables, types, `print`, `input` | Mini-calculatrice de base |
| 02 | Conditions (`if/elif/else`) | Calculatrice avec détection d'erreurs |
| 03 | Boucles (`for`, `while`) | Tables de multiplication, countdown |
| 04 | Fonctions, paramètres, `return` | Fonctions mathématiques réutilisables |
| 05 | Listes, dictionnaires | Historique de calculs |
| 06 | Modules, `import`, `mpmath` | Calculatrice avancée (grands nombres, tétration) |
| 06b | `customtkinter` + `matplotlib` — interface TI-83 | **Projet : calculatrice graphique complète** |

### Bloc 2 — Jeux 2D avec pygame (leçons 7–13) — IDE : Thonny
| Leçon | Sujet principal | Game design |
|---|---|---|
| 07 | Fenêtre, boucle de jeu, événements | 🎮 La boucle update → draw → repeat |
| 08 | Images, sprites, animations | 🎮 Le *game feel* et la fluidité |
| 09 | Collisions, limites d'écran | 🎮 Tension et risque |
| 10 | Score, vies, état du jeu | 🎮 Progression et feedback |
| 11 | Écrans multiples (menu, pause, game over) | 🎮 Structure d'un jeu complet |
| 12 | Sons, effets visuels simples | 🎮 Le polish |
| 13 | **Projet : jeu 2D complet** | 🎮 Bilan de conception |

### Bloc 3 — Lua & Luanti (leçons 14–20) — IDE : VS Code
| Leçon | Sujet principal | Game design |
|---|---|---|
| 14 | Lua vs Python — mêmes idées, syntaxe différente | — |
| 15 | Structure d'un mod, API Luanti de base | 🎮 Minecraft : règles simples, profondeur émergente |
| 16 | Événements, triggers, `on_place` / `on_use` | — |
| 17 | Tables avancées, craft recipes | — |
| 18 | Entités et mobs simples | 🎮 Les mobs comme mécaniques |
| 19 | Génération de terrain, biomes | — |
| 20 | **Projet : mini-mod Luanti complet** | 🎮 Bilan : concevoir une expérience |

---

## 8. Instructions pour Claude Code

Quand tu génères ou modifies du contenu pour ce cours, respecte ces règles :

1. **Toujours consulter ce fichier** avant de créer quoi que ce soit
2. **Un fichier à la fois** — ne pas générer toute une leçon d'un coup sans valider le premier fichier
3. **Tester mentalement** : s'assurer que les exercices sont réalisables par un enfant de 9 ans en moins de 15 minutes chacun
4. **Pas de solutions dans les exercices** — les `TODO` ne doivent jamais contenir de code solution en commentaire
5. **Le fichier `CORRECTION.md` est séparé** et doit être rappelé à chaque leçon générée
6. **Respecter la palette de couleurs exacte** définie dans la section HTML
7. **Signaler** si une leçon risque de dépasser 2 heures au total

### Commande type pour démarrer une leçon
> "Crée la leçon 01 du cours selon COURS_FORMAT.md. Commence par `presentation.html`, attends ma validation avant de générer les exercices."
