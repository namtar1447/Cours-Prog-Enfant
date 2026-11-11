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

#### Cartes « Boîte à outils » — une par TODO (depuis la leçon 11)

Chaque TODO du fichier d'Adam a sa carte dans la présentation, **avec le même
numéro**, placée dans la section qui enseigne la notion. C'est là qu'il va chercher
le modèle quand il bloque.

```html
<div class="card outils">
  <div class="label outils">🧰 Boîte à outils — TODO 3</div>
  <div class="code-block" style="margin-top:10px;">…</div>
</div>
```

- TODO « **Écris :** » → la carte montre la **ligne exacte**, avec un « avant /
  après » si Adam modifie une ligne fournie.
- TODO « **Complète :** » (à trous) → la carte montre un exemple **d'un autre jeu**
  (`score >= 100`, `vie < 0`) : Adam adapte, il ne recopie pas tel quel.
- Une clé de dictionnaire qui ne ressemble pas au nom de la variable
  (`couleur_sol` ↔ `"collines"`) → un petit tableau dans la carte.

#### Cartes « Explique à papa » — à la fin de chaque section de notion

Deux ou trois questions sur **à quoi ça sert**, pas sur le calcul. Le but :
qu'Adam puisse le dire avec ses mots, même s'il ne sait pas refaire le calcul.

```html
<div class="card papa">
  <div class="label papa">🗣️ Explique à papa</div>
  <ul>…</ul>
</div>
```

CSS : `.card.outils` bordure `#89dceb`, `.card.papa` bordure `#f5c2e7` (voir
`lecon_11/presentation.html`).

#### Les mesures et les justifications vont dans `CORRECTION.md`

La présentation montre **comment** et **à quoi ça sert**. Les chiffres de
calibrage (« immobile 42 % du temps », « 3,7 px contre 2,6 ») sont pour le père ;
à l'écran, ils prennent la place de l'explication dont Adam a besoin. Exception :
une mesure qui sert un quiz ou une discussion de game design (« le bon joueur
meurt plus tôt et va plus loin »).

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
Code Python que l'apprenant ouvre dans **Thonny** (leçons 1–14) ou **VS Code** (leçons 15–21) et complète.

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
- Maximum **5 TODO** par exercice (un TODO peut avoir deux étapes, `3a` / `3b`)
- Laisser suffisamment d'espace vide entre les TODO pour que l'apprenant écrive
- Un commentaire `# --- EXEMPLE ---` précède toujours la partie à compléter
- Ne jamais donner la réponse dans l'exemple si elle est identique à ce qu'on demande

### Doser la difficulté d'un TODO — leçons apprises (2026-11-11)

**Ce qui s'est passé.** Jusqu'à la leçon 09b, Adam avançait surtout seul. La leçon
10 a été trop dure : il ne savait pas quoi écrire, et le père a dû faire presque
tout avec lui. Il n'a avancé qu'en découvrant qu'il pouvait **recopier le résumé de
fin de leçon**. La leçon 11 bloquait de la même façon et a été refaite.

**Le diagnostic.** Les maths en elles-mêmes passent. Ce qui bloque, c'est de :

1. **combiner** plusieurs équations dans une même ligne
   (`part = min(1.0, (h - SEUIL) / (HAUT - SEUIL))`) ;
2. **inventer** la ligne à partir d'une phrase (« proportionnellement »,
   « 1 + 0.35 fois plus vite »), alors qu'en 09/09b la consigne la donnait
   (« Modèle : », « Écris : ») ;
3. **ne pas pouvoir tester** : le code fourni utilisait une variable que seul
   le dernier TODO créait, donc le jeu plantait (`NameError`) jusqu'à la fin ;
4. **plafonds et planchers** avec `min` / `max` : mal compris dès la leçon 10.

Adam sait **adapter une ligne qu'il a sous les yeux**. Le format le lui permet
désormais officiellement.

**Les règles qui en découlent** (appliquées depuis la refonte de la leçon 11) :

| # | Règle | Comment |
|---|---|---|
| 1 | **Un TODO = une idée = une ou deux lignes** | Si la ligne combine deux équations, l'une des deux est fournie (`fois_plus_vite = 1 + FACTEUR_ILE * ile`) ou le TODO est coupé en `a` / `b`. |
| 2 | **Une seule nouvelle équation à écrire par leçon**, au plus | Les autres sont fournies, ou cachées dans une fonction qu'il **appelle** (`melanger(...)`) : appeler une fonction, c'est le niveau de la leçon 04. |
| 3 | **Chaque TODO a son modèle visible** | « Écris : » + la ligne, ou « Complète : » + une ligne à trous (`if heure >= ___:`), plus sa carte « Boîte à outils » (section 1). |
| 4 | **Le jeu tourne après chaque TODO** | Le code fourni ne dépend jamais d'une variable que crée un TODO. Sinon : une **valeur par défaut** fournie, qu'Adam **modifie** (`couleur_ciel = THEME["ciel"]` → `melanger(...)`). Vérifier en lançant le jeu avec 0, 1, 2… TODO faits. |
| 5 | **Une ligne « ▶ Teste : »** par TODO | Ce qu'il doit voir à l'écran. Si l'effet est invisible, ajouter un retour visible dans le code fourni (« + jour ! »), ou le **dire honnêtement** (« rien de nouveau à voir, c'est normal »). |
| 6 | **Un « Pourquoi ? » d'une phrase** dans chaque TODO | À quoi ça sert dans le jeu, pas comment ça calcule. |
| 7 | **Pas de `min` / `max` à écrire** | Un plancher s'écrit avec un `if` (leçon 02) : `if heure < 0.0: heure = 0.0`. `min` / `max` restent permis dans le code fourni. |
| 8 | **L'ordre des TODO suit la leçon, pas le fichier** | L'en-tête du fichier le dit, et explique Ctrl+F pour trouver « TODO 3 ». |
| 9 | **Des nombres ronds pour expliquer** | Moitiés et quarts (4 cuillères), 200 et 40 plutôt que 134 et 42. Pas de nombres négatifs dans une explication s'il y a moyen de les éviter : `jour × (1 − part) + nuit × part` plutôt que `jour + (nuit − jour) × part`. |

**Ce que ça remplace.** L'ancienne règle « décrire ce que le code doit faire, jamais
comment l'écrire » reste vraie pour les exercices de **logique** (une boucle, une
condition, un algorithme) : là, chercher la ligne *est* l'exercice. Elle ne
s'applique plus aux **formules** du bloc 2 : là, la compétence visée est de savoir
à quoi la formule sert et où la mettre, pas de la redécouvrir.

