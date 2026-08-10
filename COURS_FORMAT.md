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
> checklist observable dans `presentation.html` — voir la **section 9.5**.

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

**Fil rouge unique** : une seule et même partie construite de 07 à 13 — *Le Dragonneau*,
un jeu à un bouton inspiré de *Tiny Wings*. Voir la **section 9** pour la spécification
complète (physique, thèmes, contraintes matérielles, découpage détaillé).

| Leçon | Sujet principal | Game design |
|---|---|---|
| 07 | Fenêtre, boucle de jeu, gravité | 🎮 La boucle update → draw → repeat |
| 08 | Le bouton unique, sprites, animation | 🎮 Un seul verbe, beaucoup de profondeur |
| 09 | Le terrain : `sin`, colonnes, caméra | 🎮 Le monde qui défile |
| 09b | Glisser sur la pente, décoller | 🎮 Tension et risque |
| 10 | Vitesse, distance, score, HUD | 🎮 Progression et feedback |
| 11 | Écrans multiples + système de thèmes | 🎮 Structure d'un jeu complet |
| 12 | Sons, particules, screen shake | 🎮 Le polish |
| 13 | **Projet : polish + port MakeCode Arcade** | 🎮 Même jeu, deux moteurs |

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

---

## 9. Bloc 2 — spécification du jeu fil rouge

### 9.1 Le jeu

**Le Dragonneau** — un dragon trop jeune pour voler. Il ne peut que se laisser tomber :
il plonge dans les pentes pour prendre de la vitesse et décolle au sommet des collines.
Un seul bouton (`ESPACE`) : le tenir = plonger lourd, le relâcher = planer.

Inspiré de *Tiny Wings*. Le thème « apprendre à voler » colle exactement à la mécanique :
le héros ne vole jamais vraiment, il exploite le relief. C'est le jeu, et c'est l'histoire.

### 9.2 Contraintes matérielles — à respecter dès la leçon 07

Le jeu est porté sur **ElecFreaks Retro (MakeCode Arcade)** à la leçon 13. Ces contraintes
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
runtime : la console n'a ni CPython ni SDL. C'est le **design** qui migre. La leçon 13
réécrit le jeu en MakeCode Arcade — et c'est précisément la leçon (*même jeu, deux moteurs*).

### 9.3 Le moteur physique

Tout le jeu tient dans ces lignes. Elles sont introduites progressivement de 07 à 09b.

> ⚠️ **Ces constantes sont calibrées par simulation — ne pas les improviser.** Elles ont
> été réglées par balayage numérique pour satisfaire les quatre critères de 9.3.1. Des
> valeurs « qui ont l'air raisonnables » donnent un jeu où le dragonneau ne décolle
> jamais, ou bien un jeu qui se gagne en tenant le bouton.

```python
LARGEUR, HAUTEUR = 160, 120
GRAVITE          = 0.14     # chute normale (planer)
GRAVITE_PLONGEON = 0.50     # bouton tenu
ACCEL_DESCENTE   = 0.18     # gain de vitesse en descente
FREIN_MONTEE     = 0.23     # perte en montée — VOLONTAIREMENT > ACCEL_DESCENTE
FRICTION         = 0.997
VX_MIN, VX_MAX   = 1.2, 8.0
SUIVI_CAMERA     = 0.14
HAUTEUR_VISEE    = 60       # où le héros se stabilise à l'écran

def hauteur_du_sol(x):
    """Renvoie le y du sol à la position x. y=0 en haut de l'écran."""
    return 76 + 32 * math.sin(x / 38) + 11 * math.sin(x / 17)
```

À chaque image :

```python
vy += GRAVITE_PLONGEON if bouton_tenu else GRAVITE
y  += vy

sol = hauteur_du_sol(camera_x)
if y >= sol:                                       # au sol
    y = sol
    pente = hauteur_du_sol(camera_x + 1) - sol     # > 0 = ça descend
    vy = pente * vx                                # suivre la pente
    vx += pente * (ACCEL_DESCENTE if pente > 0 else FREIN_MONTEE)
    vx = max(VX_MIN, min(VX_MAX, vx * FRICTION))

camera_x += vx
camera_y += ((y - HAUTEUR_VISEE) - camera_y) * SUIVI_CAMERA
```

Tout ce qui se dessine est ensuite décalé de `- camera_y` : le sol et le héros. Deux
soustractions, pas plus.

