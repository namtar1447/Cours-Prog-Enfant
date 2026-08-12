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
- Décrire **ce que le code doit faire**, jamais **comment l'écrire**
- Maximum **5 TODO** par exercice
- Laisser suffisamment d'espace vide entre les TODO pour que l'apprenant écrive
- Un commentaire `# --- EXEMPLE ---` précède toujours la partie à compléter
- Ne jamais donner la réponse dans l'exemple si elle est identique à ce qu'on demande

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
4. **Pas de solutions dans les exercices** — les `TODO` ne doivent jamais contenir de code solution en commentaire
5. **Le fichier `CORRECTION.md` est séparé** et doit être rappelé à chaque leçon générée
6. **Respecter la palette de couleurs exacte** définie dans la section HTML
7. **Signaler** si une leçon risque de dépasser 2 heures au total

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

Sans cette ligne, le jeu n'a aucune profondeur : ne jamais toucher le bouton donne 85 % de
temps en vol et fait presque aussi bien que le jeu optimal. Avec elle, l'écart passe de
1,12× à 3,15×. **C'est la ligne la plus importante du jeu.**

**Les collines varient.** Le dénivelé est tiré par numéro de colline. Avec des collines
identiques, le joueur se cale dans un rythme régulier et n'a plus rien à décider — mesuré :
l'écart avec le jeu habile tombe à 1,12×. La variation force à viser chaque atterrissage.

#### 9.3.1 Résultats mesurés (simulation sur 6 000 images)

Ces chiffres servent de test de non-régression : si un réglage change, les revérifier.

| Stratégie | Distance | % en vol | Rapport |
|---|---|---|---|
| Tenir **en montée** | 11 747 | 7 % | **0,86×** — pire que ne rien faire |
| Ne jamais appuyer | 13 657 | 45 % | 1,00× (référence) |
| Tenir tout le temps | 18 606 | 28 % | 1,36× |
| **Tenir en descente** | **34 440** | **69 %** | **2,52×** |

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
VITESSE_NUIT_BASE = 0.00035
BONUS_ATTERRISSAGE = 0.004      # un bel atterrissage repousse la nuit

heure += VITESSE_NUIT_BASE * (1 + 0.35 * numero_ile)   # accélère par paliers
```

**Seul l'enchaînement permet de devancer la nuit.** Chaque atterrissage qui *gagne* de la
vitesse (voir 9.3, `vx` augmente à l'impact) rend un peu de jour. Un atterrissage raté n'en
rend aucun. La boucle de récompense est donc : bien viser → plus de jour → plus de distance.

Rendu : c'est une **interpolation entre deux palettes** — palette jour et palette nuit du
thème courant. Quelques octets sur la console, et ça réutilise exactement le système de
thèmes de 9.6. Les étoiles apparaissent quand `heure > 0.6`.

#### Les îles

- **Longueur fixe** : 20 collines, soit 4 000 px (affiché « 400 m »)
- **Difficulté croissante** : `D_MAX` grandit et `L_COLLINE` rétrécit à chaque île
- **La nuit accélère d'un palier** à chaque île

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
Lune baisse `gravite` à 0.08. C'est le moment où Adam comprend qu'une donnée peut piloter
le comportement.

Valeurs RGB validées au rendu (les quatre thèmes restent lisibles en 16 couleurs) :

| Thème | ciel → ciel2 | collines / ombre | héros | Particularité |
|---|---|---|---|---|
| 🐉 **Dragonneau** (défaut) | `38,28,66` → `92,52,90` | `58,138,68` / `32,92,48` | `232,92,56` | — |
| 🎿 **Ski** | `28,44,86` → `96,140,190` | `238,244,252` / `168,190,220` | `240,80,70` | — |
| 🚀 **Lune** | `8,8,20` → `40,36,64` | `150,148,158` / `92,90,102` | `238,238,238` | `gravite` 0.08 |
| 🐬 **Dauphin** | `20,60,110` → `88,170,210` | `30,110,170` / `18,72,120` | `190,225,240` | — |

Les thèmes se débloquent à la distance parcourue — ça justifie le système au lieu d'en
faire un gadget.

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
| 12 | + `effets.py` |

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
| **13** | Sons, particules, screen shake | Ça devient *satisfaisant* |
| **14** | Réécriture MakeCode Arcade + `.uf2` | **Son jeu tourne sur la console** |

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