### Niveaux de difficulté des exercices dans une leçon
1. **Exercice 1** — guidé : structure fournie, l'apprenant remplit les trous
2. **Exercice 2** — semi-guidé : quelques indications, plus de liberté
3. **Exercice 3** (si pertinent) — ouvert : consigne courte, solution libre

### Exception au nommage — leçons « module à compléter »

Quand la leçon consiste à écrire des **modules qu'un programme fourni importe**,
les fichiers de l'apprenant portent un nom parlant plutôt que `exercice_XX.py`.

**Pourquoi** : `from exercice_01 import factorielle` dans un moteur se lit mal, et le
nom parlant fait partie de l'enseignement — écrire un module importable *est* la leçon.

**Appliqué à la leçon 06b** : `mes_operations.py` et `mon_historique.py`. Les fonctions
de test correspondantes s'appellent `tester_operations()` et `tester_historique()`
au lieu de `tester_exXX()`. Tout le reste du format (TODO max 5, deux niveaux d'indice,
bloc `__main__` qui lance les tests, `CORRECTION.md` séparé) reste identique.

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

> ⚠️ **Le bloc 2 (pygame) est exempt** — pas de `tests.py`. Une boucle de jeu n'a ni
> `stdout` capturable ni fin, et le résultat est visuel. La validation s'y fait par
> checklist observable dans `presentation.html` — voir la **section 9.7**.

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
- Tout le contenu est en **français québécois** naturel : phrases simples et
  directes, sujet-verbe-complément. Pas de tournures imagées à la française
  (« c'est heure qui tient la cuillère » → « l'heure change le nombre de
  cuillères »). En cas de doute, la version la plus plate est la bonne.
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

### Bloc 2 — Jeux 2D avec pygame (leçons 7–14) — IDE : Thonny

**Fil rouge unique** : une seule et même partie construite de 07 à 14 — *Le Dragonneau*,
un jeu à un bouton inspiré de *Tiny Wings*. Voir la **section 9** pour la spécification
complète (physique, zoom, îles et nuit, thèmes, contraintes matérielles, découpage).

| Leçon | Sujet principal | Game design |
|---|---|---|
| 07 | Fenêtre, boucle de jeu, gravité | 🎮 La boucle update → draw → repeat |
| 08 | Le bouton unique, sprites, animation | 🎮 Un seul verbe, beaucoup de profondeur |
| 09 | Le terrain-tremplin : colonnes, caméra | 🎮 Le monde qui défile |
| 09b | Glisser, décoller, **atterrir** | 🎮 Là où se gagne la vitesse |
| 10 | Caméra qui dézoome, HUD | 🎮 Voir pour décider |
| 11 | Îles et tombée de la nuit | 🎮 Donner une fin au jeu |
| 12 | Écrans multiples + système de thèmes | 🎮 Structure d'un jeu complet |
| 13 | Sons, particules, screen shake | 🎮 Le polish |
| 14 | **Projet : port MakeCode Arcade** | 🎮 Même jeu, deux moteurs |

### Bloc 3 — Lua & Luanti (leçons 15–21) — IDE : VS Code
| Leçon | Sujet principal | Game design |
|---|---|---|
| 15 | Lua vs Python — mêmes idées, syntaxe différente | — |
| 16 | Structure d'un mod, API Luanti de base | 🎮 Minecraft : règles simples, profondeur émergente |
| 17 | Événements, triggers, `on_place` / `on_use` | — |
| 18 | Tables avancées, craft recipes | — |
| 19 | Entités et mobs simples | 🎮 Les mobs comme mécaniques |
| 20 | Génération de terrain, biomes | — |
| 21 | **Projet : mini-mod Luanti complet** | 🎮 Bilan : concevoir une expérience |

---

## 8. Instructions pour Claude Code

Quand tu génères ou modifies du contenu pour ce cours, respecte ces règles :

1. **Toujours consulter ce fichier** avant de créer quoi que ce soit
2. **Un fichier à la fois** — ne pas générer toute une leçon d'un coup sans valider le premier fichier
3. **Tester mentalement** : s'assurer que les exercices sont réalisables par un enfant de 9 ans en moins de 15 minutes chacun
4. **Pas de solutions dans les exercices de logique** — pour les formules du bloc 2, voir
   « Doser la difficulté d'un TODO » (section 2) : là, la ligne est donnée ou à trous
5. **Le fichier `CORRECTION.md` est séparé** et doit être rappelé à chaque leçon générée
6. **Respecter la palette de couleurs exacte** définie dans la section HTML
7. **Signaler** si une leçon risque de dépasser 2 heures au total
8. **Lancer le jeu après chaque TODO** (bloc 2) — avec 0, puis 1, puis 2… TODO faits,
   dans l'ordre. Aucun ne doit planter ; noter dans `CORRECTION.md` ce que chaque
   étape montre à l'écran

### Commande type pour démarrer une leçon
> "Crée la leçon 01 du cours selon COURS_FORMAT.md. Commence par `presentation.html`, attends ma validation avant de générer les exercices."

---

## 9. Bloc 2 — spécification du jeu fil rouge

### 9.1 Le jeu

**Le Dragonneau** — un dragon trop jeune pour voler. Il ne peut que se laisser tomber :
il plonge dans les pentes pour prendre de la vitesse et décolle au sommet des collines.
Un seul bouton (`ESPACE`) : le tenir = plonger lourd, le relâcher = planer.

Inspiré de *Tiny Wings*. Le thème « apprendre à voler » colle exactement à la mécanique :
le héros ne vole jamais vraiment, il exploite le relief. C'est le jeu, et c'est l'histoire.

### 9.2 Contraintes matérielles — à respecter dès la leçon 07

Le jeu est porté sur **ElecFreaks Retro (MakeCode Arcade)** à la leçon 14. Ces contraintes
sont adoptées dès le début pour que le port soit mécanique plutôt qu'une réécriture.

