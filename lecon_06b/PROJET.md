# Projet — Calculatrice graphique style TI-83

## L'idée

Une vraie calculatrice graphique, en Python. Elle est **presque** terminée :
la fenêtre, les boutons, le graphique et le moteur qui lit les expressions
sont déjà écrits.

Ce qui manque, c'est le cœur — **les opérations et la mémoire**. C'est ta part.

```
   mes_operations.py   ← TOI     les cinq opérations de mathématicien
   mon_historique.py   ← TOI     la mémoire et les messages d'erreur
   ─────────────────────────────────────────────────────────────────
   calculator.py       ← fourni  lit "12+3×4" et applique les priorités
   interface.py        ← fourni  la fenêtre, les boutons, le graphique
   projet.py           ← fourni  assemble le tout et démarre
```

Chaque fois que tu finis une fonction, elle s'allume dans la vraie calculatrice.

## Ta part — `mes_operations.py`

Cinq opérations, en te servant de `mpmath` (leçon 06) :

| Fonction | Ce qu'elle doit faire | Bouton correspondant |
|---|---|---|
| `puissance(base, exposant)` | `2^10` = 1024 | `^` et `x²` |
| `racine_carree(nombre)` | `√16` = 4 | `√` |
| `racine_nieme(nombre, indice)` | `3ⁿ√8` = 2 | `ⁿ√` |
| `factorielle(nombre)` | `5!` = 120 | `n!` |
| `tetration(base, hauteur)` | `2↑↑4` = 65536 | `↑↑` |

## Ta part — `mon_historique.py`

Une **liste** et un **dictionnaire**, comme à la leçon 05 :

| Fonction | Ce qu'elle doit faire | Où ça se voit |
|---|---|---|
| `noter(...)` | ajoute un calcul à l'historique | le panneau de droite se remplit |
| `dernier(...)` | le calcul le plus récent | le bouton `Ans` |
| `du_plus_recent(...)` | la liste à l'envers | le plus récent en haut du panneau |
| `MESSAGES` | un dictionnaire d'erreurs → messages | l'écran devient rouge au lieu de planter |
| `message_pour(...)` | va chercher dans `MESSAGES` | idem |

## Comment tester

```
▶ sur mes_operations.py   →  teste tes cinq opérations
▶ sur mon_historique.py   →  teste ta mémoire
▶ sur tests.py            →  teste tout, avec le grand total
▶ sur projet.py           →  ouvre la vraie calculatrice
```

Tu peux ouvrir `projet.py` n'importe quand : la calculatrice démarre même
si tes fonctions ne sont pas finies. Elle affichera simplement
`Opération pas encore écrite` quand tu appuies sur un bouton qui manque.

## Ce que fait la calculatrice terminée

- Chiffres, `+ − × ÷`, parenthèses, et les cinq opérations ci-dessus
- **=** calcule ; ré-appuyer sur **=** refait la dernière opération
- **C** efface tout, **⌫** efface le dernier symbole, **±** change le signe
- **Ans** rappelle le dernier résultat, sans le retaper
- Le panneau de droite garde les 25 derniers calculs — clique dessus pour les réutiliser
- Une division par zéro ou une expression invalide affiche un message rouge, **sans planter**

### Les très grands nombres

- Menu **Décimales** : 15, 30, 50, 100, 500
- Bouton **NORM / SCI** : `2432902008176640000` devient `2.43290200817664e+18`
- Bouton **EE** pour écrire directement `3e8` = 300 000 000
- Sous l'écran, le **nombre de chiffres** d'un résultat énorme
- L'écran est sur plusieurs lignes : rien ne déborde, même à 500 décimales

### Le graphique

- Le bouton **X** ajoute la variable X
- Dès qu'il y a un X, le gros bouton **=** devient **📊**
  (logique : on ne peut pas calculer `X²`, mais on peut le tracer)
- Le graphique s'ouvre dans une nouvelle fenêtre, avec l'intervalle de X réglable

## Exemple de ce que tu devrais voir

```
┌────────────────────────────────────────────┬──────────────┐
│                              X²-4×X+3      │ Historique   │
│                                            │  2↑↑5        │
│  Décimales [30]   NORM     ⌫       C       │  = 2.003…    │
│    x²     ^      √      ⁿ√     ↑↑          │  12+3×4      │
│    n!     π      (      )      ±           │  = 24        │
│    7      8      9      ÷      EE          │              │
│    4      5      6      ×      Ans         │              │
│    1      2      3      −      ═╗          │              │
│    X      0      .      +       ║          │   [ Vider ]  │
└────────────────────────────────────────────┴──────────────┘
```

Quand on tape `2↑↑5` puis `=` :
```
  2.00352993040684646497907235156e+19728
  ≈ 19 729 chiffres
```

Quand on tape `5 ÷ 0` puis `=` :
```
  ❌ Division par zéro !
```

Quand on tape `X²-4×X+3` puis `📊` :
```
  (une parabole s'affiche, qui coupe l'axe en X=1 et X=3)
```

## Critères de réussite

- `python tests.py` affiche **29 / 29**
- La calculatrice démarre et calcule `12+3×4` = 24
- `2↑↑5` répond **tout de suite** au lieu de figer l'ordinateur
- `1÷6` avec 500 décimales s'affiche en entier — l'écran enroule, il ne déborde pas
- Diviser par zéro affiche ton message d'erreur, sans faire planter le programme
- Le panneau d'historique se remplit, et cliquer une ligne réutilise son résultat
- Le bouton `📊` trace `X²-4×X+3`

## Bonus (si tu veux aller plus loin)

- ⭐ Ajouter une opération à toi dans `mes_operations.py` (un logarithme ? un modulo ?)
- ⭐ Une fonction `chercher(historique, texte)` qui filtre les calculs contenant un texte
- ⭐ Le clavier : taper `7` fait la même chose que cliquer sur `7`
- ⭐ Tracer **deux** courbes en même temps pour les comparer
- ⭐ Un mode **ENG** en plus de NORM/SCI : l'exposant est toujours un multiple de 3