**Le décollage n'est pas codé — il émerge.** Au sommet d'une colline, la tangente suivie
par le dragonneau passe au-dessus du terrain qui se dérobe : `y < sol`, donc plus de
contact, donc la gravité reprend. Dans un creux, `y >= sol` reste vrai à chaque image et
la vitesse monte. Aucun cas particulier à écrire.

**Pourquoi `FREIN_MONTEE > ACCEL_DESCENTE`.** C'est le cœur du game design, pas un détail
de réglage. Si monter coûtait moins que descendre ne rapporte, rester collé au sol serait
toujours gagnant et le jeu se gagnerait en tenant le bouton — sans aucune décision. En
rendant la montée plus chère, la seule façon de progresser est de **décoller au sommet et
survoler la côte suivante**. C'est exactement la compétence que *Tiny Wings* demande.

**Le bouton ne fait effet qu'en vol** — au sol, la branche `if` réécrit `vy` à chaque
image. C'est fidèle à l'original : on ne pilote pas la glisse, on choisit *où retomber*.

Les deux `sin` ont des périodes premières entre elles (38 et 17) : le terrain ne se répète
qu'au bout de 4 059 px, soit plus de 15 secondes de jeu à pleine vitesse. Adam peut
modifier les quatre nombres de `hauteur_du_sol` en direct et voir le monde changer.

#### 9.3.1 Résultats mesurés (simulation sur 3 000 images)

Ces chiffres servent de test de non-régression : si un réglage change, les revérifier.

| Stratégie | Distance | % en vol | Vols |
|---|---|---|---|
| Ne jamais appuyer | 5 762 | 26 % | 41 |
| Bouton toujours tenu | 7 036 | 0,5 % | 0 |
| Martelage aveugle | 6 123 | 11 % | 20 |
| **Jeu habile** (plonger vers la descente) | **9 828** | **47 %** | **52** |

Le jeu habile bat le passif **1,71×**, le bouton tenu **1,40×** et le martelage **1,61×** —
il existe donc une vraie compétence, et aucune stratégie bête ne la remplace.

Vol moyen **0,42 s**, vol le plus long **0,83 s** (à 60 fps). Vitesse entre 1,2 et 5,7.
Avec `SUIVI_CAMERA = 0.14`, le héros garde 33 px de marge en haut et 18 px en bas dans le
pire cas, toutes stratégies confondues — il ne sort jamais de l'écran.

### 9.4 Le système de thèmes

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

### 9.5 Fichiers d'une leçon du bloc 2

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

### 9.6 Budget mémoire

Le flash est la ressource rare (l'utilisateur a déjà dû recompiler avec d'anciennes
versions de MakeCode pour faire tenir certains jeux). Le design l'évite par construction :

- **Terrain procédural** — deux `sin`, zéro octet d'assets
- **Thèmes = palettes** — pas de spritesheets alternatifs
- **Sprites** — le dragonneau seul, 16×16, 2 images d'animation
- **Sons** — générés (bips MakeCode), pas de fichiers `.wav` embarqués

Si le jeu ne compile pas à la leçon 13, couper dans cet ordre : particules, puis thèmes
supplémentaires, puis animation du héros.

### 9.7 Découpage leçon par leçon

| # | Ce qu'Adam écrit | Ce qu'il voit à la fin |
|---|---|---|
| **07** | Fenêtre 160×120 ×4, boucle, `vy += GRAVITE`, sol plat | Un dragonneau tombe et rebondit sur un sol plat |
| **08** | `pygame.event` → bouton tenu, sprite 16×16, animation 2 images | Tenir ESPACE le fait plonger ; il bat des ailes |
| **09** | `hauteur_du_sol(x)`, dessin en colonnes, `camera_x`, `camera_y` | De vraies collines défilent sous lui |
| **09b** | Détection `y >= sol`, `pente`, `vy = pente * vx`, accélération | **Le vrai gameplay** : il glisse, prend de la vitesse, décolle |
| **10** | Distance, vitesse, bonus « super glisse », HUD | Ça devient un jeu avec un score |
| **11** | États menu/jeu/game over, dict de thèmes | Menu, game over, 4 thèmes déblocables |
| **12** | Sons, particules, screen shake | Ça devient *satisfaisant* |
| **13** | Réécriture MakeCode Arcade + `.uf2` | **Son jeu tourne sur la console** |

⚠️ La leçon **09b** est la plus dense du bloc. Prévoir qu'elle déborde et garder la
leçon 10 courte en compensation.

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