| Contrainte | Valeur | Pourquoi |
|---|---|---|
| Résolution logique | **160 × 120** | Ce que MakeCode Arcade dessine (l'écran fait 160×128, les 8 derniers pixels sont réservés) |
| Fenêtre PC | **640 × 480** (×4) | Pixel art lisible, `pygame.transform.scale` d'une surface 160×120 |
| Couleurs | **16 maximum**, palette fixe | Contrainte Arcade (4 bits/pixel) |
| MCU | STM32F401 — **512 KB flash, 96 KB RAM** | Le framebuffer seul mange ~10 KB de RAM |
| Boutons | **A** uniquement pour le gameplay | Un seul verbe |
| Images | Aucun gros asset | Le flash est la ressource rare — voir 9.6 |

⚠️ **Le code Python ne migre pas.** Le format `.uf2` est un conteneur de flashage, pas un
runtime : la console n'a ni CPython ni SDL. C'est le **design** qui migre. La leçon 14
réécrit le jeu en MakeCode Arcade — et c'est précisément la leçon (*même jeu, deux moteurs*).

### 9.3 Le moteur physique

Tout le jeu tient dans ces lignes. Elles sont introduites progressivement de 07 à 09b.

> ⚠️ **Ces constantes sont calibrées par simulation — ne pas les improviser.** Elles ont
> été réglées par balayage numérique pour satisfaire les quatre critères de 9.3.1. Des
> valeurs « qui ont l'air raisonnables » donnent un jeu où le dragonneau ne décolle
> jamais, ou bien un jeu qui se gagne en tenant le bouton.

```python
LARGEUR, HAUTEUR = 160, 120

L_COLLINE        = 200      # longueur d'une colline, en px
R_DESCENTE       = 0.62     # part de la colline occupée par la descente
CRETE            = 46       # y du sommet (constant : les collines se raccordent)
D_MIN, D_MAX     = 30, 65   # dénivelé — tiré au sort par colline
POINTE           = 2.2      # netteté du sommet

GRAVITE          = 0.08     # chute normale (planer)
GRAVITE_PLONGEON = 0.30     # bouton tenu
ACCEL_DESCENTE   = 0.22     # gain de vitesse en descente
FREIN_MONTEE     = 0.28     # perte en montée — VOLONTAIREMENT > ACCEL_DESCENTE
BONUS_PLONGEON   = 2.6      # × l'accélération si bouton tenu EN DESCENTE
MALUS_PLONGEON   = 3.5      # × le freinage    si bouton tenu EN MONTÉE
FRICTION         = 0.997
VX_MIN, VX_MAX   = 1.2, 9.0
SUIVI_CAMERA     = 0.14


def hauteur_du_sol(x):
    """Le y du sol à la position x. y=0 en haut de l'écran.
       Descente longue et douce, puis remontée « en goutte » :
       le sommet est ARRONDI, mais la courbure culmine AVANT lui."""
    i = int(x // L_COLLINE)                          # numéro de la colline
    d = D_MIN + (D_MAX - D_MIN) * ((i * 7919) % 1000) / 1000
    t = (x % L_COLLINE) / L_COLLINE
    if t < R_DESCENTE:                               # la descente, en cosinus
        u = t / R_DESCENTE
        return CRETE + d * (1 - math.cos(math.pi * u)) / 2
    u = (t - R_DESCENTE) / (1 - R_DESCENTE)          # la remontée « en goutte »
    return CRETE + d * math.cos(math.pi * u / 2) ** POINTE
```

À chaque image :

```python
vy += GRAVITE_PLONGEON if bouton_tenu else GRAVITE
y  += vy

sol = hauteur_du_sol(camera_x)
if y >= sol:                                       # au sol
    y = sol
    pente = hauteur_du_sol(camera_x + 1) - sol     # > 0 = ça descend

    if not au_sol_avant:                           # ATTERRISSAGE
        vx = (vx + vy * pente) / (1 + pente * pente)
        vx = max(VX_MIN, min(VX_MAX, vx))

    vy = pente * vx                                # suivre la pente

    # LE BOUTON AGIT AUSSI AU SOL — c'est là qu'est le jeu
    if pente > 0:      # descente : appuyer = se coller à la pente
        accel = ACCEL_DESCENTE * (BONUS_PLONGEON if bouton_tenu else 1.0)
    else:              # montée   : appuyer = s'écraser dans la côte
        accel = FREIN_MONTEE * (MALUS_PLONGEON if bouton_tenu else 1.0)
    vx = max(VX_MIN, min(VX_MAX, (vx + pente * accel) * FRICTION))

au_sol_avant = y >= sol
camera_x += vx
```

Tout ce qui se dessine est ensuite décalé de `- camera_y` : le sol et le héros.

#### Les trois mécanismes, et pourquoi ils sont là

**1. Le bouton agit au sol — c'est le geste central du jeu.**
Tenir dans la **descente** multiplie l'accélération par `BONUS_PLONGEON` : le dragonneau se
colle à la pente et prend beaucoup de vitesse. Tenir dans la **montée** multiplie le
freinage par `MALUS_PLONGEON` : il s'écrase dans la côte. Le geste à apprendre est donc
*appuyer en descendant, relâcher avant l'horizontale*.

Mesuré : tenir en descente fait **2,52×** la distance de « ne jamais appuyer » et **1,85×**
celle de « tenir tout le temps » ; tenir en montée fait **0,86×** — donc **pire que ne rien
faire**. C'est exactement la hiérarchie de l'original.

Sans cette règle, le bouton n'a d'effet qu'en vol et la glisse est entièrement passive.

**2. La forme du sommet décide du décollage.** On quitte le sol quand
`courbure × vx² / 2 > gravité` — donc au point de **courbure maximale**. La question est :
*quelle est la pente à cet endroit ?* Sur un sinus, la courbure culmine au sommet exact, là
où la pente vaut 0 : le dragonneau décolle avec `vy = pente × vx ≈ 0`, c'est-à-dire pas du
tout.

La remontée **« en goutte »** (`cos(π·u/2)^POINTE`) place la courbure maximale *avant* le
sommet, là où la pente vaut encore **0,44**. Le sommet reste visuellement arrondi — aucun
coin, aucun segment droit. Une rampe droite donnait 0,39 pour un rendu bien plus laid : la
goutte est meilleure sur les deux plans.

| Forme | Saut de pente (coin visible) | Pente au décollage |
|---|---|---|
| **goutte** | **0,009** | **0,44** |
| tremplin (rampe droite) | 0,393 | 0,39 |
| arrondi | 0,441 | 0,24 |
| vague (sinus déformé) | 0,022 | 0,03 |

**3. `FREIN_MONTEE > ACCEL_DESCENTE`.** Si monter coûtait moins que descendre ne rapporte,
rester collé au sol serait toujours gagnant. En rendant la montée plus chère, la seule
façon de progresser est de **survoler la côte suivante**.

**4. L'atterrissage, c'est là qu'est la compétence.**
`vx = (vx + vy × pente) / (1 + pente²)` — seule la composante de la vitesse **parallèle au
sol** survit à l'impact ; la composante perpendiculaire est perdue.

- Retomber *aligné* sur une descente → `vy × pente > 0` → on **gagne** de la vitesse
- S'écraser de plein fouet dans une rampe → `pente < 0` → on perd presque tout

Mesuré sur le code livré de la leçon 09b (6 000 images, 2026-10-23) : **avec** la formule,
tenir en descente donne 34 790 px contre 13 657 px en jeu passif, soit **2,55×** ; **sans** elle,
28 405 px, soit 2,06×. Viser son atterrissage vaut donc environ un quart de la compétence.

> Les valeurs 1,12× → 3,15× qui figuraient ici dataient d'avant la règle « le bouton agit aussi
> au sol ». À l'époque le bouton n'avait aucun effet pendant la glisse, donc tout reposait sur
> l'atterrissage. Les deux mécanismes se partagent désormais le mérite — la formule reste la
> ligne la plus importante du jeu.

**Les collines varient.** Le dénivelé est tiré par numéro de colline. Avec des collines
identiques, le joueur se cale dans un rythme régulier et n'a plus rien à décider — mesuré :
l'écart avec le jeu habile tombe à 1,12×. La variation force à viser chaque atterrissage.

#### 9.3.1 Résultats mesurés (simulation sur 6 000 images)

Ces chiffres servent de test de non-régression : si un réglage change, les revérifier.
Revérifiés le 2026-10-23 sur `lecon_09b/jeu.py` ; les deux dernières lignes ont bougé de 1 %
(18 606 et 34 440 à l'origine, sur le prototype).

| Stratégie | Distance | % en vol | Rapport |
|---|---|---|---|
| Tenir **en montée** | 11 747 | 7 % | **0,86×** — pire que ne rien faire |
| Ne jamais appuyer | 13 657 | 45 % | 1,00× (référence) |
| Tenir tout le temps | 18 809 | 29 % | 1,38× |
| **Tenir en descente** | **34 790** | **67 %** | **2,55×** |

La hiérarchie est celle demandée : le bon geste domine, et **appuyer en montée est puni**.

Hauteur de vol maximale **225 px** — presque deux écrans. Le zoom arrière de 9.4 n'est donc
pas un ornement : sans lui, on ne voit plus le sol au sommet d'un vol.

### 9.4 La caméra qui dézoome

**Obligatoire, pas décoratif.** Les vols montent jusqu'à 225 px au-dessus du sol alors que
l'écran fait 120 px de haut. Sans zoom arrière, au sommet d'un vol on ne voit plus que du
ciel — et comme toute la compétence consiste à **choisir où retomber**, un joueur qui ne
voit pas le sol ne joue plus. Le zoom rend la décision possible ; la sensation de monter
haut vient en prime.

Le zoom obéit à **deux règles superposées**, et c'est ce qui résout une tension réelle :
garder le sol visible pousse à dézoomer tôt, le confort de jeu demande de dézoomer tard.

```python
ZOOM_MIN     = 0.30
SEUIL_ZOOM   = 50           # altitude SOUS laquelle on ne zoome pas du tout
HAUTEUR_ZOOM = 190          # altitude à laquelle le zoom est complètement ouvert
SUIVI_SORTIE = 0.07         # vitesse pour s'éloigner
SUIVI_RETOUR = 0.10         # vitesse pour revenir
MARGE_SOL    = 8            # px de sol qu'on garantit à l'écran
VISEE_BAS    = 60           # hauteur du héros à l'écran quand il est au sol
VISEE_HAUT   = 26           # ... et quand il est très haut

# L'altitude se mesure au-dessus de la LIGNE DES CRÊTES, jamais au-dessus
# du sol qui passe sous le héros — voir l'encadré plus bas.
hauteur_de_vol = max(0.0, CRETE - y)

# 1. LE CONFORT — rien tant qu'on vole bas, puis une rampe douce
if hauteur_de_vol <= SEUIL_ZOOM:
    k = 0.0
else:
    k = min(1.0, (hauteur_de_vol - SEUIL_ZOOM) / (HAUTEUR_ZOOM - SEUIL_ZOOM))
confort = 1.0 - (1.0 - ZOOM_MIN) * k
zoom += (confort - zoom) * (SUIVI_SORTIE if confort < zoom else SUIVI_RETOUR)

# On lisse la VISÉE, pas la caméra
visee += (VISEE_BAS + (VISEE_HAUT - VISEE_BAS) * k - visee) * SUIVI_CAMERA

# 2. LE PLAFOND DE SÉCURITÉ — formule fermée, pas de circularité
plafond = (HAUTEUR - MARGE_SOL - visee) / max(1.0, CRETE - y)
zoom = max(0.12, min(1.0, plafond, zoom))

# 3. La caméra se DÉDUIT — le héros est pile à `visee` du haut de l'écran
camera_y = y - visee / zoom
```

⚠️ **Le `0.12` est devenu `0.06` à la leçon 12** (`ZOOM_PLANCHER` dans `partie.py`). Un très
bon joueur vole jusqu'à 1 200 px sur les collines raides des îles 3–4, bien au-delà des
190 px prévus ici : bloquée à 0,12, la caméra laissait le sol sortir de l'écran (1,8 % des
images pour un expert, 9,8 % sur la Lune). À 0,06 : 0 % et 2,5 %. Le héros ne rapetisse
pas plus (taille minimale de 6 px). Les leçons 10 et 11 gardent 0,12.

**Le plafond rend la perte du sol impossible par construction**, quels que soient les
réglages de confort. On peut donc régler la rampe purement à la sensation. Il est actif
~20 % du temps (uniquement en vol haut) et reste continu — aucun à-coup visible.

⚠️ **Ne jamais lisser `camera_y` séparément.** C'est tentant (ça donne un joli retard de
caméra) mais ça casse deux choses : le plafond se calcule alors sur une position périmée
d'une image, et surtout la position du héros à l'écran n'est plus garantie par rien — il
sortait par le bas de 10 px. En lissant la **visée** et en déduisant la caméra, la position
du héros est exactement `visee`, donc bornée par construction entre `VISEE_HAUT` et
`VISEE_BAS`. Vérifié : 26,3 à 60,0 px, jamais en dehors.

