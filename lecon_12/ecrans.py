# ============================================================
# Leçon 12 — ecrans.py
# ============================================================
# Le DESSIN des deux nouveaux écrans, et le record gardé dans un fichier.
#
#   dessiner_menu(surf, choix, record)   l'écran du menu
#   dessiner_fin(surf, jeu, record)      l'écran de fin de partie
#   lire_record()                        le record gardé la dernière fois
#   sauver_record(record)                le garder pour la prochaine fois
#
# Ces fonctions DESSINENT seulement. C'est jeu.py qui décide quel écran
# montrer, et quand on passe de l'un à l'autre — c'est ton travail
# d'aujourd'hui.
#
# Tu n'as rien à modifier ici.
# ============================================================

import os

import pygame

from partie import (nouvelle_partie, avancer, dessiner_partie, distance,
                    ecrire, ecrire_centre, LARGEUR, HAUTEUR, COULEUR_PLAQUE,
                    COULEUR_SOLEIL)
from themes import THEMES

COULEUR_TITRE   = (255, 214, 102)
COULEUR_GRIS    = (160, 164, 190)
COULEUR_CADENAS = (243, 139, 168)


def plaque(surf, x, y, largeur, hauteur):
    """Un rectangle sombre à moitié transparent, derrière le texte."""
    fond = pygame.Surface((largeur, hauteur), pygame.SRCALPHA)
    fond.fill(COULEUR_PLAQUE + (200,))
    surf.blit(fond, (x, y))


# ============================================================
# Le menu
# ============================================================

# Derrière le menu, un dragonneau glisse tout seul, aux couleurs du thème
# choisi — et avec sa gravité : sur la Lune, il plane plus longtemps.
_vitrine = {"jeu": nouvelle_partie(), "images": 0}
_record_au_menu = [0]            # le record au moment où on a quitté le menu


def dessiner_menu(surf, choix, record):
    theme = THEMES[choix]
    _record_au_menu[0] = record

    vitrine = _vitrine["jeu"]
    avancer(vitrine, False, theme["gravite"])
    vitrine["heure"] = 0.15                      # toujours le matin
    if distance(vitrine) > 300:                  # on recommence la balade
        _vitrine["jeu"] = nouvelle_partie()
    _vitrine["images"] += 1

    dessiner_partie(surf, vitrine, theme, hud=False)

    # Le titre
    plaque(surf, 0, 4, LARGEUR, 20)
    ecrire_centre(surf, "LE DRAGONNEAU", 6, COULEUR_TITRE, 14, True)

    # Le thème choisi, avec les flèches
    plaque(surf, 0, 64, LARGEUR, 42)
    ecrire_centre(surf, f"<   {theme['nom']}   >", 67, taille=11, gras=True)

    # Les petits points : on voit combien il y a de thèmes, et où on est
    depart = LARGEUR // 2 - (len(THEMES) * 8) // 2
    for numero in range(len(THEMES)):
        couleur = COULEUR_TITRE if numero == choix else COULEUR_GRIS
        pygame.draw.circle(surf, couleur, (depart + numero * 8 + 4, 83), 2 if numero == choix else 1)

    if record >= theme["distance"]:
        if _vitrine["images"] // 30 % 2 == 0:    # ça clignote
            ecrire_centre(surf, "ESPACE : jouer", 90)
    else:
        ecrire_centre(surf, f"VERROUILLE - record de {theme['distance']} m", 90, COULEUR_CADENAS)

    plaque(surf, 0, 108, LARGEUR, 12)
    ecrire_centre(surf, f"record : {record} m", 110, COULEUR_GRIS)


# ============================================================
# L'écran de fin
# ============================================================

def dessiner_fin(surf, jeu, record):
    plaque(surf, 10, 18, LARGEUR - 20, 86)
    ecrire_centre(surf, "LA NUIT", 22, taille=14, gras=True)
    ecrire_centre(surf, "T'A RATTRAPE", 37, taille=14, gras=True)
    ecrire_centre(surf, f"{distance(jeu)} m", 56, COULEUR_TITRE, 11, True)

    if record > 0 and distance(jeu) >= record:
        ecrire_centre(surf, "NOUVEAU RECORD !", 70, COULEUR_SOLEIL)

    # Un thème vient de se débloquer ? Sinon, le prochain à aller chercher.
    ancien = _record_au_menu[0]
    debloques = [t["nom"] for t in THEMES if ancien < t["distance"] <= record]
    a_venir = [t for t in THEMES if t["distance"] > record]
    if debloques:
        ecrire_centre(surf, f"Debloque : {', '.join(debloques)} !", 80, COULEUR_SOLEIL)
    elif a_venir:
        prochain = a_venir[0]
        ecrire_centre(surf, f"{prochain['nom']} : record de {prochain['distance']} m",
                      80, COULEUR_GRIS)

    if jeu["attente"] > 45 and jeu["attente"] // 30 % 2 == 0:
        ecrire_centre(surf, "ESPACE : menu", 92)


# ============================================================
# Le record, gardé dans un fichier
# ============================================================
# Un fichier texte tout simple, record.txt, à côté du jeu. Tu peux
# l'ouvrir dans Thonny : il contient juste un nombre.

FICHIER_RECORD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "record.txt")


def lire_record():
    try:
        with open(FICHIER_RECORD) as fichier:
            return int(fichier.read().strip())
    except (OSError, ValueError):
        return 0                                 # pas encore de fichier : record de 0


def sauver_record(record):
    with open(FICHIER_RECORD, "w") as fichier:
        fichier.write(str(record))