⚠️ **L'altitude doit se mesurer au-dessus des CRÊTES, pas du sol sous le héros.**
C'est la cause du « sol qui monte et descend sans arrêt » ressenti en redescendant d'un
haut vol. À grande vitesse, `hauteur_du_sol(camera_x)` balaie tout le dénivelé d'une
colline : l'altitude calculée tremble de 65 px alors que le dragonneau ne bouge presque
pas, et le zoom, la visée et le plafond copient tous les trois ce tremblement.

`CRETE` est une constante (les collines se raccordent toujours à la même hauteur), donc
la mesure est parfaitement lisse. Mesuré sur les redescentes de haut vol, en inversions du
sens du zoom pour 100 images — c'est ce que l'œil perçoit comme instable :

| Référence utilisée | Inversions / 100 images |
|---|---|
| Sol sous le héros (naïf) | 9,1 |
| Sol sous le héros, filtré | 10,7 |
| **Ligne des crêtes** | **2,2** |

> Mesuré de nouveau le 2026-10-23 sur `lecon_10/jeu.py` : dans la configuration de la leçon,
> l'écart est bien **plus modeste** — la mesure prise sur le sol qui défile saute de 3,7 px par
> image contre 2,6 px sur la ligne des crêtes (pointes à 15 contre 9), et le zoom lissé change
> de sens 3,1 fois contre 2,8 par 100 images actives. Les 9,1 ci-dessus viennent du prototype,
> mesurés uniquement pendant les redescentes de très haut vol et à des vitesses supérieures.
> La raison de garder `CRETE` tient donc surtout à ce que la mesure est **stable par
> construction** : ne pas survendre l'effet auprès de l'apprenant.

Vérifié sans aucune perte du sol sur toute la plage `GRAVITE` de 0,05 à 0,14, altitude
maximale 276 px, héros toujours à l'écran.

Le monde se convertit alors en coordonnées d'écran avec le zoom :

```python
ecran_y = (monde_y - camera_y) * zoom
monde_x = camera_x + (ecran_x - X_HEROS) / zoom
```

⚠️ **La visée doit varier, pas seulement le zoom.** Quand le dragonneau monte, il faut
aussi le faire glisser vers le **haut** de l'écran pour libérer de la place sous lui.
Mesuré : à visée fixe (60), le sol n'est visible que 53 à 93 % du temps en vol haut
malgré le zoom ; avec la visée variable (60 → 26), **100 %**.

**Pourquoi `SEUIL_ZOOM`.** Sans seuil, la moindre bosse déclenche un mouvement de caméra et
le zoom « pompe » en permanence pendant les enchaînements. Avec un seuil à 50 px, le zoom
reste complètement inactif **44 %** du temps (contre 28 % sans seuil) : les petits sauts se
jouent à l'échelle normale, et le dézoom devient un événement qui signale *« là, tu montes
vraiment haut »*.

**Sur la console**, MakeCode Arcade ne sait pas redimensionner librement : les sprites sont
des images de taille fixe. Le port de la leçon 14 utilisera donc **trois paliers discrets**
(1.0 / 0.65 / 0.45) avec deux tailles de sprite pour le héros (16×16 et 8×8). Le terrain,
lui, est dessiné en colonnes — il se met à l'échelle sans rien changer.

C'est un bon sujet de discussion pour le port : *qu'est-ce qu'on coupe quand la machine ne
peut pas suivre ?* Le palier discret se lit comme un choix, pas comme un défaut.

### 9.5 Les îles et la nuit

Les deux mécaniques qui donnent une **fin** au jeu. Sans elles, on glisse indéfiniment.

#### La nuit — la mécanique de fin

C'est celle de l'original. L'auteur la décrit ainsi sur son site :

> "Watch out for the night and fly as fast as you can."

Un compteur `heure` avance à chaque image. Le ciel passe progressivement du jour au
crépuscule puis à la nuit ; quand il fait complètement noir, la partie est finie.

```python
VITESSE_NUIT = 0.00015          # calibré 2026-10-23, voir plus bas
FACTEUR_ILE = 0.35
BONUS_ATTERRISSAGE = 0.004      # × la vitesse GAGNÉE, pas un forfait

heure += VITESSE_NUIT * (1 + FACTEUR_ILE * numero_ile)   # accélère par paliers

if vx > avant:                  # l'atterrissage lui a rendu de la vitesse
    heure = max(0.0, heure - BONUS_ATTERRISSAGE * (vx - avant))
```

**La vitesse est le mécanisme principal, le bonus est une prime.** La nuit compte les
*images*, pas les mètres : aller vite est donc la vraie façon de la devancer. Chaque
atterrissage qui *gagne* de la vitesse (voir 9.3) rend en plus un peu de jour.

⚠️ **Le bonus doit rester petit, et proportionnel au gain.** Mesuré sur le code livré de la
leçon 11 : avec un bonus **forfaitaire** assez gros pour se sentir, « tenir le bouton tout le
temps » redevient la meilleure stratégie — rester collé au sol multiplie les atterrissages,
donc les bonus, et ça écrase le geste de la 09b.

| Réglage du bonus | Ne jamais | Tenir tout le temps | Tenir en descente |
|---|---|---|---|
| **0,004 × le gain** (retenu) | 1 136 m | 1 655 m | **2 168 m** ✅ |
| 0,02 forfaitaire | 1 348 m | **2 554 m** ❌ | 2 189 m |
| 0,035 forfaitaire | 1 392 m | **3 851 m** ❌ | 2 850 m |

La promesse « seul l'enchaînement de bons atterrissages rend du jour » est donc tenue en
version **faible** : elle ne peut pas porter le jeu à elle seule sans casser la hiérarchie du
bouton.

**Résultat d'une partie complète** (leçon 11, mesuré) : jeu passif 86 s et 1 136 m (île 3) ;
bouton tenu en permanence 96 s et 1 655 m (île 5) ; bouton tenu en descente 70 s et 2 168 m
(île 6). Le bon joueur meurt **plus tôt** et va **plus loin** — c'est voulu, le score est la
distance.

Rendu : c'est une **interpolation entre deux palettes** — palette jour et palette nuit du
thème courant. Quelques octets sur la console, et ça réutilise exactement le système de
thèmes de 9.6. Les étoiles apparaissent quand `heure > 0.6`.

#### Les îles

Une île se lit de gauche à droite : **plage → collines ordinaires → grande descente
bosselée → petite remontée → océan**. Longueur fixe de 4 800 px (affiché « 480 m »).

```
  plage      collines ordinaires       grande descente   tremplin   OCÉAN
  ~~~~/‾‾\__/‾‾\__/‾‾\__/‾‾\__/‾‾\__  \_/‾\_/‾\_/‾\_ ___ /‾‾‾‾‾~~~~~~~~~~~~
  400 px     ~15 collines              4 collines        60 px      500 px
```

- **Difficulté croissante** : le creux maximal grandit (65 → 110) et les collines rétrécissent
  (200 → 120 px) à chaque île.
- **La nuit accélère d'un palier** à chaque île.
- **La grande descente** fait plonger la ligne de crête de 48 px vers la mer sur 4 collines,
  pendant que les bosses s'effacent (`creux × (1 - part)^1.5`) : on finit sur une courbe lisse.
  C'est elle qui donne la vitesse du saut.
- **La petite remontée** (26 px, en `sin^1.6`) sert de tremplin et reste **22 px sous la ligne
  des crêtes** — pas une tour. Son bord tombe de 40 px dans la mer : c'est la seule
  discontinuité voulue du terrain.
- **Mesuré** : en plongeant dans les descentes, le saut dure **2,02 s** et franchit les 500 px
  d'un trait, 4 fois sur 4. En jeu passif ou bouton tenu en permanence, **aucun** saut n'est
  franchi — on tombe à l'eau et on rame. Le grand saut est donc la récompense du geste de 9.3.
- ⚠️ **Le nombre de collines doit être entier.** 3 840 / 200 = 19,2 : sinon la dernière est
  coupée en plein milieu et laisse une falaise de 27 px. La longueur réelle se déduit du
  nombre : `nombre = round(zone / longueur_voulue)`, puis `longueur = zone / nombre`.
- ⚠️ **L'eau se reconnaît à sa POSITION, jamais à sa hauteur.** Le fond des vallées descend
  plus bas que la mer : un test en hauteur peint des bandes d'eau en pleine terre.
- ⚠️ **Au-dessus de la mer, le garde-fou du zoom (9.4) doit prendre la MER comme référence**,
  pas la ligne des crêtes — sinon l'eau sort par le bas de l'écran au sommet du saut. Elle est
  parfaitement plate, donc la mesure ne tremble pas.
- ⚠️ **Les îles ne dérivent pas vers le bas.** La mer est le repère fixe : chaque île plonge
  vers elle et la suivante remonte depuis elle. `CRETE` reste donc constante partout — ce dont
  le zoom de 9.4 a besoin.
- **Taille d'écran, pas de goût** : un saut de 3 s (comme l'original) demanderait un apex de
  330 px, donc un zoom de 0,22 et un héros de 4 px. L'original tourne en 320 × 480. À
  160 × 120, 2 s est le maximum qui laisse voir son personnage (héros à 6 px au sommet).

**Le dernier saut de chaque île ne peut pas échouer.** La dernière colline est spéciale :
descente très longue et rampe surdimensionnée. Le dragonneau arrive donc à pleine vitesse
et traverse l'océan jusqu'à l'île suivante quoi qu'il fasse. Mais il y arrive **très vite**,
et un atterrissage réussi sur la nouvelle île lance l'île entière du bon pied.

C'est un moment de respiration offert entre deux montées de difficulté — le joueur ne peut
pas le rater, mais il peut le rentabiliser.

### 9.6 Le système de thèmes

Un thème est un **dictionnaire** (rappel direct de la leçon 05). En MakeCode, c'est un
simple `image.setPalette()` — donc l'idée migre telle quelle, et un thème coûte ~48 octets
de flash au lieu d'un spritesheet.

```python
THEME_DRAGON = {
    "nom":       "Dragonneau",
    "ciel":      (40, 30, 70),
    "collines":  (60, 140, 70),
    "ombre":     (35, 95, 50),
    "heros":     (232, 92, 56),
    "gravite":   0.14,
}
```

Un thème peut changer des valeurs de **gameplay**, pas seulement des couleurs — le thème
Lune baisse `gravite` (0,037 contre 0,06 depuis le recalibrage de la leçon 12, § 9.10).
C'est le moment où Adam comprend qu'une donnée peut piloter le comportement.

⚠️ Cette section disait 0.08 : c'était la gravité **normale** des leçons 09b–11, donc la Lune
n'aurait rien changé. Mesuré : à gravité réduite d'un tiers, vols plus hauts, distances
quasi identiques. La Lune se joue autrement sans fausser les records.

### Chaque couleur existe en deux versions : jour et nuit

Depuis la leçon 11, un thème porte une palette de **jour** et une palette de **nuit**, et le
rendu mélange les deux selon `heure`. Valeurs du thème Dragonneau, calibrées le 2026-10-23 :

| | ciel | collines | ombre | eau | héros | aile | contour |
|---|---|---|---|---|---|---|---|
| **jour** | `134,187,243` | `70,151,78` | `48,118,63` | `53,129,195` | `222,88,54` | `162,50,38` | `25,24,37` |
| **nuit** | `42,59,76` | `15,32,16` | `5,13,7` | `16,39,60` | `169,67,41` | `121,37,29` | `7,7,11` |

Les trois autres thèmes ont été calculés à la leçon 12 de la même façon : une teinte de
départ par couleur, une clarté visée à midi et à minuit. Valeurs complètes dans
`lecon_12/themes.py`, mesures dans `lecon_12/CORRECTION.md`.

| Thème | Débloqué à | `gravite` | Particularité |
|---|---|---|---|
| 🐉 **Dragonneau** | 0 m | 0.06 | — |
| 🎿 **Ski** | 900 m | 0.06 | neige **plus claire** que le ciel à toute heure ; la mer est un lac gelé |
| 🐬 **Dauphin** | 1 500 m | 0.06 | tout est bleu : tout repose sur la clarté. Ciel de nuit éclairci (L\* 26) pour garder eau et vagues distinctes |
| 🚀 **Lune** | 3 000 m | **0.037** | ciel noir de jour comme de nuit ; la nuit se lit au sol et aux étoiles |

⚠️ **Deux couleurs voisines ne doivent jamais changer d'ordre de clarté au cours de la
journée** (le ciel plus clair que les collines à midi, mais plus sombre à minuit) : elles se
croiseraient forcément à une heure donnée, avec un écart de 0. Seule exception : le héros,
qui a son contour.

#### La règle de lisibilité, mesurée

On ne juge pas une palette de cycle jour/nuit à l'œil sur une seule image. La mesure utile est
l'écart de **clarté perceptuelle** ΔL\* entre deux éléments voisins, pris au **pire moment du
cycle** (5 = limite du visible, 10 = écart net) :

| | palette d'origine | palette calibrée |
|---|---|---|
| collines / ciel | 9,3 | **13,8** |
| bande d'ombre / collines | 5,3 | 7,3 |
| eau / ciel | 3,8 | 9,3 |
| clarté du ciel de jour | L\* 13 (nuit déguisée en jour) | L\* 74 |

⚠️ **Le héros ne peut pas y échapper : il faut un contour.** Le ciel balaie toute la plage de
clarté au fil de la journée, donc il passe forcément par celle du dragonneau — mesuré, l'écart
héros / ciel tombe à **0** vers `heure = 0,5`. Un **contour d'un pixel** (dessiné
automatiquement autour du sprite) garde un écart d'au moins 22 avec le ciel à toute heure.
Même raison pour le HUD : ombre d'un pixel sous le texte, plaque sombre derrière les jauges.

⚠️ **Les étoiles se tirent au hasard, pas avec un modulo.** `(i * 6151) % 160` et
`(i * 3119) % 60` donnent un pas constant de (+71, −1) entre deux étoiles consécutives : 39
fois sur 39, donc des diagonales parfaitement régulières. `random.Random(graine)` donne la
même reproductibilité sans la grille, et un éclat tiré par étoile évite l'effet pochoir.

Les thèmes se débloquent au **record** (la meilleure distance, gardée dans `record.txt`) — ça
justifie le système au lieu d'en faire un gadget. Seuils mesurés sur 20 parties par joueur
automatique, avec le réglage recalibré (§ 9.10, une île = 560 m) :

| | Distance (médiane) | Ski 900 | Dauphin 1 500 | Lune 3 000 |
|---|---|---|---|---|
| ne jamais appuyer | 455 m | — | — | — |
| tenir tout le temps | 700 m | — | — | — |
| plonge, maladroit | 828 m | 10 % | — | — |
| plonge, précis | 1 638 m | 100 % | 85 % | — |
| vise son atterrissage, avec erreurs | 3 218 m | 100 % | 100 % | 70 % |
| vise bien | 3 801 m | 100 % | 100 % | 100 % |

⚠️ **Un seuil atteignable sans effort est gratuit.** Chaque seuil est placé juste au-dessus
d'une stratégie à dépasser : Ski au-dessus de « tenir tout le temps ». Une première version
(Ski à 1 300 m, avant le recalibrage) se débloquait en tenant le bouton : refusé par le père.

### 9.7 Fichiers d'une leçon du bloc 2

Le fil rouge ne casse pas la règle « chaque dossier est autonome ». **`jeu.py` d'une leçon
contient l'état terminé de la leçon précédente**, avec les nouveaux `TODO` insérés. Adam
qui décroche une semaine reprend au bon endroit sans dette.

```
lecon_09/
├── presentation.html     ← support animé par le père
├── jeu.py                ← le fil rouge + les TODO de cette leçon
├── themes.py             ← (à partir de la leçon 11)
└── CORRECTION.md         ← solution + pièges attendus (père seulement)
```

**Pas de `tests.py` dans le bloc 2.** La validation se fait par **checklist visuelle**
dans `presentation.html` — une section « ✅ Ça doit faire ça » listant des comportements
observables :

```
☐ Le dragonneau tombe et s'arrête sur la colline
☐ Tenir ESPACE le fait plonger plus vite
☐ Il accélère en descente, ralentit en montée
☐ Il décolle au sommet d'une bosse
```

C'est fidèle au vrai développement de jeu : on regarde l'écran, pas un rapport de tests.

**Découpage en modules** — le fichier est scindé au fur et à mesure plutôt que de laisser
grossir un `jeu.py` de 300 lignes (illisible à 9 ans, et pénible à faire défiler) :

| Leçon | Fichiers d'Adam |
|---|---|
| 07 → 09b | `jeu.py` seul (~120 lignes) |
| 10 | `jeu.py` + `terrain.py` |
| 11 | + `themes.py` |
| 12 | `jeu.py` **seul modifié** ; + `partie.py` (le jeu 07–11 en fonctions) et `ecrans.py` (menu, fin, record), fournis |
| 13 | + `effets.py` |

⚠️ **À la leçon 12, `jeu.py` a été vidé** : 489 lignes en leçon 11, 219 en leçon 12. Le jeu des
leçons 07 à 11 est rangé dans `partie.py` (`nouvelle_partie`, `avancer`, `dessiner_partie`,
`distance`), et `jeu.py` ne garde que les écrans et les TODO. Vérifié : même distance
(2 362 m) et nuit noire à la même image qu'en leçon 11. Les leçons suivantes partent de cette structure.

Chaque module correspond à un *namespace* MakeCode — le découpage sert le port autant que
la lisibilité, et il réactive la leçon 06 (modules et `import`).

### 9.8 Budget mémoire

Le flash est la ressource rare (l'utilisateur a déjà dû recompiler avec d'anciennes
versions de MakeCode pour faire tenir certains jeux). Le design l'évite par construction :

- **Terrain procédural** — deux `sin`, zéro octet d'assets
- **Thèmes = palettes** — pas de spritesheets alternatifs
- **Sprites** — le dragonneau seul, 16×16, 2 images d'animation
- **Sons** — générés (bips MakeCode), pas de fichiers `.wav` embarqués

Si le jeu ne compile pas à la leçon 14, couper dans cet ordre : particules, puis thèmes
supplémentaires, puis animation du héros.

### 9.9 Découpage leçon par leçon

| # | Ce qu'Adam écrit | Ce qu'il voit à la fin |
|---|---|---|
| **07** | Fenêtre 160×120 ×4, boucle, `vy += GRAVITE`, sol plat | Un dragonneau tombe et rebondit sur un sol plat |
| **08** | `pygame.event` → bouton tenu, sprite 16×16, animation 2 images | Tenir ESPACE le fait plonger ; il bat des ailes |
| **09** | `hauteur_du_sol(x)` en tremplins, dessin en colonnes, `camera_x`, `camera_y` | De vraies collines défilent sous lui |
| **09b** | `y >= sol`, `pente`, suivi de pente, **formule d'atterrissage** | **Le vrai gameplay** : il glisse, décolle, et rate ses atterrissages |
| **10** | Zoom lié à l'altitude, HUD vitesse + distance | Il monte *haut* — et on voit enfin où il va retomber |
| **11** | Compteur `heure`, palettes jour/nuit, îles, saut d'océan | Le jeu a une **fin** : la nuit le rattrape |
| **12** | États menu/jeu/game over, dict de thèmes | Menu, game over, 4 thèmes déblocables |
| **13** | Sons, particules, screen shake, **ailes repliées en plongeon** | Ça devient *satisfaisant* |
| **14** | Réécriture MakeCode Arcade + `.uf2` | **Son jeu tourne sur la console** |

⚠️ **Les ailes battent en permanence, y compris pendant le plongeon — c'est voulu, ne
pas « corriger » avant la leçon 13.** Observé par le père en jouant la leçon 09 le
2026-11-10. Ce n'est pas un bug : `animation += VITESSE_AILES` s'exécute à chaque image
sans regarder le bouton, et le prototype de référence fait pareil (il ne fait varier que la
*vitesse* du battement, `0.25` au sol contre `0.12` en vol, jamais selon le bouton).

Ça raconte même la prémisse du jeu : le dragonneau est *trop jeune pour voler*, il bat des
ailes sans que ça le porte.

La ligne vit dans quatre `jeu.py` (09, 09b, 10, 11) comme code fourni, et c'est Adam qui
l'écrit en 08 (TODO 3). La changer rétroactivement réécrirait donc sa propre ligne et
casserait la règle « `jeu.py` = l'état terminé de la leçon précédente ».

**Décision du père (2026-11-10)** : en faire un exercice de la **leçon 13**, dans la version
« ailes figées pendant le plongeon » :

```python
image = SPRITES[1] if bouton else SPRITES[int(animation) % 2]
```

`SPRITES[1]` est l'image « aile basse ». Elle se lit comme des ailes rabattues, mais ça
reste une image de mi-battement : un **troisième motif 16 × 12 « ailes repliées »** serait
plus propre, et c'est un bon exercice de pixel art pour Adam.

⚠️ La leçon **09b** est la plus dense du bloc : elle contient la formule d'atterrissage,
qui est le cœur du jeu. Prévoir qu'elle déborde et garder la leçon 10 courte en
compensation.

⚠️ **La leçon 10 n'est pas du polish.** Sans le zoom arrière, les vols de la leçon 09b
sortent de l'écran et le joueur ne voit plus le sol — donc ne peut plus viser. 09b et 10
forment une paire ; ne pas les séparer de plusieurs semaines.

⚠️ **Leçons 07 et 08 — le sol plat doit faire rebondir**, pas coller :

```python
if y >= SOL_PLAT:
    y = SOL_PLAT
    vy = -vy * 0.6        # rebond amorti
```

Sans ça, le bouton n'a **aucun effet visible** : la branche « au sol » réécrit `vy` à
chaque image, et le dragonneau reste posé quoi qu'Adam fasse. Le rebond garantit qu'il
passe du temps en l'air dès la leçon 07, donc que `ESPACE` se voit immédiatement. Le
rebond disparaît en 09b, remplacé par le suivi de pente.

### 9.10 Le recalibrage de la leçon 12 — l'écart entre bons et mauvais joueurs

**Le constat du père** (2026-11-11) : dans *Tiny Wings*, ne rien faire ne termine pas l'île 1,
tenir tout le temps finit avant la fin de l'île 2, Adam atteint l'île 5 et le père l'île 7.
Avec le réglage des leçons 09b–11, ne rien faire menait à l'île 3 : le bon joueur n'allait
que **1,6 fois** plus loin que celui qui ne fait rien, contre **7 à 10 fois** dans l'original.

**La cause.** Dans l'original, le bon joueur vit **4 fois plus longtemps** (4 min contre
1 min) : le soleil recule quand on enchaîne de bons coups, et chaque nouvelle île redonne du
jour. Chez nous, rien ne rendait vraiment du jour, et `VX_MIN = 1.2` garantissait à lui seul
1,7 île.

**Le nouveau réglage** (code fourni de la leçon 12, détail dans `lecon_12/CORRECTION.md`),
en deux passes : mesures de l'original, puis essai du père :

- **gravité 0,06**, plongeon 0,16, ACCEL 0,098, FREIN 0,124, FRICTION 0,998, vitesse 0,4 à
  6,0 (une 1re passe à 0,036 a été jugée « trop flottante ») ;
- **îles de 5 600 px**, creux de 50 (+4 par île, max 70) au lieu de 65 (+10, max 110),
  collines raccourcies de 8 px par île (min 150) ;
- **forme d'île** : plateau de départ de 100 px, chaque île **commence par une descente**,
  grande descente de 84 px sur 3 collines, **bosse arrondie** de 60 px, puis la mer ;
- **le grand saut réussit toujours** (comme l'original) : on retombe dans la 1re descente de
  l'île suivante, ~2,4 s de vol, au moins `VITESSE_SAUT` 4.0 ;
- **caméra** : en vol haut, elle garde le **fond des vallées** à l'écran (repère lissé) ;
  au-dessus de la mer et en fin d'île, tout le fond ;
- **jour de 60 s** au départ, nuit +20 % par île ;
- **+15 % de jour par nouvelle île** (+3 % par île de plus) ;
- **le beau coup** : relâché au décollage, plongé en vol, retombé dans une descente, après
  au moins 18 images de vol → +2 % de jour, ×2 puis ×3 en série.

| Joueur automatique | Îles | Durée |
|---|---|---|
| ne jamais appuyer | 0,81 | 60 s |
| tenir tout le temps | 1,25 | 67 s |
| vise son atterrissage, avec erreurs | 5,7 | 2 min 13 |
| vise bien | 6,7 | 2 min 19 |

⚠️ **Récompenser « un atterrissage qui fait gagner de la vitesse » ne suffit pas** : plonger en
vol puis retomber dans une pente en fait gagner, et « tenir tout le temps » le fait sans le
vouloir (mesuré : jusqu'à l'île 11). La règle exige donc d'avoir **relâché au décollage**.
Mesuré : ni le passif ni « tenir tout le temps » ne réussit un seul beau coup.

⚠️ **Mesurer avec des joueurs qui visent.** Un joueur automatique qui plonge « dès qu'il
descend » atterrit en montée une fois sur deux et ne représente pas un bon joueur humain.
Les joueurs qui simulent appuyer / relâcher jusqu'à l'atterrissage et gardent le meilleur
donnent les durées et les distances de l'original.

Écart restant : une partie de bon joueur dure ~2 min 15 (le père, dans l'original : ~4 min).
À juger en jouant. Les leçons 09b–11 gardent l'ancien réglage.
